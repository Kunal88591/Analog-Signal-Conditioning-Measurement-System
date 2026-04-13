# Design Rationale (What reviewers expect)

## Architecture

- Stage 1: non-inverting amplifier to scale a low-level sensor voltage.
- Stage 2: 2nd-order active low-pass (Sallen-Key) to suppress high-frequency noise.

This matches typical conditioning used ahead of an ADC: gain + anti-noise / anti-alias behavior.

## Op-Amp Selection Notes

The current design targets LM358/LMV358-class dual op-amps because they are common and breadboard-friendly.

Key constraints to mention:

- Input common-mode range: LM358 inputs typically include ground but not the positive rail.
- Output swing: LM358 is not rail-to-rail; near the top rail it saturates early.
- GBW and phase margin: ensure the chosen Sallen-Key configuration is stable.

Industry upgrade path (same topology):

- Use a rail-to-rail input/output op-amp for better headroom at 5 V (for example MCP6002, TLV9002, OPA2333 depending on budget and needs).

## Input Protection and Robustness

Recommended minimal protection for internship-level hygiene:

- Series resistor (100 Ω to 1 kΩ) at the sensor output into the op-amp input.
- Clamp diodes to rails (or rely on op-amp input protection if datasheet allows) when connecting to unknown sources.
- Proper decoupling:
  - 100 nF at op-amp supply pins
  - optional 1–10 µF bulk capacitor on the breadboard rails

## Component Choice Notes

- For 10 Hz cutoff, large capacitors are required. Electrolytics work, but tolerance/leakage is high.
- If possible, use film capacitors (1 µF) or parallel smaller MLCCs.
- Use 1% resistors for repeatable gain and cutoff.

## Signal Range Planning

A design review question you should be able to answer:

- “What is the maximum expected output and do you clip?”

For a non-rail-to-rail op-amp at 5 V:

- Plan to keep `V_OUT` comfortably below the top rail (target < 4.0 V).
- If you need more range, reduce total gain or select a rail-to-rail output op-amp.
