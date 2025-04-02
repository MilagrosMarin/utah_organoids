import datajoint as dj
import numpy as np
from scipy import signal
from datetime import timedelta, datetime, timezone

from workflow import DB_PREFIX

from .ephys import ephys

schema = dj.schema(DB_PREFIX + "analysis")


@schema
class SpectralBand(dj.Lookup):
    definition = """
    band_name: varchar(16)
    ---
    lower_freq: float # (Hz)
    upper_freq: float # (Hz)
    """
    contents = [
        ("delta", 2.0, 4.0),
        ("theta", 4.0, 7.0),
        ("alpha", 8.0, 12.0),
        ("beta", 13.0, 30.0),
        ("gamma", 30.0, 50.0),
        ("highgamma1", 70.0, 110.0),
        ("highgamma2", 130.0, 500.0),
    ]


@schema
class SpectrogramParameters(dj.Lookup):
    definition = """
    param_idx: int
    ---
    window_size:     float    # Time in seconds
    overlap_size=0:  float    # Time in seconds
    description="":  varchar(64)
    """
    contents = [(0, 0.5, 0.0, "Default 0.5s time segments without overlap.")]


@schema
class LFPSpectrogram(dj.Computed):
    """Calculate spectrogram at each channel.

    Assumes the LFP is:
        1. Low-pass filtered at 1000 Hz.
        2. Notch filtered at 50/60 Hz.
        3. Resampled to 2500 Hz.
    """

    definition = """
    -> ephys.LFP.Trace
    -> SpectrogramParameters
    """

    class ChannelSpectrogram(dj.Part):
        definition = """
        -> master
        ---
        spectrogram: longblob # Power with dimensions (frequecy, time).
        time: longblob        # Timestamps
        frequency: longblob   # Fourier frequencies
        """

    class ChannelPower(dj.Part):
        definition = """
        -> master
        -> SpectralBand
        ---
        power: longblob   # Mean power in spectral band as a function of time
        mean_power: float # Mean power in a spectral band for a time window.
        std_power: float  # Standard deviation of the power in a spectral band for a time window.
        """

    def make(self, key):
        self.insert1(key)

        window_size, overlap_size = (SpectrogramParameters & key).fetch1(
            "window_size", "overlap_size"
        )

        lfp_sampling_rate = (ephys.LFP & key).fetch1("lfp_sampling_rate")

        lfp = (ephys.LFP.Trace & key).fetch1("lfp")
        frequency, time, Sxx = signal.spectrogram(
            lfp,
            fs=int(lfp_sampling_rate),
            nperseg=int(window_size * lfp_sampling_rate),
            noverlap=int(overlap_size * lfp_sampling_rate),
            window="boxcar",
        )

        self.ChannelSpectrogram.insert1(
            {**key, "spectrogram": Sxx, "frequency": frequency, "time": time}
        )
        band_keys, lower_frequencies, upper_frequencies = SpectralBand.fetch(
            "KEY", "lower_freq", "upper_freq"
        )
        for power_key, fl, fh in zip(band_keys, lower_frequencies, upper_frequencies):
            freq_mask = np.logical_and(frequency >= fl, frequency < fh)
            power = Sxx[freq_mask, :].mean(axis=0)  # mean across freq domain
            self.ChannelPower.insert1(
                dict(
                    **power_key,
                    **key,
                    power=power,
                    mean_power=power.mean(),
                    std_power=power.std(),
                )
            )


@schema
class SpectrogramPlot(dj.Computed):
    """
    Generate spectrogram plots for each channel per electrode.
    """

    definition = """
    -> LFPSpectrogram
    ---
    freq_min: float  # min frequency
    freq_max: float  # max frequency
    execution_duration: float  # execution duration in hours
    """

    class Channel(dj.Part):
        definition = """
        -> master
        -> LFPSpectrogram.ChannelSpectrogram
        ---
        spectrogram_plot: longblob
        """

    def make(self, key):
        execution_time = datetime.now(timezone.utc)

        # Find which frequencies are within 1–300 Hz
        FREQ_MIN = 1
        FREQ_MAX = 300

        from plotly import graph_objects as go
        import plotly.express as px

        # Fetch multiple spectrograms
        electrodes = [e for e in (LFPSpectrogram.ChannelSpectrogram).fetch("electrode")]
        spectrogram_fig = go.Figure()

        for e in electrodes:
            Sxx, t, f = (LFPSpectrogram.ChannelSpectrogram & {"electrode": e}).fetch1(
                "spectrogram", "time", "frequency"
            )
            freq_mask = (f >= FREQ_MIN) & (f <= FREQ_MAX)
            spectrogram_fig.add_trace(
                go.Heatmap(
                    z=np.log(Sxx[freq_mask, :]),
                    x=t,
                    y=f[freq_mask],
                    visible=(e == electrodes[0]),
                    colorbar=dict(title="log Power"),
                )
            )

        # Add buttons for electrode switching
        buttons = [
            dict(
                label=f"Electrode {e}",
                method="update",
                args=[{"visible": [e == i for i in electrodes]}],
            )
            for e in electrodes
        ]

        spectrogram_fig.update_layout(
            updatemenus=[dict(buttons=buttons, direction="down", x=1.05, y=1)],
            title="Spectrogram (log Power) per Electrode",
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)",
        )

        self.insert1(
            {
                **key,
                "freq_min": FREQ_MIN,
                "freq_max": FREQ_MAX,
                "execution_duration": (
                    datetime.now(timezone.utc) - execution_time
                ).total_seconds()
                / 3600,
            }
        )

        self.Channel.insert1(
            {
                **key,
                "spectrogram_plot": spectrogram_fig.to_json(),
            }
        )
