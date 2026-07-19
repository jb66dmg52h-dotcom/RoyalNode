# 2Watt Project Final Power Calculations, Rev A

## Scope

These calculations size the Rev A charger and 5 V radio supply around:

- protected 1S 10 Ah LiPo target
- 12 V nominal solar panel recommendation, approximately 10-20 W
- XIAO nRF52840
- E22-900M33S at up to 33 dBm
- USB-C charging through the XIAO USB-C connector

The board only is being designed. Enclosure and battery physical packaging are outside this calculation.

## Design load

### 5 V rail

- E22 maximum transmit current design value: 1.2 A
- XIAO and logic allowance: 0.15 A
- margin for LEDs, gauge and conversion transients: 0.15 A
- expected full-power operating load: approximately 1.5 A at 5 V
- continuous design rating: 2.0 A at 5 V = 10 W
- transient design rating: 3.0 A at 5 V = 15 W

The 3 A target is not expected continuous radio demand. It is headroom for startup, bulk-capacitor charging, tolerance and bench testing.

## Battery current requirement

Using conservative boost efficiency assumptions:

| Battery voltage | 5 V / 1.5 A at 88% | 5 V / 2 A at 85% | 5 V / 3 A at 85% |
|---:|---:|---:|---:|
| 4.2 V | 2.03 A | 2.80 A | 4.20 A |
| 3.7 V | 2.30 A | 3.18 A | 4.77 A |
| 3.2 V | 2.66 A | 3.68 A | 5.51 A |
| 3.0 V | 2.84 A | 3.92 A | 5.88 A |

Therefore:

- battery pack continuous discharge rating: at least 5 A
- preferred battery protection rating: 8 A or greater transient
- PCB battery path design: 6 A continuous minimum with margin
- full-power transmit should be reduced or disabled as the cell approaches 3.2 V under load

## BQ25798 charger design

### Charge-current target

For a 10 Ah pack:

- 1 A charge rate = 0.1 C
- 2 A charge rate = 0.2 C

Rev A target charge current: **2.0 A maximum**, configurable lower in firmware.

This is deliberately conservative and compatible with many protected 10 Ah packs, but the final pack datasheet must still permit at least 2 A charging.

### Charge time

Ignoring system load:

- 10 Ah / 2 A = 5 hours ideal
- practical full charge including CV taper and losses: approximately 6-7 hours of sufficient input power

At 1 A USB charge current, practical time is roughly 11-13 hours. At a 500 mA USB limit, practical time is roughly 22-26 hours.

### Switching frequency and inductor

Use the BQ25798 750 kHz option with a **2.2 uH shielded inductor**. TI specifies 2.2 uH for 750 kHz and 1 uH for 1.5 MHz. The lower-frequency option is selected for improved efficiency and lower switching loss.

Inductor requirements:

- value: 2.2 uH, tolerance ±20% or better
- saturation current: at least 8 A
- preferred saturation current: 10 A or higher
- heating current rating: at least 6 A
- DCR target: below 20 mOhm
- shielded construction

### BQ25798 capacitors

Initial schematic values:

- VBUS input: 2 x 10 uF, 35 V, X7R, 1210 plus 100 nF
- PMID: 2 x 10 uF, 35 V, X7R, 1210
- VSYS: 4 x 22 uF, 10 V, X7R, 1206 plus 100 uF low-ESR bulk footprint
- BAT: 2 x 22 uF, 10 V, X7R, 1206
- REGN and local bypass parts: exactly per the latest TI datasheet/EVM reference circuit

Capacitor values are nominal. Effective capacitance after DC-bias derating must be checked from the selected capacitor curves.

### Solar input power

A 20 W panel with Vmp near 17-18 V supplies roughly 1.1 A at maximum power. After charger losses, that is enough for approximately 2 A battery charging while also supporting normal repeater load, depending on radio duty cycle.

A 10 W panel can support the node but may not maintain a 2 A charge rate while the radio is active. Firmware input-current and charge-current limits must let the charger prioritize the system load.

### USB input

Rev A startup limit: 500 mA.

Firmware may raise the BQ25798 input-current limit after source detection. Practical board target:

- ordinary USB fallback: 500 mA
- preferred capable USB source: 1.5 A
- do not assume 3 A unless the XIAO connector, traces and detected source are verified for it

## TPS61088 5 V boost design

### Electrical target

- input range for calculation: 3.0-4.2 V
- output: 5.0 V
- continuous output: 2.0 A
- transient output: 3.0 A
- selected switching frequency: approximately 500 kHz
- operating mode: PFM for low idle current, with an option to force PWM during RF testing if needed

### Feedback divider

TPS61088 feedback reference is approximately 1.204 V. Using the TI-recommended 56 kOhm low-side resistor:

