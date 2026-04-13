# Calibration Notes

## Why calibrate?

Even with a good schematic, real builds drift due to:

- sensor offset and accuracy
- resistor/capacitor tolerance
- op-amp offset

Calibration converts “a working circuit” into “a measurement system.”

## LM35 Two-Point Calibration (Practical)

1. Point A: ambient (measure with a reference thermometer).
2. Point B: warm point (e.g., near 40–50 °C using warm water in a sealed bag, or a controlled heat source).
3. Record:
   - `T_A`, `Vout_A`
   - `T_B`, `Vout_B`

Fit line:

- `Vout = m*T + b`
- `m = (Vout_B - Vout_A)/(T_B - T_A)`
- `b = Vout_A - m*T_A`

Then temperature estimate:

- `T_est = (Vout - b)/m`

## LDR Calibration

LDR response is typically non-linear and part-dependent.

- For internship documentation, plot Vout vs lux (or “relative light level”) and use a lookup table or log fit.
- Focus on repeatability and process, not absolute precision unless you have a calibrated lux meter.
