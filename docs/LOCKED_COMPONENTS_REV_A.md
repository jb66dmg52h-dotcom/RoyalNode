# 2Watt Project Locked Components, Rev A

## Core ICs and modules

| Function | Locked part | Notes |
|---|---|---|
| MCU module | Seeed Studio XIAO nRF52840, standard | Socketed |
| Radio module | EBYTE E22-900M33S | Factory-placed if available |
| Charger/power path | TI BQ25798RQMR | 29-pin VQFN-HR |
| 5 V boost | TI TPS61088RHLR | 20-pin VQFN |
| Fuel gauge | ADI MAX17048G+T10 | 1S fuel gauge |
| XIAO reverse-current blocker | TI LM66100DCKR | 1.5 V to 5.5 V, 1.5 A ideal diode |

## Magnetics

| Function | Locked part | Key ratings |
|---|---|---|
| TPS61088 inductor | Coilcraft XAL7030-222MEC | 2.2 uH, 15.1 mOhm max DCR, 18 A saturation, 12.9 A Irms at 40 C rise |
| BQ25798 inductor | Coilcraft XAL7070-222MEC | 2.2 uH, high-current shielded molded inductor |

The XAL7030 part has ample margin over the calculated TPS61088 peak inductor current. The XAL7070 footprint is retained for the charger because of its larger thermal mass and current margin.

## Solar input protection

| Function | Locked part | Notes |
|---|---|---|
| Solar fuse | Littelfuse 0483002.DR | 2 A, 75 V, 1206 fast-acting SMD |
| Solar TVS | Littelfuse SMBJ22A | 22 V standoff, unidirectional, 600 W, DO-214AA |
| Solar reverse-polarity FET | Infineon BSL303SPE | P-channel, -30 V, 52 mOhm max at 4.5 V, TSOP-6 |

## Connectors

| Function | Locked part/class | Notes |
|---|---|---|
| Solar input | AMASS XT30PW board-mount | Gender/orientation opposite battery |
| Battery input | AMASS XT30PW board-mount | Keyed, no electronic reverse-polarity stage |
| XIAO power receptacle | JST B2B-PH-SM4-TB(LF)(SN) | 2-pin, 2.0 mm, board-mounted SMT |
| XIAO cable housing | JST PHR-2 | Two-wire removable lead |
| RF output | Molex 0732512440 | Board-edge SMA female candidate; verify launch against stack-up |

## BQ25798 locked startup values

- Cell configuration: 1S
- PROG resistor: 4.7 kOhm, 1%, to set the 1S default profile
- /CE: tied low so autonomous charging is enabled
- TS bias: 10 kOhm from REGN to TS and 10 kOhm from TS to GND, placing TS at 50% of REGN
- Switching frequency: 750 kHz
- Inductor: 2.2 uH
- Default firmware charge current after boot: 2.0 A maximum
- Safe autonomous default charge current remains the IC default until firmware writes the higher limit
- D+ and D- on BQ25798: not used; leave unconnected

## TPS61088 locked starting values

- Output: approximately 5.0 V
- Feedback divider: 178 kOhm top, 56 kOhm bottom, 1%
- Frequency resistor: 300 kOhm, 1%, approximately 500 kHz starting point
- Current-limit resistor: 140 kOhm, 1%
- Soft-start capacitor: 10 nF
- Inductor: 2.2 uH, XAL7030-222MEC
- MODE: include a configuration footprint so PFM and forced-PWM can be compared during RF testing
- EN: pulled high for automatic startup when the battery/system rail is present

## Capacitor targets

### TPS61088 input

- 2 x 22 uF, 10 V, X7R, 1206
- 100 uF low-ESR bulk
- 100 nF local bypass
- 4.7 uF VCC bypass

### TPS61088 output

- 3 x 22 uF, 10 V, X7R, 1206 near converter
- 2 x 22 uF, 10 V, X7R near E22
- 1 uF plus multiple 100 nF near E22
- 330-470 uF low-ESR bulk near E22

### BQ25798

- VBUS: 2 x 10 uF, 35 V, X7R plus 100 nF
- PMID: 2 x 10 uF, 35 V, X7R
- SYS: 4 x 22 uF, 10 V, X7R plus 100 uF bulk footprint
- BAT: 2 x 22 uF, 10 V, X7R
- REGN and SDRV bypass values: follow the latest TI reference schematic exactly

Final capacitor manufacturer numbers may be substituted by the assembler only when voltage rating, dielectric, package and effective capacitance after DC-bias derating are equal or better.

## Parts intentionally not fitted

- Power button controller
- eFuse
- Radio load switch
- Battery thermistor connector
- SWD connector
- Extra LEDs beyond charge LED
