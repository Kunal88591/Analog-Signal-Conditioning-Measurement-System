# Requirements and Assumptions

## Scope

Analog signal conditioning chain for a slow sensor (temperature via LM35 or light via LDR divider), built on a breadboard, powered from a single 5 V supply, using a dual op-amp.

## Functional Requirements

- Accept one of the following sensor inputs:
  - LM35 temperature sensor output (10 mV/°C)
  - LDR + fixed resistor divider (voltage proportional to light)
- Provide an op-amp signal conditioning / amplification stage.
- Provide an active low-pass filter stage.
- Provide an output node suitable for measurement on a DMM/scope or feeding a microcontroller ADC (high impedance input).

## Performance Targets (Breadboard Realistic)

- Supply: 5.0 V (USB power bank or regulated supply)
- Passband: DC to ~5 Hz (temperature/slow light changes)
- Low-pass cutoff: ~10 Hz (nominal)
- Noise reduction target: > 10 dB attenuation at 25–50 Hz relative to passband (depends on layout and interference)
- Output range: keep typical operation within ~0.2 V to ~4.0 V to avoid rail-swing limits of non-rail-to-rail op-amps.

## Assumptions

- The measurement instrument has high input impedance (≥ 1 MΩ).
- The sensor signal bandwidth is low (no need for fast response).
- Component tolerances are typical hobby parts unless specified:
  - Resistors: ±1% to ±5%
  - Capacitors: ±10% to ±20% (electrolytics can be worse)

## Non-Goals

- Precision metrology across full temperature range.
- Operation with negative input voltages or dual supplies.
- EMI compliance testing (only basic best-practice mitigations).
