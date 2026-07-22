# 2Watt Project Final Power Calculations, Rev A

## Scope

These calculations size the Rev A charger and 5 V radio supply around:

- protected 1S 3.6/3.7 V Li-ion/LiPo pack, 10-20 Ah class
- 12 V nominal solar panel, 10 W supported / 20 W recommended
- Seeed Studio XIAO nRF52840
- EBYTE E22-900M33S at up to approximately 33 dBm
- USB-C charging through the XIAO USB-C connector into the BQ25798 input-selector path

The board only is being designed. Enclosure and battery physical packaging are outside this calculation.

## Design load

### 5 V rail

- E22 full-power transmit design current allowance: approximately 1.2 A class
- radio rail nominal voltage: 5.0 V
- continuous converter design rating: 2.0 A at 5 V = 10 W
- XIAO is not powered from this 5 V rail; it is powered separately through LM66100 into the XIAO BAT pad
- E22 local energy storage: 330-470 uF low-ESR bulk plus ceramics

The 2 A rating provides margin above the expected E22 load without carrying forward the older 3 A bench-transient requirement as a production specification.

## Battery current requirement

Using a conservative 85% boost efficiency assumption at the full 10 W converter design point:

| Battery voltage | Approximate battery current for 5 V / 2 A |
|---:|---:|
| 4.2 V | 2.80 A |
| 3.7 V | 3.18 A |
| 3.2 V | 3.68 A |
| 3.0 V | 3.92 A |
| 2.7 V | 4.36 A |

Therefore:

- battery pack continuous discharge rating: at least 5 A
- preferred battery protection rating: 8 A or greater transient
- PCB battery/current path design target: at least 6 A continuous capability with margin
- firmware should reduce or disable full-power radio operation before a deeply discharged cell reaches its protection cutoff under load

## BQ25798 charger design

### Charge-current target

Rev A maximum programmed charge current: **2.0 A**, configurable lower in firmware.

Examples:

- 10 Ah pack at 2 A = 0.2 C
- 20 Ah pack at 2 A = 0.1 C

The selected battery pack must explicitly permit at least 2 A charging if the full configured rate is used.

### Charge voltage

- battery class: standard 1S 4.20 V-charge Li-ion/LiPo
- regulation target: 4.20 V

### Switching frequency and inductor

- BQ25798 switching option: 750 kHz
- inductor: Coilcraft XAL7070-222MEC, 2.2 uH

### BQ25798 capacitors

Current locked nominal values:

- VBUS: 2 x 10 uF plus 100 nF
- PMID: 3 x 10 uF plus 100 nF
- SYS: 5 x 10 uF plus 100 nF
- BAT: 2 x 10 uF
- REGN: 4.7 uF
- BTST1: 47 nF
- BTST2: 47 nF
- SDRV: 1 nF

Final capacitor manufacturer numbers must be checked for effective capacitance after DC-bias derating.

### Battery-temperature protection

- sensor: battery-mounted Semitec 103AT-2 10 kOhm NTC
- TS network: 5.23 kOhm REGN-to-TS and 30.1 kOhm TS-to-NTC node
- target policy: suspend charging below 0 C and at/above 45 C
- no simulated-temperature bypass network is fitted

### Solar input power

A representative 20 W, 12 V-class panel with Vmp around 17-18 V supplies roughly 1.1-1.2 A near maximum power. This is sufficient to support a 2 A battery-charge target under strong sun while also covering normal repeater load depending on radio duty cycle.

A 10 W panel can operate the node but provides less battery-recovery margin during radio activity and poor solar conditions.

### USB input policy

The BQ25798 D+/D- pins are not used. The XIAO owns USB enumeration and firmware controls the charger's input-current limit.

Locked policy:

- 100 mA BQ25798 USB input-current limit before enumeration
- 350 mA maximum after enumeration
- never intentionally exceed 350 mA through the shared XIAO USB-C input path

This replaces the older 500 mA / 1.5 A concept.

## TPS61088 5 V boost design

### Electrical target

- input operating design range: 2.7-4.2 V
- output: approximately 5.0 V nominal
- continuous output rating: 2.0 A
- mode: PFM/light-load operation with MODE floating
- no production PFM/PWM selection jumper

### Locked power-stage values

- U3: TPS61088RHLR
- inductor: Coilcraft XAL7030-222MEC, 2.2 uH
- feedback: 176 kOhm top / 56.0 kOhm bottom, 0.1%
- RFREQ: 330 kOhm from FSW to SW
- RILIM: 100 kOhm to AGND
- compensation: 20.0 kOhm and 4.7 nF
- soft-start: 47 nF
- VCC bypass: 2.2 uF
- BOOT: 100 nF from BOOT to SW
- EN: XIAO D7, with 100 kOhm pulldown

### TPS61088 input capacitors

Near VIN/inductor:

- 2 x 22 uF, 10 V ceramic
- 100 nF local VIN bypass

### TPS61088 output capacitors

Near converter:

- 2 x 47 uF, 10 V ceramic, 1210 target
- exact part must retain adequate effective capacitance at 5 V DC bias

Near E22:

- 2 x 22 uF, 10 V ceramic
- 1 uF ceramic
- multiple 100 nF ceramics
- 330-470 uF low-ESR bulk

### Radio branch

There is no separate load switch or eFuse between TPS61088 and E22. Radio power cycling is performed by disabling/enabling the TPS61088 through XIAO D7.

## Power budget summary

| Item | Final Rev A target |
|---|---|
| Battery | Protected 1S 3.6/3.7 V, 10-20 Ah class |
| Battery discharge capability | >=5 A continuous, >=8 A transient preferred |
| Charger IC | BQ25798RQMR |
| Max charge current | 2.0 A |
| Charge voltage | 4.20 V |
| Charger switching setup | 750 kHz, 2.2 uH |
| Charger inductor | Coilcraft XAL7070-222MEC |
| 5 V converter | TPS61088RHLR |
| 5 V output | approximately 5.0 V |
| Continuous 5 V rating | 2 A |
| TPS61088 inductor | Coilcraft XAL7030-222MEC, 2.2 uH |
| TPS61088 current limit resistor | 100 kOhm |
| TPS61088 RFREQ | 330 kOhm |
| Output bulk at E22 | 330-470 uF plus ceramics |
| Fuel gauge | None; BQ25798 telemetry only |

## Production validation still required

The schematic values are frozen enough for capture, but manufactured Rev A hardware still requires validation before being considered production-qualified:

1. 5 V droop during repeated full-power transmit bursts.
2. TPS61088 inductor and IC temperature at low battery voltage.
3. Charger temperature at the configured charge rate.
4. Effective capacitance after DC-bias derating.
5. USB input-current behavior through the XIAO USB-C connector.
6. Solar MPPT behavior with representative 10 W and 20 W panel classes.
7. RF noise floor with the production PFM configuration.
8. Battery-protection-board behavior under worst-case radio load.

## Final conclusion

The 10-20 Ah 1S battery class is compatible with the selected architecture. The 2 A charge ceiling is modest for this battery capacity range, the 20 W solar panel remains the preferred permanent-deployment option, and the TPS61088 stage is designed around a 10 W continuous 5 V rail with substantial local E22 decoupling.
