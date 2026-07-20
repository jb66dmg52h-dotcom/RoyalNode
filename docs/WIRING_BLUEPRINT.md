# 2Watt Project Wiring Blueprint, Rev A

## Core modules

- Seeed Studio XIAO nRF52840, standard version
- EBYTE E22-900M33S radio module
- TI BQ25798RQMR charger/power path
- TI TPS61088RHLR 5 V boost converter
- ADI MAX17048G+T10 fuel gauge
- TI LM66100DCKR ideal diode for XIAO power isolation
- Protected 1S flat LiPo, 10 Ah target
- Board-mounted XT30 for solar
- Board-mounted XT30 for battery
- Board-edge SMA female connector
- Socketed XIAO with a separate two-wire JST-PH power lead

## XIAO radio pin map

| XIAO pin | nRF52840 pin | Signal |
|---|---|---|
| D0 | P0.02 | E22 NRST |
| D1 | P0.03 | E22 DIO1 |
| D2 | P0.28 | E22 BUSY |
| D3 | P0.29 | E22 NSS |
| D4 | P0.04 | I2C SDA, shared by BQ25798 and MAX17048 |
| D5 | P0.05 | I2C SCL, shared by BQ25798 and MAX17048 |
| D6 | P1.11 | E22 TXEN |
| D7 | P1.12 | E22 RXEN |
| D8 | P1.13 | SPI SCK |
| D9 | P1.14 | SPI MISO |
| D10 | P1.15 | SPI MOSI |

All 11 exposed GPIOs are allocated.

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
  -> Infineon BSL303SPE reverse-polarity MOSFET
  -> Littelfuse SMBJ22A TVS
  -> BQ25798 solar input

XIAO USB-C VBUS
  -> protected current-limited path
  -> BQ25798 USB input

Protected 1S LiPo
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

## BQ25798 connections

- PROG: 4.7 kOhm, 1%, for 1S default configuration
- /CE: tied low for autonomous charging
- TS: 10 kOhm from REGN to TS and 10 kOhm from TS to GND
- SDA/SCL: XIAO D4/D5 with 3.3 V pull-ups
- D+/D- on BQ25798: no connection
- charge LED: driven from charger status output
- no charger interrupt GPIO; poll by I2C

## Battery interface

- XT30 carries battery positive and negative only
- no battery temperature signal
- no carrier reverse-polarity stage
- battery must include over-charge, over-discharge, over-current and short-circuit protection
- battery target: 1S, 10 Ah, at least 5 A continuous discharge and at least 2 A permitted charge current

## E22 power and control

- E22 VCC: regulated 5.0 V
- no eFuse and no separate radio load switch
- TXEN and RXEN each receive default-low pull-down resistors
- DIO3 remains the TCXO-control function inside the module
- place 330-470 uF low-ESR bulk plus ceramic decoupling beside E22 VCC

TXEN/RXEN truth table:

| TXEN | RXEN | Mode |
|---:|---:|---|
| 1 | 0 | Transmit |
| 0 | 1 | Receive |
| 0 | 0 | RF path closed |

## RF path

```text
E22 ANT
  -> optional tuning footprint / 0-ohm link
  -> short 50-ohm controlled-impedance trace
  -> board-edge SMA female
```

Rules:

- no u.FL connector
- uninterrupted ground reference
- via fence beside RF route
- no switch-node copper near E22, RF route or SMA
- calculate geometry from the selected 4-layer fabrication stack-up

## Indicators and service

- one external charge LED only
- XIAO onboard RGB LED remains available to firmware
- no power button
- no carrier reset button
- no SWD connector
- firmware update and normal recovery use XIAO USB-C and onboard reset

## Automatic startup

- TPS61088 EN is pulled high from the valid system rail
- inserting the protected battery powers the system automatically
- removing the battery is the master disconnect
