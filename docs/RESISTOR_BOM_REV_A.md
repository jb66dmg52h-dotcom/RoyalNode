# RoyalNode Rev A Resistor BOM

## Status

This document captures resistor values that have been re-verified against current manufacturer datasheets/reference designs before KiCad capture. Generic pull-ups/pull-downs use standard 1% 0603 parts; threshold and feedback networks use tighter tolerance where noted.

## BQ25798

### PROG

- Function: set POR battery cell count and switching frequency
- Value: 4.70 kOhm
- Tolerance: 1%
- Package: 0603
- Verified behavior: BQ25798 Rev. C Table 7-1 specifies 4.7 kOhm for 1S / 750 kHz.
- Production part: Walsin WR06X4701FTL, JLC C163914

This confirms the existing RoyalNode 4.7 kOhm value. The 6.04 kOhm value shown in some TI application drawings is for a different PROG configuration and must not replace the Rev A 1S/750 kHz setting.

### Battery TS network

TI support explicitly recommends the BQ25798 EVM values for a Semitec 103AT-2:

- RT1: 5.23 kOhm, 0.1%
- RT2: 30.1 kOhm, 0.1%

Production parts:

- RT1: KOA RN73H1JTTD5231B25, 5.23 kOhm, 0.1%, 25 ppm/C, 0603, JLC C4047317
- RT2: Stackpole RNCF0603BKE30K1, 30.1 kOhm, 0.1%, 25 ppm/C, 0603, JLC C4314708

### I2C and control pull-ups

Use one common production part:

- Yageo RC0603FR-0710KL
- 10 kOhm, 1%, 0603
- JLC C98220

Population:

- SDA pull-up: 10 kOhm
- SCL pull-up: 10 kOhm
- INT pull-up: 10 kOhm; INT is not routed to the XIAO

Only one SDA/SCL pull-up pair is fitted on the carrier.

### BATP Kelvin resistor

- 100 Ohm, 1%, 0603
- Production part: Walsin MR06X1000FTL, JLC C327825
- routed in series only with the dedicated BATP Kelvin sense trace

## LTC4365 solar threshold divider

Locked values:

- R3: 1.78 MOhm
- R2: 180 kOhm
- R1: 40.2 kOhm

Production parts:

- R3: TBD stocked 1.78 MOhm, 1%, 0603
- R2: TBD stocked 180 kOhm, 0.1% preferred, 0603
- R1: TBD stocked 40.2 kOhm, 0.1% preferred, 0603

The 1.78 MOhm / 180 kOhm / 40.2 kOhm chain is the 6 V-panel candidate, targeting roughly 4.54 V UV cutoff and roughly 24.9 V OV cutoff before threshold tolerance and hysteresis. Normal deployed panel cold-weather Voc must remain below the BQ25798 recommended operating limit; the approximately 25 V LTC4365 threshold is a protection ceiling, not a normal operating target.

## TPS61088

### Feedback divider

- RFB_TOP: 176 kOhm, 0.1%, 0603
- RFB_BOTTOM: 56.0 kOhm, 0.1%, 0603

Production parts:

- 176 kOhm: KOA RN731JTTD1763B50, JLC C4291479
- 56.0 kOhm: Yageo RP0603BRD0756KL, JLC C6196204

The divider produces approximately 4.99 V nominal with the TPS61088 1.204 V feedback reference.

### Current limit

- RILIM: 100 kOhm, 1%, 0603
- TPS61088 Rev. D Equation 6 gives approximately 11.9 A typical peak-current limit for 100 kOhm.
- Production part: Yageo RC0603FR-07100KL, JLC C14675

### Frequency-setting resistor

- RFREQ: 330 kOhm, 1%, 0603
- Connection: FSW to SW, not FSW to ground
- Production part: Viking Tech ARG03FTC3303, 25 ppm/C, JLC C217968

### Compensation

- RCOMP: 20.0 kOhm, 1%, 0603
- Production part: Vishay CRCW060320K0FKEA, JLC C844923
- CCOMP remains 4.7 nF and is handled in the capacitor BOM

### EN default state

- TPS61088 EN pulldown: 100 kOhm, 1%, 0603
- Production part: Yageo RC0603FR-07100KL, JLC C14675

## Charge/status LED

### LED

- Everlight 19-217/R6C-AL1M2VY/3T
- red, 0603
- nominal forward voltage approximately 1.95 V
- rated forward current 5 mA
- operating temperature -40 C to +85 C
- JLC C72044

### Series resistor

- 2.2 kOhm, 1%, 0603
- Production part: Walsin WR06X2201FTL, JLC C163872

Topology:

```text
3V3 -> LED -> 2.2 kOhm -> BQ25798 STAT
```

At approximately 3.3 V supply and about 1.95 V LED forward voltage, nominal LED current is roughly 0.6 mA. This is intentionally far below the LED's 5 mA rating and the BQ25798 STAT sink capability.

## Generic logic resistors

- 10 kOhm: Yageo RC0603FR-0710KL, JLC C98220
- 100 kOhm: Yageo RC0603FR-07100KL, JLC C14675
- 100 Ohm: Walsin MR06X1000FTL, JLC C327825
- 2.2 kOhm: Walsin WR06X2201FTL, JLC C163872

All are 0603 and 1% unless otherwise stated.

## Resistor BOM status

The resistor selection is closed for schematic capture. Any substitution must maintain resistance, tolerance, voltage rating, power rating and temperature range appropriate to the original location.

The remaining pin-level audit will determine whether the E22 module needs any additional explicit external logic pull-downs beyond the current control scheme; if so, use the common 10 kOhm 1% part unless the EBYTE datasheet requires another value.
