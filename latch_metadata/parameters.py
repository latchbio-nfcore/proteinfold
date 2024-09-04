from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flytekit.core.annotation import FlyteAnnotation
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import (
    Fork,
    ForkBranch,
    LatchAuthor,
    NextflowMetadata,
    NextflowParameter,
    NextflowRuntimeResources,
    Params,
    Section,
    Spoiler,
    Text,
)


class Mode(Enum):
    alphafold2 = "alphafold2"
    colabfold = "colabfold"
    esmfold = "esmfold"


flow = [
    Section(
        "Input",
        Params(
            "input",
            "run_name",
            "outdir",
            "mode",
        ),
    ),
    Section(
        "Alphafold2 options",
        Params(
            "max_template_date",
            "alphafold2_db",
            "full_dbs",
            "alphafold2_mode",
            "alphafold2_model_preset",
        ),
    ),
    Section(
        "Colabfold options",
        Params(
            "colabfold_db",
            "colabfold_server",
            "colabfold_model_preset",
            "num_recycles_colabfold",
            "use_amber",
            "db_load_mode",
            "host_url",
            "use_templates",
            "create_colabfold_index",
        ),
    ),
    Section(
        "Esmfold options",
        Params(
            "esmfold_db",
            "num_recycles_esmfold",
            "esmfold_model_preset",
        ),
    ),
    Section(
        "Process skipping options",
        Params(
            "skip_multiqc",
        ),
    ),
    Spoiler(
        "Advanced options",
        Section(
            "General options",
            Params(
                "use_gpu",
                "email",
                "multiqc_title",
            ),
        ),
        Section(
            "Alphafold2 DBs and parameters links options",
            Params(
                "bfd_link",
                "small_bfd_link",
                "alphafold2_params_link",
                "mgnify_link",
                "pdb70_link",
                "pdb_mmcif_link",
                "pdb_obsolete_link",
                "uniref30_alphafold2_link",
                "uniref90_link",
                "pdb_seqres_link",
                "uniprot_sprot_link",
                "uniprot_trembl_link",
            ),
        ),
        Section(
            "Alphafold2 DBs and parameters paths options",
            Params(
                "bfd_path",
                "small_bfd_path",
                "alphafold2_params_path",
                "mgnify_path",
                "pdb70_path",
                "pdb_mmcif_path",
                "uniref30_alphafold2_path",
                "uniref90_path",
                "pdb_seqres_path",
                "uniprot_path",
            ),
        ),
        Section(
            "Colabfold DBs and parameters links options",
            Params(
                "colabfold_db_link",
                "uniref30_colabfold_link",
                "colabfold_alphafold2_params_link",
            ),
        ),
        Section(
            "Colabfold DBs and parameters paths options",
            Params(
                "colabfold_db_path",
                "uniref30_colabfold_path",
                "colabfold_alphafold2_params_path",
                "colabfold_alphafold2_params_tags",
            ),
        ),
        Section(
            "Esmfold parameters links options",
            Params(
                "esmfold_3B_v1",
                "esm2_t36_3B_UR50D",
                "esm2_t36_3B_UR50D_contact_regression",
            ),
        ),
        Section(
            "Esmfold parameters paths options",
            Params(
                "esmfold_params_path",
            ),
        ),
    ),
    Section(
        "Generic options",
        Params(
            "multiqc_methods_description",
        ),
    ),
]

