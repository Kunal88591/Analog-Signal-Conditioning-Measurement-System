"""Time-series analysis for the Analog Signal Conditioning project.

This module is intentionally software-first: it can be used with measured CSV
data (from scope/DAQ/ADC), or with a built-in synthetic demo signal.

What it does:
- Plots input vs output (time domain)
- Shows FFT magnitude (frequency domain)
- Computes a band-limited noise reduction metric above cutoff

CSV format (header required): time,input,output (output optional)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def butterworth_lowpass_biquad(signal: np.ndarray, sample_rate: float, cutoff_hz: float) -> np.ndarray:
    """2nd-order Butterworth low-pass via RBJ biquad coefficients."""

    if cutoff_hz <= 0:
        raise ValueError("cutoff_hz must be > 0")
    if sample_rate <= 0:
        raise ValueError("sample_rate must be > 0")
    if cutoff_hz >= sample_rate / 2:
        raise ValueError("cutoff_hz must be < Nyquist (sample_rate/2)")

    q = 1.0 / np.sqrt(2.0)
    w0 = 2.0 * np.pi * (cutoff_hz / sample_rate)
    cos_w0 = float(np.cos(w0))
    sin_w0 = float(np.sin(w0))
    alpha = sin_w0 / (2.0 * q)

    b0 = (1.0 - cos_w0) / 2.0
    b1 = 1.0 - cos_w0
    b2 = (1.0 - cos_w0) / 2.0
    a0 = 1.0 + alpha
    a1 = -2.0 * cos_w0
    a2 = 1.0 - alpha

    # Normalize
    b0 /= a0
    b1 /= a0
    b2 /= a0
    a1 /= a0
    a2 /= a0

    output = np.empty_like(signal, dtype=float)
    x1 = x2 = 0.0
    y1 = y2 = 0.0
    for index, x0 in enumerate(signal.astype(float)):
        y0 = b0 * x0 + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        output[index] = y0
        x2, x1 = x1, x0
        y2, y1 = y1, y0
    return output


def rms(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(values))))


def band_energy(signal: np.ndarray, sample_rate: float, f_low: float, f_high: float) -> float:
    """Relative band energy (for comparing input vs output).

    Uses the squared magnitude of the rFFT in a frequency band. This is not an
    absolute calibrated power measurement, but ratios are meaningful.
    """

    if f_low < 0 or f_high <= f_low:
        raise ValueError("Invalid band limits")

    signal = signal - float(np.mean(signal))
    spectrum = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(signal.size, d=1.0 / sample_rate)

    band = (freq >= f_low) & (freq <= f_high)
    return float(np.sum(np.abs(spectrum[band]) ** 2))


def load_csv(path: Path, time_col: str = "time", input_col: str = "input", output_col: str | None = "output"):
    data = np.genfromtxt(path, delimiter=",", names=True, dtype=float)
    if data.dtype.names is None:
        raise ValueError("CSV file must contain a header row with named columns.")

    time = np.asarray(data[time_col], dtype=float)
    input_signal = np.asarray(data[input_col], dtype=float)
    output_signal = None if output_col is None else np.asarray(data[output_col], dtype=float)
    return time, input_signal, output_signal


def generate_demo_data(sample_rate: float = 200.0, duration_s: float = 10.0, cutoff_hz: float = 10.0):
    rng = np.random.default_rng(7)
    time = np.arange(0.0, duration_s, 1.0 / sample_rate)

    clean_signal = 2.0 + 0.25 * np.sin(2.0 * np.pi * 0.2 * time)
    noise = 0.10 * np.sin(2.0 * np.pi * 25.0 * time) + 0.05 * rng.normal(size=time.size)
    input_signal = clean_signal + noise
    output_signal = butterworth_lowpass_biquad(input_signal, sample_rate=sample_rate, cutoff_hz=cutoff_hz)
    return time, input_signal, output_signal, clean_signal


def plot_signals(
    time: np.ndarray,
    input_signal: np.ndarray,
    output_signal: np.ndarray,
    title: str,
    *,
    save_path: Path | None,
    show: bool,
):
    fig, (ax_time, ax_spec) = plt.subplots(2, 1, figsize=(10, 8), constrained_layout=True)

    ax_time.plot(time, input_signal, label="Input", linewidth=1.5)
    ax_time.plot(time, output_signal, label="Output", linewidth=1.8)
    ax_time.set_title(title)
    ax_time.set_xlabel("Time (s)")
    ax_time.set_ylabel("Voltage (V)")
    ax_time.grid(True, alpha=0.3)
    ax_time.legend()

    sample_spacing = float(np.mean(np.diff(time)))
    sample_rate = 1.0 / sample_spacing
    frequency = np.fft.rfftfreq(time.size, d=sample_spacing)
    input_spectrum = np.abs(np.fft.rfft(input_signal - np.mean(input_signal)))
    output_spectrum = np.abs(np.fft.rfft(output_signal - np.mean(output_signal)))

    ax_spec.semilogy(frequency, input_spectrum + 1e-12, label="Input spectrum")
    ax_spec.semilogy(frequency, output_spectrum + 1e-12, label="Output spectrum")
    ax_spec.set_xlim(0, min(50, sample_rate / 2))
    ax_spec.set_xlabel("Frequency (Hz)")
    ax_spec.set_ylabel("Magnitude")
    ax_spec.set_title("Noise Filtering Effect")
    ax_spec.grid(True, alpha=0.3)
    ax_spec.legend()

    if save_path is not None:
        fig.savefig(save_path, dpi=160)

    if show:
        plt.show()
    else:
        plt.close(fig)


def summarize_noise_reduction(time: np.ndarray, input_signal: np.ndarray, output_signal: np.ndarray, *, cutoff_hz: float) -> str:
    sample_rate = 1.0 / float(np.mean(np.diff(time)))
    hf_low = max(cutoff_hz * 1.5, 1.0)
    hf_high = min(50.0, sample_rate / 2 - 1e-6)
    e_in = band_energy(input_signal, sample_rate, hf_low, hf_high)
    e_out = band_energy(output_signal, sample_rate, hf_low, hf_high)
    return f"HF band ({hf_low:.1f}-{hf_high:.1f} Hz) reduction: {10.0 * np.log10(e_in / e_out):.2f} dB"
