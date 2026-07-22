# RoyalNode Rev A Resistor BOM

## Status

This document captures resistor values that have been re-verified against the current manufacturer datasheets/reference designs before KiCad capture. Generic pull-ups/pull-downs may use standard 1% 0603 parts; threshold and feedback networks use tighter tolerance where noted.

## BQ25798

### PROG

- Function: set POR battery cell count and switching frequency
- Value: 4.70 kOhm
- Tolerance: 1%
- Package target: 0603
- Verified behavior: current BQ25798 Rev. C Table 7-1 specifies 4.7 kOhm for 1S / 750 kHz.
- Production part: Walsin WR06X4701FTL, JLC C163914, 4.7 kOhm, 1%, 0603

This confirms the existing RoyalNode 4.7 kOhm value. The 6.04 kOhm value shown in TI application drawings is for a different PROG configuration and must not replace the Rev A 1S/750 kHz setting.

### Battery TS network

TI support explicitly recommends the BQ25798 EVM values for a Semitec 103AT-2:

- RT1: 5.23 kOhm, 0.1%
- RT2: 30.1 kOhm, 0.1%

These EVM values supersede the rounded/non-standard values printed in some BQ25798 application drawings.

Production parts:

- RT1: KOA RN73H1JTTD5231B25, 5.23 kOhm, 0.1%, 25 ppm/C, 0603, JLC C4047317
- RT2: Stackpole RNCF0603BKE30K1, 30.1 kOhm, 0.1%, 25 ppm/C, 0603, JLC C4314708

### I2C and control pull-ups

- SDA pull-up: 10 kOhm, 1%, 0603
- SCL pull-up: 10 kOhm, 1%, 0603
- INT pull-up: 10 kOhm, 1%, 0603; INT is not routed to the XIAO

Only one SDA/SCL pull-up pair is fitted on the carrier.

### BATP Kelvin resistor

- 100 Ohm, 1%, 0603
- routed in series only with the dedicated BATP Kelvin sense trace

## LTC4365 solar threshold divider

Locked values:

- R3: 1.87 MOhm
- R2: 104 kOhm
- R1: 40.2 kOhm

These values produce the already documented approximately 7 V undervoltage and 25 V overvoltage thresholds with the LTC4365 0.5 V UV/OV comparator architecture.

Production parts:

- R3: Vishay CRCW06031M87FKTA, 1.87 MOhm, 1%, 0603, JLC C4212657
- R2: Vishay TNPW0603104KBEEA, 104 kOhm, 0.1%, 25 ppm/C, 0603, JLC C1693693
- R1: Yageo AT0603BRD0740K2L, 40.2 kOhm, 0.1%, 25 ppm/C, 0603, JLC C855848

R3 at 1% is accepted for Rev A. The LTC4365 datasheet design procedure itself uses standard 1% divider values, and R3's 1% tolerance contributes under approximately 1% divider-ratio shift because R3 dominates the total resistance. The LTC4365 UV/OV comparator threshold itself is specified at 500 mV typical with 492.5-507.5 mV limits, so moving R3 to an exotic 0.1% part would not materially eliminate the dominant threshold uncertainty. Normal deployed panel cold-weather Voc must still remain below the BQ25798 recommended 24 V operating limit; the approximately 25 V LTC4365 threshold is a protection ceiling, not a normal operating target.

## TPS61088

### Feedback divider

- RFB_TOP: 176 kOhm, 0.1%, 0603
- RFB_BOTTOM: 56.0 kOhm, 0.1%, 0603

Production parts:

- 176 kOhm: KOA RN731JTTD1763B50, 0.1%, 0603, JLC C4291479
- 56.0 kOhm: Yageo RP0603BRD0756KL, 0.1%, 25 ppm/C, 0603, JLC C6196204

The divider produces approximately 4.99 V nominal with the TPS61088 1.204 V feedback reference.

### Current limit

- RILIM: 100 kOhm, 1%, 0603
- TPS61088 Rev. D Equation 6 gives approximately 11.9 A typical peak-current limit for 100 kOhm.
- Production part: TA-I RM06FTN1003, 1%, 0603, JLC C177186

### Frequency-setting resistor

- RFREQ: 330 kOhm, 1%, 0603
- Connection: FSW to SW, not FSW to ground
- Production part: Viking Tech ARG03FTC3303, 330 kOhm, 1%, 25 ppm/C, 0603, JLC C217968

### Compensation

- RCOMP: 20.0 kOhm, 1%, 0603
- Production part: Vishay CRCW060320K0FKEA, 1%, 0603, JLC C844923
- CCOMP remains 4.7 nF and is handled in the capacitor BOM

### EN default state

- TPS61088 EN pulldown: 100 kOhm, 1%, 0603
- use the same 100 kOhm production part as RILIM where appropriate

## Charge/status LED

### LED

- Everlight 19-217/R6C-AL1M2VY/3T
- red, 0603
- nominal forward voltage approximately 1.95 V
- rated 5 mA
- operating temperature -40 C to +85 C
- JLC C72044

### Series resistor

- 2.2 kOhm, 1%, 0603
- Production part: Walsin WR06X2201FTL, JLC C163872

Topology:

```text
3V3 -> LED -> 2.2 kOhm -> BQ25798 STAT
```

At approximately 3.3 V supply and about 1.95 V LED forward voltage, nominal LED current is roughly 0.6 mA. This is intentionally far below the LED's 5 mA rating and the BQ25798 STAT sink capability, reducing continuous charge-indicator power while remaining visible.

## Generic logic resistors

For non-threshold logic functions, 1% 0603 thick-film parts are sufficient unless a specific IC datasheet requires tighter tolerance.

Examples include:

- 10 kOhm I2C/INT pull-ups
- 100 kOhm TPS61088 EN pulldown
- E22 control pull-downs retained by the final module schematic

## Remaining resistor-related work

1. Freeze one standard 10 kOhm 1% 0603 JLC part for all compatible pull-ups/pull-downs.
2. Freeze one standard 100 Ohm 1% 0603 part for BATP.
3. Verify whether any remaining E22 control pins require explicit external pull-downs after the final module pin-level audit.
4. Re-run repository-wide resistor-value contradiction search after schematic net mapping is complete.
