# 2Watt Project Locked Components, Rev A

## Core ICs and modules

| Function | Locked part | Notes |
|---|---|---|
| MCU module | Seeed Studio XIAO nRF52840, standard | Socketed |
| Radio module | EBYTE E22-900M33S | High-power 915 MHz module |
| Charger/power path | TI BQ25798RQMR | 29-pin VQFN-HR |
| 5 V boost | TI TPS61088RHLR | 20-pin VQFN |
| XIAO reverse-current blocker | TI LM66100DCKR | 1.5 V to 5.5 V, 1.5 A ideal diode |

Rev A intentionally has no dedicated fuel-gauge IC. Battery voltage and charger-state telemetry come from the BQ25798 over I2C.

## Magnetics

| Function | Locked part | Key ratings |
|---|---|---|
| TPS61088 inductor | Coilcraft XAL7030-222MEC | 2.2 uH, 15.1 mOhm max DCR, 18 A saturation, 12.9 A Irms at 40 C rise |
| BQ25798 inductor | Coilcraft XAL7070-222MEC | 2.2 uH, high-current shielded molded inductor |

## Battery temperature sensing

| Function | Locked part/value | Notes |
|---|---|---|
| Battery NTC | Semitec 103AT-2 | 10 kOhm at 25 C, mounted to battery pack |
| TS upper resistor | 5.23 kOhm | REGN to TS |
| TS lower resistor | 30.1 kOhm | TS to NTC node |

The NTC is mandatory for the production assembly. There is no fixed TS bypass, simulated-temperature divider, or bench-test selection network.

## Connectors

| Function | Locked part/class | Notes |
|---|---|---|
| Solar input | AMASS XT30PW board-mount | Final gender/orientation per mechanical design |
| Battery input | AMASS XT30PW board-mount | Keyed, no carrier battery reverse-polarity stage |
| XIAO power receptacle | JST B2B-PH-SM4-TB(LF)(SN) | 2-pin, 2.0 mm, board-mounted SMT |
| XIAO cable housing | JST PHR-2 | Two-wire removable lead |
| Battery NTC PCB header | Molex 5037630291 | Pico-Lock 1.00 mm, 2-circuit, right-angle SMT, positive lock, -40 to +105 C; JLCPCB C586113 |
| Battery NTC cable housing | Molex 5037640201 | Pico-Lock 1.00 mm, 2-circuit positive-lock receptacle, -40 to +105 C |
| Battery NTC crimp terminal | Molex 5037650098 | Pico-Lock female crimp terminal, gold mating surface, 30-28 AWG |
| RF output | Molex 0732511150 / 732511150 | Standard-polarity 50-ohm SMA female edge mount for 1.60 mm PCB; JLCPCB C841205 |

The Pico-Lock header is a current JLCPCB assembly-library part. Because JLCPCB inventory is dynamic, production BOM review must verify stock/pre-order status immediately before ordering.

## BQ25798 locked startup values

- Cell configuration: 1S
- Battery class: protected 3.6/3.7 V nominal Li-ion/LiPo, 4.20 V maximum
- PROG resistor: 4.7 kOhm, 1%
- /CE: tied low
- Switching frequency: 750 kHz
- Inductor: 2.2 uH, XAL7070-222MEC
- Maximum firmware charge current: 2.0 A
- D+ and D-: not used; leave unconnected
- TS network: Semitec 103AT-2 with 5.23 kOhm / 30.1 kOhm network
- Charge temperature policy target: suspend below 0 C and at/above 45 C
- Watchdog disabled by firmware
- ADC enabled by firmware
- MPPT enabled/restored by firmware for solar operation

## BQ25798 capacitor BOM

### Main 10 uF power capacitors

Use one common production part for VBUS, PMID, SYS and BAT:

- TDK C3225X7R1H106KT000E
- 10 uF, 50 V, X7R, +/-10%, 1210
- JLCPCB C432929

Population:

- VBUS: 2 x 10 uF
- PMID: 3 x 10 uF
- SYS: 5 x 10 uF
- BAT: 2 x 10 uF

DC-bias audit:

- TI requires at least 2 uF effective VBUS capacitance, 4 uF effective PMID capacitance, 6 uF effective SYS capacitance and 3 uF effective BAT capacitance.
- TDK's characterization graph for C3225X7R1H106K250AC, the same 10 uF / 50 V / X7R / 1210 electrical construction family, shows roughly 45% nominal capacitance remaining at about 25 V DC bias and very small loss at 4.2 V.
- Even using a conservative ~4.5 uF per capacitor at 25 V before tolerance, the VBUS pair provides about 9 uF and the PMID trio about 13.5 uF, both comfortably above TI minimum effective-capacitance requirements.
- At the 1S battery/SYS voltage region, five SYS capacitors and two BAT capacitors retain very large margin over TI's 6 uF and 3 uF minimums.
- The 50 V rating also provides comfortable voltage-rating margin above the approximately 25 V solar overvoltage threshold.

### High-frequency 100 nF bypass capacitors

Use:

- TDK CGA2B3X7R1H104K050BD
- 100 nF, 50 V, X7R, +/-10%, 0402
- JLCPCB C2167088

Population:

- VBUS: 1 x 100 nF, closest capacitor to VBUS/GND
- PMID: 1 x 100 nF, closest capacitor to PMID/GND
- SYS: 1 x 100 nF, closest capacitor to SYS/GND

