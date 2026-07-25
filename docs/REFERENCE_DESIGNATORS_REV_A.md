# RoyalNode Rev A Reference Designators

## Status

This file defines the reference-designator scheme for KiCad schematic capture. It resolves earlier documentation drift where some preliminary tables reused `U1` for different assemblies.

Use this file for new KiCad work.

## Modules

| Ref | Part | Function |
|---|---|---|
| MOD1 | Seeed Studio XIAO nRF52840 | Socketed MCU module |
| MOD2 | EBYTE E22-900M33S | High-power LoRa radio module |

## ICs

| Ref | Part | Function |
|---|---|---|
| U1 | BQ25798RQMR | Solar/USB charger and power path |
| U2 | LM66100DCKR | XIAO reverse-current blocker |
| U3 | TPS61088RHLR | 1S-to-5 V radio boost converter |
| U4 | LTC4365ITS8-1#TRMPBF | Solar input UV/OV/reverse protection controller |

## MOSFETs

| Ref | Part | Function |
|---|---|---|
| Q1 | ISA170170N04LMDSXTMA1 | LTC4365-controlled solar protection back-to-back MOSFET pair |
| Q2 | ISA170170N04LMDSXTMA1 | BQ25798 solar input selector MOSFET pair |
| Q3 | ISA170170N04LMDSXTMA1 | BQ25798 USB input selector MOSFET pair |

## Connectors

| Ref | Part/class | Function |
|---|---|---|
| J1 | AMASS XT30PW-M | Solar input |
| J2 | AMASS XT30PW-M | Battery input |
| J3 | JST-GH SM02B-GHS-TB(LF)(SN) | XIAO battery harness output |
| J4 | JST-GH SM02B-GHS-TB(LF)(SN) | Battery NTC input |
| J5 | Molex 0732511150 | Edge-launch SMA RF output |
| J6 | JST-GH SM04B-GHS-TB(LF)(SN) | Optional BME680/environmental I2C input |

## Magnetics

| Ref | Part | Function |
|---|---|---|
| L1 | Coilcraft XAL7070-222MEC | BQ25798 charger inductor |
| L2 | Coilcraft XAL7030-222MEC | TPS61088 boost inductor |

## Protection and Indicators

| Ref | Part/class | Function |
|---|---|---|
| F1 | Littelfuse 0483005.DR | Solar input fuse |
| D1 | Low-current red LED | BQ25798 charge status |

## Passive Numbering Blocks

Use these blocks during schematic capture:

| Range | Subsystem |
|---|---|
| R100-C199 | Solar input protection |
| R200-C299 | BQ25798 charger |
| R300-C399 | Battery and XIAO supply path |
| R400-C499 | TPS61088 5 V boost |
| R500-C599 | E22 radio and RF support |
| R600-C699 | XIAO/module interface |

Do not create reference designators for test points, shunts, or bench-only configuration links; Rev A intentionally excludes them.