- Rbottom = 56.0 kOhm
- Rtop calculated for 5.0 V = approximately 176.6 kOhm
- selected standard value: **178 kOhm, 1%**

Expected nominal output is approximately 5.03 V, before tolerance.

### Switching-frequency resistor

TI support guidance identifies approximately 300 kOhm as a typical value for about 500 kHz operation.

- RFREQ initial value: **300 kOhm, 1%**
- retain an alternate footprint/value option after bench measurement

### Inductor calculation

Selected inductor: **2.2 uH shielded**.

Worst-case calculation assumptions:

- VIN = 3.0 V
- VOUT = 5.0 V
- IOUT = 3.0 A transient
- efficiency = 85%
- switching frequency = 500 kHz
- inductance at -30% tolerance = 1.54 uH

Results:

- average inductor/input current ≈ 5.88 A
- estimated ripple current ≈ 1.56 A peak-to-peak
- estimated peak inductor current ≈ 6.66 A

Inductor requirements:

- 2.2 uH
- saturation current at least 10 A
- preferred 12 A or higher
- heating current at least 8 A
- DCR preferably 15 mOhm or lower

A TI-listed example class is the PIMB065T-2R2MS range, but the exact supplier part remains a BOM decision.

### Current-limit resistor

For the non-Q1 TPS61088, the datasheet relationship is approximately:

- ILIM = 1,190,000 / RILIM

To guarantee margin above the calculated 6.66 A peak, including TI's stated possible 1.3 A minimum-limit reduction:

- target typical limit: about 8.5 A
- selected RILIM: **140 kOhm, 1%**
- typical current limit: approximately 8.5 A
- worst-case minimum estimate: approximately 7.2 A

This leaves about 0.5 A margin over the calculated transient peak. The value must be verified on the bench for thermal behavior and startup response.

### Soft-start

- CSS initial value: **10 nF**
- provide footprint flexibility for 4.7 nF to 22 nF during bring-up

### TPS61088 input capacitors

Near VIN and the inductor:

- 2 x 22 uF, 10 V, X7R, 1206
- 100 uF low-ESR polymer or electrolytic bulk
- 100 nF directly at VIN
- at least 1 uF at VCC, with 4.7 uF preferred if layout permits

### TPS61088 output capacitors

Near the converter:

- 3 x 22 uF, 10 V, X7R, 1206

Near the E22 supply pins:

- 2 x 22 uF, 10 V, X7R
- 1 uF ceramic
- multiple 100 nF ceramics
- 330-470 uF low-ESR bulk capacitor

This follows TI guidance that multiple ceramic capacitors plus 220-470 uF bulk can reduce pulse-load voltage drop.

### Radio branch

- retain a high-current load switch/eFuse between 5 V and E22
- current capability: at least 3 A continuous
- controlled rise time to avoid collapsing the 5 V rail
- true output disconnect preferred

## Power budget summary

| Item | Final Rev A target |
|---|---|
| Battery | Protected 1S, 10 Ah target |
| Battery discharge capability | ≥5 A continuous, ≥8 A transient preferred |
| Charger IC | BQ25798 |
| Max charge current | 2.0 A |
| Charger switching setup | 750 kHz, 2.2 uH |
| Charger inductor | ≥8 A saturation, 10 A preferred |
| 5 V converter | TPS61088 |
| 5 V output | 5.03 V nominal with 178 k / 56 k divider |
| Continuous 5 V rating | 2 A |
| Transient 5 V rating | 3 A |
| TPS61088 frequency | ~500 kHz with 300 kOhm initial RFREQ |
| TPS61088 inductor | 2.2 uH, ≥10 A saturation, 12 A preferred |
| TPS61088 current limit | ~8.5 A typical using 140 kOhm RILIM |
| Output bulk at E22 | 330-470 uF plus ceramics |

## Verification still required

These calculations are sufficient for schematic capture, but not a substitute for prototype measurements. Rev A bring-up must verify:

1. 5 V droop during repeated 33 dBm transmit bursts.
2. TPS61088 inductor and IC temperature at 3.0-3.2 V battery voltage.
3. Charger temperature at 2 A charge current from both solar and USB.
4. Effective capacitance after DC-bias derating.
5. USB input-current behavior through the XIAO connector.
6. Solar MPPT behavior with 10 W and 20 W panel classes.
7. Radio noise floor with PFM enabled versus forced PWM.
8. Battery-protection-board trip behavior during 3 A 5 V transient testing.

## Final conclusion

The 10 Ah target is compatible with the selected power architecture. A 2 A charge limit is conservative, a 20 W panel is the better deployment recommendation, and the TPS61088 power stage can support the E22 with comfortable margin when built around a 2.2 uH high-current inductor, substantial ceramic capacitance and 330-470 uF local bulk capacitance.
