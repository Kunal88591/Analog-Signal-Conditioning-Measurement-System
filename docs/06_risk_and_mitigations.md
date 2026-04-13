# Risks and Mitigations

## Electrical Risks

- Reverse polarity: can destroy sensor/op-amp.
  - Mitigation: keyed connector, series diode or ideal diode, pre-power check.

- Overvoltage on inputs (wrong wiring, external sensor): can damage op-amp.
  - Mitigation: series resistor + clamp diodes to rails.

- Grounding noise on breadboard:
  - Mitigation: star ground, keep high-current loads off the analog ground rail, short wires.

## Measurement Risks

- Scope probe ground clip can create ground loops.
  - Mitigation: keep the ground clip short, probe at the same ground node.

- Function generator output impedance (usually 50 Ω) impacts amplitude.
  - Mitigation: measure Vin at the circuit input (not at the generator front panel).

## Performance Risks

- Op-amp saturation due to limited output swing.
  - Mitigation: design headroom, reduce gain, or use rail-to-rail op-amp.

- Sallen-Key stability / peaking if components or gain are off.
  - Mitigation: verify step response; consider reducing Q or using a different filter topology.
