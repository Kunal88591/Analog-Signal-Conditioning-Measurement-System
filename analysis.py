"""CLI wrapper for scripts/analysis.py.

This repository is simulation-first. Use this entrypoint for convenience.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts import analysis as analysis_lib


def main() -> None:
    parser = argparse.ArgumentParser(description="Time-series analysis (simulation-first).")
    parser.add_argument("--csv", type=Path, help="CSV file with named columns")
    parser.add_argument("--time-col", default="time", help="Time column name in the CSV file")
    parser.add_argument("--input-col", default="input", help="Input signal column name in the CSV file")
    parser.add_argument("--output-col", default=None, help="Output signal column name in the CSV file")
    parser.add_argument("--cutoff", type=float, default=10.0, help="Cutoff frequency used when filtering demo data")
    parser.add_argument("--save", type=Path, default=None, help="Save plots to a PNG instead of (or in addition to) showing")
    parser.add_argument("--no-show", action="store_true", help="Do not open an interactive plot window")
    args = parser.parse_args()

    show = not args.no_show

    if args.csv is not None:
        time, input_signal, output_signal = analysis_lib.load_csv(
            args.csv,
            time_col=args.time_col,
            input_col=args.input_col,
            output_col=args.output_col,
        )

        if output_signal is None:
            sample_rate = 1.0 / float((time[1:] - time[:-1]).mean())
            output_signal = analysis_lib.butterworth_lowpass_biquad(input_signal, sample_rate=sample_rate, cutoff_hz=args.cutoff)

        analysis_lib.plot_signals(time, input_signal, output_signal, "Measured Input vs Output", save_path=args.save, show=show)
        print(analysis_lib.summarize_noise_reduction(time, input_signal, output_signal, cutoff_hz=args.cutoff))
        return

    time, input_signal, output_signal, clean = analysis_lib.generate_demo_data(cutoff_hz=args.cutoff)
    analysis_lib.plot_signals(time, input_signal, output_signal, "Demo Input vs Output", save_path=args.save, show=show)
    print(analysis_lib.summarize_noise_reduction(time, input_signal, output_signal, cutoff_hz=args.cutoff))


if __name__ == "__main__":
    main()
