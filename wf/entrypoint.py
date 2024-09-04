import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Annotated, List, Optional

import requests
from flytekit.core.annotation import FlyteAnnotation
from latch.executions import rename_current_execution, report_nextflow_used_storage
from latch.ldata.path import LPath
from latch.resources.tasks import custom_task, nextflow_runtime_task
from latch.resources.workflow import workflow
from latch.types import metadata
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.nextflow.workflow import get_flag
from latch_cli.services.register.utils import import_module_by_path
from latch_cli.utils import urljoins

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

sys.stdout.reconfigure(line_buffering=True)


class Mode(Enum):
    alphafold2 = "alphafold2"
    colabfold = "colabfold"
    esmfold = "esmfold"


@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_expiration_hours": 0,
            "version": 2,
        },
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]


@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(
    pvc_name: str,
    run_name: str,
    input: LatchFile,
    outdir: LatchOutputDir,
    use_gpu: bool,
    email: Optional[str],
    multiqc_title: Optional[str],
    alphafold2_db: Optional[str],
    colabfold_db: Optional[str],
    host_url: Optional[str],
    create_colabfold_index: bool,
    esmfold_db: Optional[LatchDir],
    esmfold_model_preset: Optional[str],
    skip_multiqc: bool,
    bfd_path: Optional[LatchDir],
    small_bfd_path: Optional[LatchDir],
    alphafold2_params_path: Optional[LatchDir],
    mgnify_path: Optional[LatchDir],
    pdb70_path: Optional[LatchDir],
    pdb_mmcif_path: Optional[LatchDir],
    uniref30_alphafold2_path: Optional[LatchDir],
    uniref90_path: Optional[LatchDir],
    pdb_seqres_path: Optional[LatchDir],
    uniprot_path: Optional[LatchDir],
    colabfold_alphafold2_params_link: Optional[str],
    colabfold_db_path: Optional[LatchDir],
    uniref30_colabfold_path: Optional[str],
    colabfold_alphafold2_params_path: Optional[LatchDir],
    colabfold_alphafold2_params_tags: Optional[str],
    esmfold_params_path: Optional[LatchDir],
    multiqc_methods_description: Optional[LatchFile],
    mode: Mode,
    max_template_date: Optional[str],
    full_dbs: bool,
    alphafold2_mode: Optional[str],
    alphafold2_model_preset: Optional[str],
    colabfold_server: Optional[str],
    colabfold_model_preset: Optional[str],
    num_recycles_colabfold: Optional[int],
    use_amber: bool,
    db_load_mode: Optional[int],
    use_templates: bool,
    num_recycles_esmfold: Optional[int],
    bfd_link: Optional[str],
    small_bfd_link: Optional[str],
    alphafold2_params_link: Optional[str],
    mgnify_link: Optional[str],
    pdb70_link: Optional[str],
    pdb_mmcif_link: Optional[str],
    pdb_obsolete_link: Optional[str],
    uniref30_alphafold2_link: Optional[str],
    uniref90_link: Optional[str],
    pdb_seqres_link: Optional[str],
    uniprot_sprot_link: Optional[str],
    uniprot_trembl_link: Optional[str],
    colabfold_db_link: Optional[str],
    uniref30_colabfold_link: Optional[str],
    esmfold_3B_v1: Optional[str],
    esm2_t36_3B_UR50D: Optional[str],
    esm2_t36_3B_UR50D_contact_regression: Optional[str],
) -> None:
    shared_dir = Path("/nf-workdir")
    rename_current_execution(str(run_name))

    ignore_list = [
        "latch",
        ".latch",
        ".git",
        "nextflow",
        ".nextflow",
        "work",
        "results",
        "miniconda",
        "anaconda3",
        "mambaforge",
    ]

    shutil.copytree(
        Path("/root"),
        shared_dir,
        ignore=lambda src, names: ignore_list,
        ignore_dangling_symlinks=True,
        dirs_exist_ok=True,
    )

    profile_list = ["docker", "test"]

    if len(profile_list) == 0:
        profile_list.append("standard")

    profiles = ",".join(profile_list)

    cmd = [
        "/root/nextflow",
        "run",
        str(shared_dir / "main.nf"),
        "-work-dir",
        str(shared_dir),
        "-profile",
        profiles,
        "-c",
        "latch.config",
        "-resume",
        *get_flag("input", input),
        *get_flag("outdir", LatchOutputDir(f"{outdir.remote_path}/{run_name}")),
        *get_flag("mode", mode),
        *get_flag("use_gpu", use_gpu),
        *get_flag("email", email),
        *get_flag("multiqc_title", multiqc_title),
        *get_flag("max_template_date", max_template_date),
        *get_flag("alphafold2_db", alphafold2_db),
        *get_flag("full_dbs", full_dbs),
        *get_flag("alphafold2_mode", alphafold2_mode),
        *get_flag("alphafold2_model_preset", alphafold2_model_preset),
        *get_flag("colabfold_db", colabfold_db),
        *get_flag("colabfold_server", colabfold_server),
        *get_flag("colabfold_model_preset", colabfold_model_preset),
        *get_flag("num_recycles_colabfold", num_recycles_colabfold),
        *get_flag("use_amber", use_amber),
        *get_flag("db_load_mode", db_load_mode),
        *get_flag("host_url", host_url),
        *get_flag("use_templates", use_templates),
        *get_flag("create_colabfold_index", create_colabfold_index),
        *get_flag("esmfold_db", esmfold_db),
        *get_flag("num_recycles_esmfold", num_recycles_esmfold),
        *get_flag("esmfold_model_preset", esmfold_model_preset),
        *get_flag("skip_multiqc", skip_multiqc),
        *get_flag("bfd_link", bfd_link),
        *get_flag("small_bfd_link", small_bfd_link),
        *get_flag("alphafold2_params_link", alphafold2_params_link),
        *get_flag("mgnify_link", mgnify_link),
        *get_flag("pdb70_link", pdb70_link),
        *get_flag("pdb_mmcif_link", pdb_mmcif_link),
        *get_flag("pdb_obsolete_link", pdb_obsolete_link),
        *get_flag("uniref30_alphafold2_link", uniref30_alphafold2_link),
        *get_flag("uniref90_link", uniref90_link),
        *get_flag("pdb_seqres_link", pdb_seqres_link),
        *get_flag("uniprot_sprot_link", uniprot_sprot_link),
        *get_flag("uniprot_trembl_link", uniprot_trembl_link),
        *get_flag("bfd_path", bfd_path),
        *get_flag("small_bfd_path", small_bfd_path),
        *get_flag("alphafold2_params_path", alphafold2_params_path),
        *get_flag("mgnify_path", mgnify_path),
        *get_flag("pdb70_path", pdb70_path),
        *get_flag("pdb_mmcif_path", pdb_mmcif_path),
        *get_flag("uniref30_alphafold2_path", uniref30_alphafold2_path),
        *get_flag("uniref90_path", uniref90_path),
        *get_flag("pdb_seqres_path", pdb_seqres_path),
        *get_flag("uniprot_path", uniprot_path),
        *get_flag("colabfold_db_link", colabfold_db_link),
        *get_flag("uniref30_colabfold_link", uniref30_colabfold_link),
        *get_flag("colabfold_alphafold2_params_link", colabfold_alphafold2_params_link),
        *get_flag("colabfold_db_path", colabfold_db_path),
        *get_flag("uniref30_colabfold_path", uniref30_colabfold_path),
        *get_flag("colabfold_alphafold2_params_path", colabfold_alphafold2_params_path),
        *get_flag("colabfold_alphafold2_params_tags", colabfold_alphafold2_params_tags),
        *get_flag("esmfold_3B_v1", esmfold_3B_v1),
        *get_flag("esm2_t36_3B_UR50D", esm2_t36_3B_UR50D),
        *get_flag(
            "esm2_t36_3B_UR50D_contact_regression", esm2_t36_3B_UR50D_contact_regression
        ),
        *get_flag("esmfold_params_path", esmfold_params_path),
        *get_flag("multiqc_methods_description", multiqc_methods_description),
    ]

    print("Launching Nextflow Runtime")
    print(" ".join(cmd))
    print(flush=True)

    failed = False
    try:
        env = {
            **os.environ,
            "NXF_ANSI_LOG": "false",
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms1536M -Xmx6144M -XX:ActiveProcessorCount=4",
            "NXF_DISABLE_CHECK_LATEST": "true",
            "NXF_ENABLE_VIRTUAL_THREADS": "false",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    except subprocess.CalledProcessError:
        failed = True
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(
                    urljoins(
                        "latch:///your_log_dir/nf_nf_core_proteinfold",
                        name,
                        "nextflow.log",
                    )
                )
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)

        print("Computing size of workdir... ", end="")
        try:
            result = subprocess.run(
                ["du", "-sb", str(shared_dir)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5 * 60,
            )

            size = int(result.stdout.split()[0])
            report_nextflow_used_storage(size)
            print(f"Done. Workdir size: {size / 1024 / 1024 / 1024: .2f} GiB")
        except subprocess.TimeoutExpired:
            print(
                "Failed to compute storage size: Operation timed out after 5 minutes."
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to compute storage size: {e.stderr}")
        except Exception as e:
            print(f"Failed to compute storage size: {e}")

    if failed:
        sys.exit(1)


@workflow(metadata._nextflow_metadata)
def nf_nf_core_proteinfold(
    run_name: str,
    input: LatchFile,
    outdir: LatchOutputDir,
    use_gpu: bool,
    email: Optional[str],
    multiqc_title: Optional[str],
    alphafold2_db: Optional[str],
    colabfold_db: Optional[str],
    host_url: Optional[str],
    create_colabfold_index: bool,
    esmfold_db: Optional[LatchDir],
    esmfold_model_preset: Optional[str],
    skip_multiqc: bool,
    bfd_path: Optional[LatchDir],
    small_bfd_path: Optional[LatchDir],
    alphafold2_params_path: Optional[LatchDir],
    mgnify_path: Optional[LatchDir],
    pdb70_path: Optional[LatchDir],
    pdb_mmcif_path: Optional[LatchDir],
    uniref30_alphafold2_path: Optional[LatchDir],
    uniref90_path: Optional[LatchDir],
    pdb_seqres_path: Optional[LatchDir],
    uniprot_path: Optional[LatchDir],
    colabfold_alphafold2_params_link: Optional[str],
    colabfold_db_path: Optional[LatchDir],
    uniref30_colabfold_path: Optional[str],
    colabfold_alphafold2_params_path: Optional[LatchDir],
    colabfold_alphafold2_params_tags: Optional[str],
    esmfold_params_path: Optional[LatchDir],
    multiqc_methods_description: Optional[LatchFile],
    mode: Mode = Mode.alphafold2,
    max_template_date: Optional[str] = "2020-05-14",
    full_dbs: bool = False,
    alphafold2_mode: Optional[str] = "standard",
    alphafold2_model_preset: Optional[str] = "monomer",
    colabfold_server: Optional[str] = "webserver",
    colabfold_model_preset: Optional[str] = "alphafold2_ptm",
    num_recycles_colabfold: Optional[int] = 3,
    use_amber: bool = True,
    db_load_mode: Optional[int] = 0,
    use_templates: bool = True,
    num_recycles_esmfold: Optional[int] = 4,
    bfd_link: Optional[
        str
    ] = "https://storage.googleapis.com/alphafold-databases/casp14_versions/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt.tar.gz",
    small_bfd_link: Optional[
        str
    ] = "https://storage.googleapis.com/alphafold-databases/reduced_dbs/bfd-first_non_consensus_sequences.fasta.gz",
    alphafold2_params_link: Optional[
        str
    ] = "https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar",
    mgnify_link: Optional[
        str
    ] = "https://storage.googleapis.com/alphafold-databases/v2.3/mgy_clusters_2022_05.fa.gz",
    pdb70_link: Optional[
        str
    ] = "http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/pdb70_from_mmcif_200916.tar.gz",
    pdb_mmcif_link: Optional[
        str
    ] = "rsync.rcsb.org::ftp_data/structures/divided/mmCIF/",
    pdb_obsolete_link: Optional[
        str
    ] = "https://files.wwpdb.org/pub/pdb/data/status/obsolete.dat",
    uniref30_alphafold2_link: Optional[
        str
    ] = "https://storage.googleapis.com/alphafold-databases/v2.3/UniRef30_2021_03.tar.gz",
    uniref90_link: Optional[
        str
    ] = "https://ftp.ebi.ac.uk/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz",
    pdb_seqres_link: Optional[
        str
    ] = "https://files.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt",
    uniprot_sprot_link: Optional[
        str
    ] = "https://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz",
    uniprot_trembl_link: Optional[
        str
    ] = "https://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz",
    colabfold_db_link: Optional[
        str
    ] = "http://wwwuser.gwdg.de/~compbiol/colabfold/colabfold_envdb_202108.tar.gz",
    uniref30_colabfold_link: Optional[
        str
    ] = "https://wwwuser.gwdg.de/~compbiol/colabfold/uniref30_2302.tar.gz",
    esmfold_3B_v1: Optional[
        str
    ] = "https://dl.fbaipublicfiles.com/fair-esm/models/esmfold_3B_v1.pt",
    esm2_t36_3B_UR50D: Optional[
        str
    ] = "https://dl.fbaipublicfiles.com/fair-esm/models/esm2_t36_3B_UR50D.pt",
    esm2_t36_3B_UR50D_contact_regression: Optional[
        str
    ] = "https://dl.fbaipublicfiles.com/fair-esm/regression/esm2_t36_3B_UR50D-contact-regression.pt",
) -> None:
    """
    nf-core/proteinfold

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(
        run_name=run_name,
        pvc_name=pvc_name,
        input=input,
        outdir=outdir,
        mode=mode,
        use_gpu=use_gpu,
        email=email,
        multiqc_title=multiqc_title,
        max_template_date=max_template_date,
        alphafold2_db=alphafold2_db,
        full_dbs=full_dbs,
        alphafold2_mode=alphafold2_mode,
        alphafold2_model_preset=alphafold2_model_preset,
        colabfold_db=colabfold_db,
        colabfold_server=colabfold_server,
        colabfold_model_preset=colabfold_model_preset,
        num_recycles_colabfold=num_recycles_colabfold,
        use_amber=use_amber,
        db_load_mode=db_load_mode,
        host_url=host_url,
        use_templates=use_templates,
        create_colabfold_index=create_colabfold_index,
        esmfold_db=esmfold_db,
        num_recycles_esmfold=num_recycles_esmfold,
        esmfold_model_preset=esmfold_model_preset,
        skip_multiqc=skip_multiqc,
        bfd_link=bfd_link,
        small_bfd_link=small_bfd_link,
        alphafold2_params_link=alphafold2_params_link,
        mgnify_link=mgnify_link,
        pdb70_link=pdb70_link,
        pdb_mmcif_link=pdb_mmcif_link,
        pdb_obsolete_link=pdb_obsolete_link,
        uniref30_alphafold2_link=uniref30_alphafold2_link,
        uniref90_link=uniref90_link,
        pdb_seqres_link=pdb_seqres_link,
        uniprot_sprot_link=uniprot_sprot_link,
        uniprot_trembl_link=uniprot_trembl_link,
        bfd_path=bfd_path,
        small_bfd_path=small_bfd_path,
        alphafold2_params_path=alphafold2_params_path,
        mgnify_path=mgnify_path,
        pdb70_path=pdb70_path,
        pdb_mmcif_path=pdb_mmcif_path,
        uniref30_alphafold2_path=uniref30_alphafold2_path,
        uniref90_path=uniref90_path,
        pdb_seqres_path=pdb_seqres_path,
        uniprot_path=uniprot_path,
        colabfold_db_link=colabfold_db_link,
        uniref30_colabfold_link=uniref30_colabfold_link,
        colabfold_alphafold2_params_link=colabfold_alphafold2_params_link,
        colabfold_db_path=colabfold_db_path,
        uniref30_colabfold_path=uniref30_colabfold_path,
        colabfold_alphafold2_params_path=colabfold_alphafold2_params_path,
        colabfold_alphafold2_params_tags=colabfold_alphafold2_params_tags,
        esmfold_3B_v1=esmfold_3B_v1,
        esm2_t36_3B_UR50D=esm2_t36_3B_UR50D,
        esm2_t36_3B_UR50D_contact_regression=esm2_t36_3B_UR50D_contact_regression,
        esmfold_params_path=esmfold_params_path,
        multiqc_methods_description=multiqc_methods_description,
    )
