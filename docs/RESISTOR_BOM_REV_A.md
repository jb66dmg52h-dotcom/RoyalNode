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
- Candidate JLC part: Walsin WR06X4701FTL, JLC C163914, 4.7 kOhm, 1%, 0603

This confirms the existing RoyalNode 4.7 kOhm value. The 6.04 kOhm value shown in TI application drawings is for a different PROG configuration and must not replace the Rev A 1S/750 kHz setting.

### Battery TS network

TI support explicitly recommends the BQ25798 EVM values for a Semitec 103AT-2:

- RT1: 5.23 kOhm, 0.1% preferred
- RT2: 30.1 kOhm, 0.1% preferred

These EVM values supersede the rounded/non-standard values printed in some BQ25798 application drawings.

Candidate JLC parts:

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

Locked values remain:

- R3: 1.87 MOhm
- R2: 104 kOhm
- R1: 40.2 kOhm

These values produce the already documented approximately 7 V undervoltage and 25 V overvoltage thresholds with the LTC4365 0.5 V UV/OV comparator architecture.

Tolerance policy:

- R1/R2/R3: 0.1% preferred for production threshold consistency
- use matched low-TCR thin-film parts where available

Verified JLC candidates:

- R2 104 kOhm: Vishay TNPW0603104KBEEA, 0.1%, 25 ppm/C, 0603, JLC C1693693
- R1 40.2 kOhm: Yageo AT0603BRD0740K2L, 0.1%, 25 ppm/C, 0603, JLC C855848

R3 1.87 MOhm currently has a verified JLC 1% candidate (Vishay CRCW06031M87FKTA, C4212657). Before release, either a 0.1% stocked/pre-orderable part must be selected or the threshold tolerance analysis must explicitly accept 1% for R3. Do not silently substitute it.

## TPS61088

### Feedback divider

- RFB_TOP: 176 kOhm, 0.1%, 0603
- RFB_BOTTOM: 56.0 kOhm, 0.1%, 0603

Verified JLC candidates:

- 176 kOhm: KOA RN731JTTD1763B50, 0.1%, 0603, JLC C4291479
- 56.0 kOhm: Yageo RP0603BRD0756KL, 0.1%, 25 ppm/C, 0603, JLC C6196204

The divider produces approximately 4.99 V nominal with the TPS61088 1.204 V feedback reference.

### Current limit

- RILIM: 100 kOhm, 1%, 0603
- TPS61088 Rev. D Equation 6 gives approximately 11.9 A typical peak-current limit for 100 kOhm.
- Candidate: TA-I RM06FTN1003, 1%, 0603, JLC C177186

### Frequency-setting resistor

- RFREQ: 330 kOhm, 1%, 0603
- Connection: FSW to SW, not FSW to ground

Exact JLC manufacturer part still to be frozen, but the electrical value/topology is locked.

### Compensation

- RCOMP: 20.0 kOhm, 1%, 0603
- Candidate: Vishay CRCW060320K0FKEA, 1%, 0603, JLC C844923
- CCOMP remains 4.7 nF and is handled in the capacitor BOM

### EN default state

- TPS61088 EN pulldown: 100 kOhm, 1%, 0603
- may share the same 100 kOhm production part as RILIM/pull-ups where voltage/power rating is suitable

## Generic logic resistors

For non-threshold logic functions, 1% 0603 thick-film parts are sufficient unless a specific IC datasheet requires tighter tolerance.

Examples include:

- 10 kOhm I2C/INT pull-ups
- 100 kOhm TPS61088 EN pulldown
- any E22 control pull-downs retained by the final module schematic

## Open resistor items before BOM freeze

1. Freeze an exact 0.1% 1.87 MOhm part for the LTC4365 divider, or formally accept the verified 1% part after worst-case threshold analysis.
2. Freeze exact 330 kOhm RFREQ JLC part.
3. Freeze exact LED series resistor after the LED part is selected.
4. Re-run repository-wide resistor-value contradiction search after these are locked.
