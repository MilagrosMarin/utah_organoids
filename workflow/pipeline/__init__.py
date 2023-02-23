from . import induction, lineage
from .ephys import ephys, probe
import os

os.environ["DJ_SUPPORT_FILEPATH_MANAGEMENT"] = "TRUE"
os.environ["EXTERN_STORE_PROTOCOL"] = "file"