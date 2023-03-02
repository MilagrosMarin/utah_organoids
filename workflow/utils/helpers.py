from pathlib import Path
import datajoint as dj
import numpy as np
import yaml

from workflow.pipeline import probe
from workflow.utils.paths import get_ephys_root_data_dir

logger = dj.logger


def get_probe_info() -> list[dict]:
    """Find probe.yaml in the root directory."""
    try:
        probe_meta_file = next(get_ephys_root_data_dir().glob("probe.yaml"))
    except StopIteration:
        raise FileNotFoundError("probe.yaml not found in the root data directory")
    else:
        with open(probe_meta_file, "r") as f:
            return yaml.safe_load(f)


def ingest_probe() -> None:
    """Fetch probe meta information from probe.yaml file in the ephys root directory to populate probe schema."""

    probe_info = get_probe_info()

    for probe_config_id, probe_config in probe_info.items():
        probe.ProbeType.insert1(
            dict(probe_type=probe_config["config"]["probe_type"]), skip_duplicates=True
        )

        electrode_layouts = probe.build_electrode_layouts(**probe_config["config"])

        probe.ProbeType.Electrode.insert(electrode_layouts, skip_duplicates=True)

        probe.Probe.insert1(
            dict(
                probe=probe_config["serial_number"],
                probe_type=probe_config["config"]["probe_type"],
                probe_comment=probe_config["comment"],
            ),
            skip_duplicates=True,
        )

        # Insert into probe.ElectrodeConfig & probe.ElectrodeConfig.Electrode
        probe_type = probe_config["config"]["probe_type"]
        electrode_keys = [
            {"probe_type": probe_type, "channel": c, "electrode": e}
            for c, e in probe_config["channel_to_electrode_map"].items()
        ]
        probe.generate_electrode_config(
            probe_type, electrode_keys, electrode_config_name=probe_config_id
        )