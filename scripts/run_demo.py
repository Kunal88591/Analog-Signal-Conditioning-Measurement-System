"""Generate fully reproducible demo outputs (no hardware required).

Creates:
- results/demo.png : time + FFT plots
- results/bode.png : synthetic sweep Bode magnitude with extracted fc

Run:
- MPLBACKEND=Agg python scripts/run_demo.py
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import analysis as analysis_lib
from scripts import sweep_analysis as sweep_lib


def write_synthetic_sweep_csv(path: Path, *, fc_hz: float = 10.0) -> None:
    freq = np.logspace(np.log10(0.5), np.log10(100.0), 25)
    w = freq / fc_hz
    # 2nd-order Butterworth magnitude (analog prototype)
    mag = 1.0 / np.sqrt(1.0 + w**4)
    vin = np.full_like(freq, 0.1)
    vout = vin * mag

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write("freq_hz,vin_v,vout_v\n")
        for f, i, o in zip(freq, vin, vout):
            handle.write(f"{f},{i},{o}\n")


def main() -> None:
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # Demo time-series plot
    t, x, y, _clean = analysis_lib.generate_demo_data(cutoff_hz=10.0)
    analysis_lib.plot_signals(t, x, y, "Demo Input vs Output", save_path=results_dir / "demo.png", show=False)
    print(analysis_lib.summarize_noise_reduction(t, x, y, cutoff_hz=10.0))

    # Demo sweep plot
    sweep_csv = results_dir / "synthetic_sweep.csv"
    write_synthetic_sweep_csv(sweep_csv, fc_hz=10.0)
    freq, vin, vout = sweep_lib.load_sweep_csv(sweep_csv)
    gain = vout / vin
    passband = sweep_lib.estimate_passband_gain(freq, gain)
    fc = sweep_lib.find_cutoff(freq, gain, passband_gain=passband)
    print(f"Synthetic sweep extracted fc: {fc:.2f} Hz")
    sweep_lib.plot_bode(freq, gain, fc_hz=fc, passband_gain=passband, save_path=results_dir / "bode.png", show=False)


if __name__ == "__main__":
    main()