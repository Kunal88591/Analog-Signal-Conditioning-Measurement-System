"""CLI wrapper for scripts/sweep_analysis.py."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from scripts import sweep_analysis as sweep_lib


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep analysis (simulation-first).")
    parser.add_argument("--csv", type=Path, required=True, help="Sweep CSV file")
    parser.add_argument("--freq-col", default="freq_hz", help="Frequency column name")
    parser.add_argument("--vin-col", default="vin_v", help="Input amplitude column name")
    parser.add_argument("--vout-col", default="vout_v", help="Output amplitude column name")
    parser.add_argument("--save", type=Path, default=None, help="Save plot to PNG")
    parser.add_argument("--no-show", action="store_true", help="Do not open an interactive plot window")
    parser.add_argument("--passband-max-hz", type=float, default=2.0, help="Max frequency used to estimate passband gain (Hz)")
    args = parser.parse_args()

    show = not args.no_show

    freq, vin, vout = sweep_lib.load_sweep_csv(args.csv, freq_col=args.freq_col, vin_col=args.vin_col, vout_col=args.vout_col)
    gain = np.where(vin != 0, vout / vin, np.nan)

    valid = np.isfinite(freq) & np.isfinite(gain) & (freq > 0) & (gain > 0)
    freq = freq[valid]
    gain = gain[valid]

    passband = sweep_lib.estimate_passband_gain(freq, gain, max_passband_hz=args.passband_max_hz)
    fc = sweep_lib.find_cutoff(freq, gain, passband_gain=passband)

    print(f"Estimated passband gain: {passband:.3f} ({20.0 * np.log10(passband):.2f} dB)")
    print(f"Estimated cutoff fc (-3 dB): {fc:.2f} Hz")

    sweep_lib.plot_bode(freq, gain, fc_hz=fc, passband_gain=passband, save_path=args.save, show=show)


if __name__ == "__main__":
    main()
