try:
    import matlab.engine
except Exception:
    pass

import os
import datajoint as dj

dj.config["filepath_checksum_size_limit"] = 1000000000

if "custom" not in dj.config:
    dj.config["custom"] = {}

# overwrite dj.config["custom"] values with environment variables if available

dj.config["custom"]["database.prefix"] = os.getenv(
    "DATABASE_PREFIX", dj.config["custom"].get("database.prefix", "")
)

dj.config["custom"]["ephys_root_data_dir"] = os.getenv(
    "EPHYS_ROOT_DATA_DIR", dj.config["custom"].get("ephys_root_data_dir", "")
)

dj.config["custom"]["ephys_processed_data_dir"] = os.getenv(
    "EPHYS_PROCESSED_DATA_DIR", dj.config["custom"].get("ephys_processed_data_dir", "")
)


db_prefix = dj.config["custom"].get("database.prefix", "")

worker_max_idled_cycle = int(
    os.getenv(
        "WORKER_MAX_IDLED_CYCLE", dj.config["custom"].get("worker_max_idled_cycle", 3)
    )
)