generated_parameters = {
    "run_name": NextflowParameter(
        type=str,
        display_name="Run Name",
        description="Name of run",
        batch_table_column=True,
    ),
    "input": NextflowParameter(
        type=LatchFile,
        display_name="Input CSV",
        default=None,
        description="Path to comma-separated file containing information about the samples in the experiment.",
    ),
    "outdir": NextflowParameter(
        type=LatchOutputDir,
        display_name="Output Directory",
        default=None,
        description="The output directory where the results will be saved.",
    ),
    "mode": NextflowParameter(
        type=Mode,
        display_name="Pipeline Mode",
        default=Mode.alphafold2,
        description="Specifies the mode in which the pipeline will be run",
    ),
    "use_gpu": NextflowParameter(
        type=bool,
        display_name="Use GPU",
        default=None,
        description="Run on CPUs (default) or GPUs",
    ),
    "email": NextflowParameter(
        type=Optional[str],
        display_name="Email",
        default=None,
        description="Email address for completion summary.",
    ),
    "multiqc_title": NextflowParameter(
        type=Optional[str],
        display_name="MultiQC Title",
        default=None,
        description="MultiQC report title. Printed as page header, used for filename if not otherwise specified.",
    ),
    "max_template_date": NextflowParameter(
        type=Optional[str],
        display_name="Max Template Date",
        default="2020-05-14",
        description="Maximum date of the PDB templates used by 'AlphaFold2' mode",
    ),
    "alphafold2_db": NextflowParameter(
        type=Optional[str],
        display_name="AlphaFold2 DB",
        default=None,
        description="Specifies the DB and PARAMS path used by 'AlphaFold2' mode",
    ),
    "full_dbs": NextflowParameter(
        type=bool,
        display_name="Use Full DBs",
        default=False,
        description="If true uses the full version of the BFD database otherwise, otherwise it uses its reduced version, small bfd",
    ),
    "alphafold2_mode": NextflowParameter(
        type=Optional[str],
        display_name="AlphaFold2 Mode",
        default="standard",
        description="Specifies the mode in which Alphafold2 will be run",
    ),
    "alphafold2_model_preset": NextflowParameter(
        type=Optional[str],
        display_name="AlphaFold2 Model Preset",
        default="monomer",
        description="Model preset for 'AlphaFold2' mode",
    ),
    "colabfold_db": NextflowParameter(
        type=Optional[str],
        display_name="ColabFold DB",
        default=None,
        description="Specifies the PARAMS and DB path used by 'colabfold'  mode",
    ),
    "colabfold_server": NextflowParameter(
        type=Optional[str],
        display_name="ColabFold Server",
        default="webserver",
        description="Specifies the MSA server used by Colabfold",
    ),
    "colabfold_model_preset": NextflowParameter(
        type=Optional[str],
        display_name="ColabFold Model Preset",
        default="alphafold2_ptm",
        description="Model preset for 'colabfold' mode",
    ),
    "num_recycles_colabfold": NextflowParameter(
        type=Optional[int],
        display_name="ColabFold Recycles",
        default=3,
        description="Number of recycles for Colabfold",
    ),
    "use_amber": NextflowParameter(
        type=bool,
        display_name="Use Amber",
        default=True,
        description="Use Amber minimization to refine the predicted structures",
    ),
    "db_load_mode": NextflowParameter(
        type=Optional[int],
        display_name="DB Load Mode",
        default=0,
        description="Specify the way that MMSeqs2 will load the required databases in memory",
    ),
    "host_url": NextflowParameter(
        type=Optional[str],
        display_name="Host URL",
        default=None,
        description="Specify your custom MMSeqs2 API server url",
    ),
    "use_templates": NextflowParameter(
        type=bool,
        display_name="Use Templates",
        default=True,
        description="Use PDB templates",
    ),
    "create_colabfold_index": NextflowParameter(
        type=bool,
        display_name="Create ColabFold Index",
        default=None,
        description="Create databases indexes when running colabfold_local mode",
    ),
    "esmfold_db": NextflowParameter(
        type=Optional[str],
        display_name="ESMFold DB",
        default=None,
        description="Specifies the PARAMS path used by 'esmfold' mode",
    ),
    "num_recycles_esmfold": NextflowParameter(
        type=Optional[int],
        display_name="ESMFold Recycles",
        default=4,
        description="Specifies the number of recycles used by Esmfold",
    ),
    "esmfold_model_preset": NextflowParameter(
        type=Optional[str],
        display_name="ESMFold Model Preset",
        default=None,
        description="Specifies whether is a 'monomer' or 'multimer' prediction",
    ),
    "skip_multiqc": NextflowParameter(
        type=bool,
        display_name="Skip MultiQC",
        default=None,
        description="Skip MultiQC.",
    ),
    "bfd_link": NextflowParameter(
        type=Optional[str],
        display_name="BFD Database Link",
        default="https://storage.googleapis.com/alphafold-databases/casp14_versions/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt.tar.gz",
        description="Link to BFD dababase",
    ),
    "small_bfd_link": NextflowParameter(
        type=Optional[str],
        display_name="Small BFD Link",
        default="https://storage.googleapis.com/alphafold-databases/reduced_dbs/bfd-first_non_consensus_sequences.fasta.gz",
        description="Link to a reduced version of the BFD dababase",
    ),
    "alphafold2_params_link": NextflowParameter(
        type=Optional[str],
        display_name="AlphaFold2 Params Link",
        default="https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar",
        description="Link to the Alphafold2 parameters",
    ),
    "mgnify_link": NextflowParameter(
        type=Optional[str],
        display_name="MGnify Link",
        default="https://storage.googleapis.com/alphafold-databases/v2.3/mgy_clusters_2022_05.fa.gz",
        description="Link to the MGnify database",
    ),
    "pdb70_link": NextflowParameter(
        type=Optional[str],
        display_name="PDB70 Link",
        default="http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/pdb70_from_mmcif_200916.tar.gz",
        description="Link to the PDB70 database",
    ),
    "pdb_mmcif_link": NextflowParameter(
        type=Optional[str],
        display_name="PDB mmCIF Link",
        default="rsync.rcsb.org::ftp_data/structures/divided/mmCIF/",
        description="Link to the PDB mmCIF database",
    ),
    "pdb_obsolete_link": NextflowParameter(
        type=Optional[str],
        display_name="PDB Obsolete Link",
        default="https://files.wwpdb.org/pub/pdb/data/status/obsolete.dat",
        description="Link to the PDB obsolete database",
    ),
    "uniref30_alphafold2_link": NextflowParameter(
        type=Optional[str],
        display_name="UniRef30 AlphaFold2 Link",
        default="https://storage.googleapis.com/alphafold-databases/v2.3/UniRef30_2021_03.tar.gz",
        description="Link to the Uniclust30 database",
    ),
    "uniref90_link": NextflowParameter(
        type=Optional[str],
        display_name="UniRef90 Link",
        default="https://ftp.ebi.ac.uk/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz",
        description="Link to the UniRef90 database",
    ),
    "pdb_seqres_link": NextflowParameter(
        type=Optional[str],
        display_name="PDB SEQRES Link",
        default="https://files.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt",
        description="Link to the PDB SEQRES database",
    ),
    "uniprot_sprot_link": NextflowParameter(
        type=Optional[str],
        display_name="UniProt Swiss-Prot Link",
        default="https://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz",
        description="Link to the SwissProt UniProt database",
    ),
    "uniprot_trembl_link": NextflowParameter(
        type=Optional[str],
        display_name="UniProt TrEMBL Link",
        default="https://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz",
        description="Link to the TrEMBL UniProt database",
    ),
    "bfd_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="BFD Path",
        default=None,
        description="Path to BFD dababase",
    ),
    "small_bfd_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="Small BFD Path",
        default=None,
        description="Path to a reduced version of the BFD database",
    ),
    "alphafold2_params_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="AlphaFold2 Params Path",
        default=None,
        description="Path to the Alphafold2 parameters",
    ),
    "mgnify_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="MGnify Path",
        default=None,
        description="Path to the MGnify database",
    ),
    "pdb70_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="PDB70 Path",
        default=None,
        description="Path to the PDB70 database",
    ),
    "pdb_mmcif_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="PDB mmCIF Path",
        default=None,
        description="Path to the PDB mmCIF database",
    ),
    "uniref30_alphafold2_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="UniRef30 AlphaFold2 Path",
        default=None,
        description="Path to the Uniref30 database",
    ),
    "uniref90_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="UniRef90 Path",
        default=None,
        description="Path to the UniRef90 database",
    ),
    "pdb_seqres_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="PDB SEQRES Path",
        default=None,
        description="Path to the PDB SEQRES database",
    ),
    "uniprot_path": NextflowParameter(
        type=Optional[LatchDir],
        display_name="UniProt Path",
        default=None,
        description="Path to UniProt database containing the SwissProt and the TrEMBL databases",
    ),
    "colabfold_db_link": NextflowParameter(
        type=Optional[str],
        display_name="ColabFold DB Link",
        default="http://wwwuser.gwdg.de/~compbiol/colabfold/colabfold_envdb_202108.tar.gz",
        description="Link to the Colabfold database",
    ),
    "uniref30_colabfold_link": NextflowParameter(
        type=Optional[str],
        display_name="UniRef30 ColabFold Link",
        default="https://wwwuser.gwdg.de/~compbiol/colabfold/uniref30_2302.tar.gz",
        description="Link to the UniRef30 database",
    ),
    "colabfold_alphafold2_params_link": NextflowParameter(
        type=Optional[str],
        display_name="ColabFold AlphaFold2 Params Link",
        default=None,
        description="Link to the Alphafold2 parameters for Colabfold",
    ),
    "colabfold_db_path": NextflowParameter(
        type=Optional[str],
        display_name="ColabFold DB Path",
        default=None,
        description="Link to the Colabfold database",
    ),
    "uniref30_colabfold_path": NextflowParameter(
        type=Optional[str],
        display_name="UniRef30 ColabFold Path",
        default=None,
        description="Link to the UniRef30 database",
    ),
    "colabfold_alphafold2_params_path": NextflowParameter(
        type=Optional[str],
        display_name="ColabFold AlphaFold2 Params Path",
        default=None,
        description="Link to the Alphafold2 parameters for Colabfold",
    ),
    "colabfold_alphafold2_params_tags": NextflowParameter(
        type=Optional[str],
        display_name="ColabFold AlphaFold2 Params Tags",
        default=None,
        description="Dictionary with Alphafold2 parameters tags",
    ),
    "esmfold_3B_v1": NextflowParameter(
        type=Optional[str],
        display_name="ESMFold 3B v1",
        default="https://dl.fbaipublicfiles.com/fair-esm/models/esmfold_3B_v1.pt",
        description="Link to the Esmfold 3B-v1 model",
    ),
    "esm2_t36_3B_UR50D": NextflowParameter(
        type=Optional[str],
        display_name="ESM2 t36 3B UR50D Model",
        default="https://dl.fbaipublicfiles.com/fair-esm/models/esm2_t36_3B_UR50D.pt",
        description="Link to the Esmfold t36-3B-UR50D model",
    ),
    "esm2_t36_3B_UR50D_contact_regression": NextflowParameter(
        type=Optional[str],
        display_name="ESM2 t36 3B UR50D Contact Regression",
        default="https://dl.fbaipublicfiles.com/fair-esm/regression/esm2_t36_3B_UR50D-contact-regression.pt",
        description="Link to the Esmfold t36-3B-UR50D-contact-regression model",
    ),
    "esmfold_params_path": NextflowParameter(
        type=Optional[str],
        display_name="ESMFold Parameters Path",
        default=None,
        description="Link to the Esmfold parameters",
    ),
    "multiqc_methods_description": NextflowParameter(
        type=Optional[LatchFile],
        display_name="MultiQC Methods Description",
        default=None,
        description="Custom MultiQC yaml file containing HTML including a methods description.",
    ),
}
