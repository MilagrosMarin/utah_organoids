import datajoint as dj
import re
from pathlib import Path
from datetime import datetime

from workflow import REL_PATH_INBOX, SUPPORT_DB_PREFIX
from workflow.pipeline import induction, ephys
from workflow.support import FileManifest, utils

logger = dj.logger  # type: ignore

schema = dj.schema(f"{SUPPORT_DB_PREFIX}ingestion_support")


@schema
class FileProcessing(dj.Imported):
    definition = """
    -> FileManifest
    ---
    execution_time: datetime  # UTC time
    log_message='': varchar(1000)
    """

    def make(self, key):
        """
        For each new file in FileManifest, process the file to attempt to:
        1. register new entries for ephys.EphysRawFile (from .rhs files)
        2. attempt to create ephys.EphysSession
        """
        log_message = ""
        remote_fullpath = Path(key["remote_fullpath"])
        if Path(REL_PATH_INBOX) in remote_fullpath.parents:
            if remote_fullpath.suffix == ".rhs": 
                filename_prefix, start_time = re.search(r"(.*)_(\d{6}_\d{6})", file).groups()
                start_time = np.datetime64(
                    datetime.strptime(start_time, "%y%m%d_%H%M%S")
                )  # start time based on the file name
                subject_key = {}      
                ephys.EphysRawFile.insert1(
                    {
                    **subject_key,
                    "file_time": start_time,
                    "file_path": remote_fullpath.as_posix(),
                    "parent_folder": remote_fullpath.parent.name,
                    "filename_prefix": filename_prefix,
                    "file": (FileManifest & key).fetch1('file'),
                    }
                )
                log_message += f"Added new raw ephys: {remote_fullpath.name}" + "\n"

        self.insert1(
            {**key, "execution_time": datetime.utcnow(), "log_message": log_message}
        )
