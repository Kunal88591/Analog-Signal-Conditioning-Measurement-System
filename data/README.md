# Data Folder

Store measurement CSV files here.

## 1) Time-Series CSV format (for analysis.py)

Header row required.

Recommended columns:

- `time` (seconds)
- `input` (volts)  — e.g., V_AMP or V_SENSOR
- `output` (volts) — V_OUT (optional; if missing, the script will apply a modeled filter)

Example header:

```
time,input,output
```

## 2) Frequency Sweep CSV format (for sweep analysis)

Header row required.

Recommended columns:

- `freq_hz`
- `vin_v`
- `vout_v`

Example header:

```
freq_hz,vin_v,vout_v
```

Run:

```bash
python sweep_analysis.py --csv data/sweep.csv --no-show --save bode.png
```
