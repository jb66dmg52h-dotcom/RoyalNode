# 2Watt Project Locked Components, Rev A

## Core ICs and modules

| Function | Locked part | Notes |
|---|---|---|
| MCU module | Seeed Studio XIAO nRF52840, standard | Socketed |
| Radio module | EBYTE E22-900M33S | High-power 915 MHz module |
| Charger/power path | TI BQ25798RQMR | 29-pin VQFN-HR |
| 5 V boost | TI TPS61088RHLR | 20-pin VQFN |
| Fuel gauge | ADI MAX17048G+T10 | 1S fuel gauge |
| XIAO reverse-current blocker | TI LM66100DCKR | 1.5 V to 5.5 V, 1.5 A ideal diode |

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
| Battery NTC connector | Small locking 2-pin connector, exact family pending | Temperature sense only |
| RF output | Board-edge SMA female | Exact part to be mechanically verified against stack-up/launch |

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

## BQ25798 locked supporting values

- VBUS: 2 x 10 uF plus 100 nF
- PMID: 3 x 10 uF plus 100 nF
- SYS: 5 x 10 uF plus 100 nF
- BAT: 2 x 10 uF
- REGN: 4.7 uF
- BTST1: 47 nF
- BTST2: 47 nF
- SDRV: 1 nF to GND
- BATP: 100 Ohm series resistor on dedicated Kelvin trace
- ILIM_HIZ: tied to REGN
- INT: 10 kOhm pullup to 3.3 V and routed to XIAO GPIO

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

## Capacitor targets

### TPS61088 input

- 2 x 22 uF, 10 V ceramic
- 100 nF local VIN bypass

### TPS61088 output

- 2 x 47 uF, 10 V ceramic, 1210 target near converter
- exact capacitor manufacturer number must be checked for effective capacitance at 5 V DC bias
- E22 local decoupling: 2 x 22 uF, 1 uF, multiple 100 nF, plus 330-470 uF low-ESR bulk

### BQ25798

- VBUS: 2 x 10 uF plus 100 nF
- PMID: 3 x 10 uF plus 100 nF
- SYS: 5 x 10 uF plus 100 nF
- BAT: 2 x 10 uF
- REGN: 4.7 uF

Final capacitor manufacturer numbers may be substituted only when voltage rating, dielectric, package and effective capacitance after DC-bias derating are equal or better.

## Parts intentionally not fitted

- Power button controller
- eFuse
- Radio load switch
- SWD connector
- Extra LEDs beyond charge LED
- TS bypass or simulated-temperature network
- PFM/PWM mode-selection jumper
- Bench-test-only features
