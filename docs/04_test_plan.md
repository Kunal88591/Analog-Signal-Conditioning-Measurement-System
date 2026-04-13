# Lab Test Plan

This is a structured, repeatable plan you can run and document (internship-style).

## Equipment

- Breadboard build of the circuit
- Regulated 5 V supply (or USB + known-good regulator)
- Multimeter
- Oscilloscope (2 channels preferred)
- Function generator (sine + square)
- Optional: USB sound card / DAQ / microcontroller ADC for logging

## Test 1: Power-Up and Sanity

1. Verify 5 V rail and GND continuity.
2. Check LM358 pinout orientation.
3. With sensor disconnected, confirm no oscillation:
   - Probe op-amp outputs (pin 1 and pin 7) for unexpected high-frequency oscillations.
4. Confirm quiescent current is reasonable (no overheating).

## Test 2: DC Gain Verification

Goal: verify amplifier gain and overall scaling.

1. Feed a DC voltage into the amplifier input (use a divider/pot or a calibrated source).
2. Measure `V_AMP` and `V_OUT`.
3. Compute:
   - `Av1_meas = V_AMP / V_IN`
   - `Av_total_meas = V_OUT / V_IN` (at DC)
4. Record results and compare against expected.

## Test 3: Cutoff Frequency (fc) Verification

Goal: measure the -3 dB cutoff.

1. Disconnect the sensor.
2. Inject a sine wave at small amplitude (e.g., 100 mVpp) into the filter input.
3. Sweep frequency logarithmically from 0.5 Hz to 100 Hz.
4. Measure amplitude ratio `|Vout/Vin|`.
5. Identify `fc` where magnitude drops to 0.707× the low-frequency gain.

Tip: you can store results as a CSV and use the sweep analysis script.

## Test 4: Noise Reduction

Goal: quantify noise suppression.

Time-domain method (scope):

1. Keep the sensor in a steady condition.
2. Measure ripple/noise (RMS or peak-to-peak) at `V_SENSOR` and `V_OUT`.
3. Compute reduction:

- `NR_dB = 20 log10(Vnoise_in / Vnoise_out)`

Frequency-domain method (recommended):

1. Capture a time trace from `V_AMP` and `V_OUT`.
2. Compute FFT and compare energy above cutoff (e.g., 15–50 Hz).

## Test 5: Step Response

Goal: show the filter behavior and stability.

1. Apply a small square-wave step at the filter input.
2. Observe overshoot/ringing at the output.
3. Document if the response is underdamped (too much peaking) and adjust if needed.

## Deliverables

- Photos of breadboard
- Measured gains
- Measured fc and Bode plot
- Noise reduction metric(s)
- Notes on anomalies and fixes
