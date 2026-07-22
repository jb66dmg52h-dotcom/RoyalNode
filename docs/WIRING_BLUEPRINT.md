# 2Watt Project Wiring Blueprint, Rev A

## Core modules

- Seeed Studio XIAO nRF52840, standard version
- EBYTE E22-900M33S radio module
- TI BQ25798RQMR charger/power path
- TI TPS61088RHLR 5 V boost converter
- TI LM66100DCKR ideal diode for XIAO power isolation
- Protected 1S 3.6/3.7 V Li-ion/LiPo pack, 10-20 Ah class
- Board-mounted XT30 for solar
- Board-mounted XT30 for battery
- Battery-mounted Semitec 103AT-2 NTC through a dedicated two-wire temperature connector
- Board-edge 50-ohm SMA female connector
- Socketed XIAO with a separate two-wire JST-PH power lead

Rev A intentionally has no dedicated fuel-gauge IC. Battery and charger telemetry come from the BQ25798.

## Final XIAO pin map

| XIAO pin | nRF52840 pin | Signal |
|---|---|---|
| D0 | P0.02 | E22 NRST |
| D1 | P0.03 | E22 DIO1 |
| D2 | P0.28 | E22 BUSY |
| D3 | P0.29 | E22 NSS |
| D4 | P0.04 | BQ25798 I2C SDA |
| D5 | P0.05 | BQ25798 I2C SCL |
| D6 | P1.11 | E22 RXEN |
| D7 | P1.12 | TPS61088 EN |
| D8 | P1.13 | SPI SCK |
| D9 | P1.14 | SPI MISO |
| D10 | P1.15 | SPI MOSI |

All 11 exposed XIAO GPIOs are allocated.

E22 TXEN is not assigned to the XIAO. E22 DIO2 connects directly to E22 TXEN and firmware enables the SX1262 DIO2 RF-switch function.

## XIAO power lead

Only two wires are soldered to the underside of the XIAO.

| JST pin | Carrier signal | XIAO pad |
|---:|---|---|
| 1 | XIAO_BAT_ISO | BAT positive |
| 2 | GND | GND |

Power path:

```text
Protected battery/system node
  -> LM66100DCKR ideal diode
  -> JST B2B-PH-SM4-TB(LF)(SN)
  -> PHR-2 cable housing
  -> short flexible two-wire harness
  -> XIAO BAT and GND underside pads
```

Rules:

- do not drive the XIAO 5V/VBUS pad from the carrier
- use flexible stranded wire
- keep the lead short
- add strain relief at the XIAO solder points
- mark polarity on both cable and PCB
- the XIAO and lead are removed together
- USB-C remains available for firmware and native USB power

## Power tree

```text
12 V nominal solar
  -> XT30
  -> Littelfuse 0483002.DR 2 A fuse
  -> LTC4365ITS8-1#TRMPBF protection controller
  -> Infineon ISA170170N04LMDSXTMA1 back-to-back protection MOSFET pair
  -> BQ25798 solar input selector MOSFET pair
  -> BQ25798 VBUS

XIAO USB-C VBUS
  -> BQ25798 USB input selector MOSFET pair
  -> BQ25798 VBUS

Protected 1S Li-ion/LiPo
  <-> XT30
  <-> BQ25798 BAT / SYS power path

BQ25798 SYS
  -> TPS61088
  -> regulated 5 V
  -> E22 VCC pins directly

Protected battery/system node
  -> LM66100
  -> 2-pin JST-PH
  -> XIAO BAT and GND
```

The solar and USB input-selector paths use separate back-to-back MOSFET pairs so neither source backfeeds the other.

## BQ25798 connections

- PROG: 4.7 kOhm, 1%, for 1S default configuration
- /CE: tied low for autonomous charging
- TS: Semitec 103AT-2 network using 5.23 kOhm from REGN to TS and 30.1 kOhm from TS to the NTC node; NTC to GND
- SDA/SCL: XIAO D4/D5 with 10 kOhm pull-ups to 3.3 V
- D+/D-: no connection
- INT: 10 kOhm pull-up to 3.3 V, not routed to XIAO; poll status/fault registers by I2C
- STAT: direct open-drain LED drive, 3.3 V -> LED -> RLED -> STAT
- BATP: 100 Ohm series resistor on a dedicated Kelvin route from battery positive
- ILIM_HIZ: tied to REGN
- REGN: 4.7 uF
- SDRV: 1 nF to GND
- BTST1/BTST2: 47 nF each

## Battery interface

- XT30 carries battery positive and negative
- separate small locking 2-pin connector carries battery NTC and GND
- battery-mounted NTC is required for charge-temperature protection
- no carrier battery reverse-polarity stage
- battery pack must include suitable internal protection
- battery target: protected 1S, 10-20 Ah class, at least 5 A continuous discharge and at least 2 A permitted charge current
- target charging policy: suspend below 0 C and at/above 45 C

## E22 power and control

- E22 VCC: regulated 5.0 V
- no eFuse and no separate radio load switch
- TPS61088 D7 enable provides full radio-rail power cycling
- E22 DIO2 drives TXEN directly through the SX1262 RF-switch function
- E22 RXEN is controlled by XIAO D6
- DIO3 remains the TCXO-control function inside the module
- place 330-470 uF low-ESR bulk plus ceramic decoupling beside E22 VCC

RF switch behavior:

| TXEN | RXEN | Mode |
|---:|---:|---|
| 1 | 0 | Transmit |
| 0 | 1 | Receive |
| 0 | 0 | RF path inactive |

## RF path

```text
E22 pin 21 ANT
  -> direct 50-ohm grounded coplanar waveguide
  -> board-edge SMA female
```

Rules:

- no 0-ohm series link
- no pi tuning network
- no external DC-block capacitor
- no RF test connector or jumper
- uninterrupted Layer-2 ground reference
- grounded-coplanar via fence, target no greater than 1.5 mm pitch where practical
- no switch-node copper or digital route beneath the RF path
- JLCPCB is the Rev A fabricator
- preferred stack-up: JLC04161H-3313, 4-layer, 1.6 mm
- final width/gap must be generated from JLCPCB's production impedance model before routing release

## Indicators and service

- one external charge/status LED only
- XIAO onboard RGB LED remains available to firmware
- no power button
- no carrier reset button
- no SWD connector
- firmware update and normal recovery use XIAO USB-C and onboard reset

## Automatic startup

- TPS61088 EN is held low by 100 kOhm during MCU startup
- XIAO D7 intentionally enables the TPS61088 after board initialization
- inserting the protected battery powers the XIAO automatically
- removing the battery is the master disconnect