The 50 V rating is deliberately common across these locations so the same bypass part can be used on the high-voltage input nodes and the low-voltage SYS node.

### REGN capacitor

Use:

- TDK C3216X7R1E475K160AC
- 4.7 uF, 25 V, X7R, +/-10%, 1206
- production-status part

Population:

- REGN: 1 x 4.7 uF to power ground, placed immediately beside the IC

The 25 V rating is substantially above the REGN operating voltage and provides better DC-bias margin than a minimally rated 10 V part.

### Bootstrap capacitors

Use:

- TDK C1005X7R1H473M050BB
- 47 nF, 50 V, X7R, +/-20%, 0402
- JLCPCB C3846080

Population:

- BTST1-SW1: 1 x 47 nF
- BTST2-SW2: 1 x 47 nF

TI requires 10 V or higher bootstrap-capacitor rating; 50 V is intentionally conservative and the small capacitance has negligible DC-bias concern in this package/rating.

### SDRV capacitor

Use:

- TDK C1005C0G1H102J050BA
- 1 nF, 50 V, C0G, +/-5%, 0402
- JLCPCB C2182279

Population:

- SDRV-GND: 1 x 1 nF

C0G is used because the 1 nF value should remain essentially invariant with DC bias and temperature.

## BQ25798 locked supporting values

- BATP: 100 Ohm series resistor on dedicated Kelvin trace
- ILIM_HIZ: tied to REGN
- INT: 10 kOhm pullup to 3.3 V, not routed to XIAO; firmware polls over I2C

## TPS61088 production-locked values

- Output: 5.0 V nominal
- Continuous design target: 2 A
- Inductor: Coilcraft XAL7030-222MEC, 2.2 uH
- Feedback divider: 176 kOhm top / 56.0 kOhm bottom, 0.1%
- Frequency resistor: 330 kOhm from FSW to SW
- Current-limit resistor: 100 kOhm to AGND
- Compensation: 20.0 kOhm and 4.7 nF
- Soft-start: 47 nF
- VCC bypass: 2.2 uF
- BOOT capacitor: 100 nF from BOOT to SW
- MODE: floating for PFM/light-load efficiency
- EN: XIAO-controlled, with 100 kOhm pulldown
- No mode jumper, test selector, or other bench-only configuration feature

## TPS61088 and E22 capacitor BOM

### Common 22 uF power capacitor

Use:

- Murata GRM31CZ71C226ME15L
- 22 uF, 16 V, X7R, +/-20%, 1206
- JLCPCB C909845

Population:

- TPS61088 VIN: 2 x 22 uF
- E22 local 5 V rail: 2 x 22 uF

The 16 V rating is intentionally above the 4.2 V battery input and 5 V E22 rail to reduce DC-bias loss compared with a 10 V-rated 22 uF part. JLCPCB currently lists substantial stock for this part.

### TPS61088 output capacitors

Use:

- TDK C3225X5R1A476MT000E
- 47 uF, 10 V, X5R, +/-20%, 1210
- JLCPCB C76680

Population:

- TPS61088 VOUT: 2 x 47 uF

Rationale:

- TI recommends low-ESR ceramic output capacitance and explicitly warns that effective capacitance under DC bias must be considered.
- A TI engineer reviewed a near-identical 2.5-4.2 V to 5 V / 2 A TPS61088 application using 2 x 47 uF, 1210, 10 V ceramic output capacitors and accepted that output-capacitor class while recommending the 20 kOhm / 4.7 nF compensation network used by Rev A.
- C3225X5R1A476MT000E is a current JLCPCB assembly-library 47 uF / 10 V / X5R / 1210 part with current stock.
- Final production validation still measures 5 V transient droop under repeated E22 full-power transmit bursts; that is validation of the assembled power stage, not a placeholder BOM decision.

### TPS61088 VIN high-frequency bypass

Use the existing common BQ bypass part:

- TDK CGA2B3X7R1H104K050BD
- 100 nF, 50 V, X7R, 0402
- JLCPCB C2167088

Population:

- TPS61088 VIN: 1 x 100 nF immediately beside VIN/PGND

### E22 1 uF local bypass

Use:

- Murata GCM188R71C105KA64D
- 1 uF, 16 V, X7R, +/-10%, 0603
- JLCPCB C161212

Population:

- E22 5 V rail: 1 x 1 uF close to the module VCC pins

### E22 100 nF local bypass

Use:

- Murata GCJ188R71C104KA01D
- 100 nF, 16 V, X7R, +/-10%, 0603
- JLCPCB C710619

Population:

- E22 5 V rail: multiple 100 nF capacitors, one adjacent to each practical local VCC/ground entry region of the module footprint

### E22 bulk capacitor

The bulk capacitor remains intentionally not locked to an anonymous JLCPCB generic part. Rev A requires 330-470 uF, >=10 V, low-ESR, -40 C-or-better rated operation. A manufacturer-qualified part with explicit ESR/ripple/lifetime data must be selected before the BOM is declared complete.

This is the only remaining high-value capacitor selection in the radio power block.

## Parts intentionally not fitted

- MAX17048 or other dedicated fuel gauge
- Power button controller
- eFuse
- Radio load switch
- SWD connector
- Extra LEDs beyond charge LED
- TS bypass or simulated-temperature network
- PFM/PWM mode-selection jumper
- Bench-test-only features
