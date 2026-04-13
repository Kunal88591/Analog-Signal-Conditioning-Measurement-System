# Error Budget (Internship-Style)

This document outlines the main contributors to output error and how to quantify them.

## 1) Sensor Error

### LM35

Key contributors:

- Sensor accuracy (datasheet): typically ±0.5 °C to ±2 °C depending on grade and conditions.
- Self-heating: depends on airflow and mounting.
- Supply sensitivity and wiring drops: minimized with local decoupling.

Convert temperature error to voltage:

- LM35 sensitivity is 10 mV/°C.
- Equivalent input error: `V_err_in = 10 mV/°C * T_err`.

Example: ±1 °C → ±10 mV at sensor output.

## 2) Amplifier Gain Error

Non-inverting gain:

- `Av = 1 + Rf/Rg`

Approximate relative gain sensitivity (small errors):

- `dAv/Av ≈ sqrt((dRf/Rf)^2 + (dRg/Rg)^2)` (first-order)

Example with ±1% resistors:

- `dAv/Av ≈ sqrt(0.01^2 + 0.01^2) = 1.41%`

## 3) Op-Amp Errors

For a single-supply LM358-class op-amp:

- Input offset voltage contributes output DC error:
  - Output offset ≈ `V_os * (noise_gain)`
  - For non-inverting amp, noise gain is `1 + Rf/Rg`.
- Input bias current causes additional offsets due to resistor drops.
- Output swing limitation near top rail can create gain compression/clipping.

Practical recommendation:

- Keep output below ~4.0 V on a 5 V supply for non-rail-to-rail parts.

## 4) Filter Cutoff Error (Tolerance Analysis)

For equal-component Sallen-Key cutoff approximation:

- `fc ≈ 1 / (2πRC)`

Relative cutoff sensitivity:

- `dfc/fc ≈ sqrt((dR/R)^2 + (dC/C)^2)`

Example:

- R ±1%, C ±10% → `dfc/fc ≈ sqrt(0.01^2 + 0.10^2) ≈ 10.05%`

This is why film/MLCC capacitors (tighter tolerance) help when you care about fc.

## 5) Putting It Together (Example)

If the project uses:

- LM35 ±1 °C typical
- Total gain ≈ 7.93

Then output error due to sensor alone:

- `V_err_out ≈ 10 mV/°C * 1 °C * 7.93 ≈ 79 mV`

This is a strong interview talking point: you can explain why calibration and component selection matter.
