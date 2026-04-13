"""Frequency-sweep analysis to estimate -3 dB cutoff.

Expected CSV columns (header row required):
- freq_hz
- vin_v
- vout_v

Outputs:
- estimated passband gain
- estimated cutoff frequency (first -3 dB crossing)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_sweep_csv(path: Path, freq_col: str = "freq_hz", vin_col: str = "vin_v", vout_col: str = "vout_v"):
    data = np.genfromtxt(path, delimiter=",", names=True, dtype=float)
    if data.dtype.names is None:
        raise ValueError("CSV file must contain a header row with named columns.")

    freq = np.asarray(data[freq_col], dtype=float)
    vin = np.asarray(data[vin_col], dtype=float)
    vout = np.asarray(data[vout_col], dtype=float)

    if freq.size < 5:
        raise ValueError("Need at least ~5 sweep points to estimate cutoff.")

    return freq, vin, vout


def estimate_passband_gain(freq: np.ndarray, gain: np.ndarray, max_passband_hz: float = 2.0) -> float:
    low = gain[freq <= max_passband_hz]
    if low.size < 3:
        low = gain[:3]
    return float(np.median(low))


def find_cutoff(freq: np.ndarray, gain: np.ndarray, passband_gain: float) -> float:
    target = passband_gain / np.sqrt(2.0)

    order = np.argsort(freq)
    freq = freq[order]
    gain = gain[order]

    below = np.where(gain <= target)[0]
    if below.size == 0:
        raise ValueError("No -3 dB crossing found in sweep range (gain never falls below target).")

    idx = int(below[0])
    if idx == 0:
        return float(freq[0])

    f1, f2 = float(freq[idx - 1]), float(freq[idx])
    g1, g2 = float(gain[idx - 1]), float(gain[idx])

    x1, x2 = np.log10(f1), np.log10(f2)
    if g2 == g1:
        x = x2
    else:
        x = x1 + (target - g1) * (x2 - x1) / (g2 - g1)

    return float(10**x)


def plot_bode(freq: np.ndarray, gain: np.ndarray, *, fc_hz: float, passband_gain: float, save_path: Path | None, show: bool):
    gain_db = 20.0 * np.log10(gain)
    passband_db = 20.0 * np.log10(passband_gain)

    fig, ax = plt.subplots(figsize=(9, 5), constrained_layout=True)
    ax.semilogx(freq, gain_db, marker="o", linewidth=1.5, label="Measured")
    ax.axhline(passband_db, linestyle="--", linewidth=1.2, label="Passband")
    ax.axhline(passband_db - 3.0, linestyle=":", linewidth=1.2, label="-3 dB")
    ax.axvline(fc_hz, linestyle="-.", linewidth=1.2, label=f"fc={fc_hz:.2f} Hz")

    ax.set_title("Low-Pass Filter Bode Magnitude")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()

    if save_path is not None:
        fig.savefig(save_path, dpi=160)

    if show:
        plt.show()
    else:
        plt.close(fig)
