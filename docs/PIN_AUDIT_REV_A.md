# RoyalNode Rev A Manufacturer Pin Audit

## Status

This file is the pre-KiCad electrical pin-number audit. Pin numbers are taken from current manufacturer documentation. Connections shown here are the intended Rev A schematic connections and supersede earlier concept notes where they conflict.

## BQ25798RQMR — TI RQM 29-pin VQFN-HR

Source basis: TI BQ25798 Rev. C, June 2026, Table 5-1.

| Pin | Name | RoyalNode Rev A connection |
|---:|---|---|
| 1 | STAT | Charge LED sink: 3V3 -> red LED -> 2.2 kOhm -> STAT |
| 2,3 | VBUS | Common charger input after the active input-selector MOSFETs; 2 x 10 uF + 100 nF to GND |
| 4 | BTST1 | 47 nF to SW1 |
| 5 | REGN | 4.7 uF to GND; source for TS bias and ILIM_HIZ high state |
| 6 | D+ | NC |
| 7 | D- | NC |
| 8 | VAC2 | USB-C source-sense node before USB ACFET/RBFET pair |
| 9 | VAC1 | Solar protected-source sense node before solar ACFET/RBFET pair |
| 10 | ACDRV2 | Gates of USB ACFET2/RBFET2 common-source pair |
| 11 | ACDRV1 | Gates of solar ACFET1/RBFET1 common-source pair |
| 12 | QON | No external connection; internal pull-up retained; no ship/reset button in Rev A |
| 13 | CE | GND; active-low charge enable |
| 14 | SCL | XIAO D5, 10 kOhm pull-up to 3V3 |
| 15 | SDA | XIAO D4, 10 kOhm pull-up to 3V3 |
| 16 | TS | 103AT-2 temperature network: 5.23 kOhm REGN-to-TS, 30.1 kOhm TS-to-NTC node, NTC to GND |
| 17 | ILIM_HIZ | REGN, selecting maximum hardware input-current ceiling so firmware IINDPM controls the lower limit |
| 18 | BATP | Dedicated battery-positive Kelvin sense through 100 Ohm series resistor |
| 19 | BTST2 | 47 nF to SW2 |
| 20 | PROG | 4.70 kOhm, 1%, to GND; 1S / 750 kHz POR configuration |
| 21 | INT | 10 kOhm pull-up to 3V3; not connected to MCU; firmware polls I2C status/fault registers |
| 22,23 | BAT | Battery-positive power node; 2 x 10 uF to GND |
| 24 | SDRV | No external ship FET; 1 nF / 50 V to GND |
| 25 | SYS | System rail; 5 x 10 uF + 100 nF to GND; feeds TPS61088 input path |
| 26 | SW2 | Charger inductor terminal 2 |
| 27 | GND | Power ground |
| 28 | SW1 | Charger inductor terminal 1 |
| 29 | PMID | 3 x 10 uF + 100 nF to GND |

### Dual-input assignment

- Port 1 (`VAC1` / `ACDRV1`) = **SOLAR**.
- Port 2 (`VAC2` / `ACDRV2`) = **USB-C**.

TI states port 1 has priority when both inputs appear simultaneously. This assignment matches RoyalNode's policy that solar is the primary charging source. Firmware must also explicitly prefer port 1 when solar becomes valid after USB is already active, because the charger otherwise keeps the first-present valid source until host intervention or that source becomes invalid.

## TPS61088RHLR — TI RHL 20-pin VQFN + exposed thermal pad

Source basis: TI TPS61088 Rev. D, Table 5-1.

| Pin | Name | RoyalNode Rev A connection |
|---:|---|---|
| 1 | VCC | 2.2 uF to AGND |
| 2 | EN | XIAO D7; 100 kOhm pulldown to GND |
| 3 | FSW | 330 kOhm to SW |
| 4,5,6,7 | SW | Switching node; inductor/BOOT/RFREQ network; keep copper compact |
| 8 | BOOT | 100 nF to SW |
| 9 | VIN | BQ25798 SYS rail; 2 x 22 uF + 100 nF local bypass |
| 10 | SS | 47 nF to AGND |
| 11,12 | NC | TI recommends connecting these package NC pins to the ground plane for thermal dissipation |
| 13 | MODE | Floating for PFM light-load mode |
| 14,15,16 | VOUT | 5 V rail; 2 x 47 uF local output capacitors; feeds E22 |
| 17 | FB | Junction of 176 kOhm VOUT-to-FB and 56.0 kOhm FB-to-AGND |
| 18 | COMP | 20.0 kOhm / 4.7 nF compensation network to AGND |
| 19 | ILIM | 100 kOhm to AGND |
| 20 | AGND | Signal ground |
| EP / 21 | PGND | Exposed thermal/power-ground pad; solid ground and thermal vias per TI land pattern |

Important symbol note: TI's pin table numbers the exposed PGND thermal pad as 21 even though the package is described as 20-pin VQFN. KiCad symbol/footprint must preserve that numbering.

## LM66100DCKR — TI DCK 6-pin SC-70

Source basis: TI LM66100 Rev. A.

| Pin | Name | RoyalNode Rev A connection |
|---:|---|---|
| 1 | VIN | Protected battery/system node |
| 2 | GND | GND |
| 3 | CE | **VOUT** for always-on reverse-current blocking |
| 4 | NC | NC |
| 5 | ST | **GND** because status is unused |
| 6 | VOUT | XIAO_BAT_ISO -> JST-PH -> XIAO BAT |

### Mandatory correction

Earlier RoyalNode documents said `CE tied high` and `ST NC`. That is incorrect for the intended function. TI states CE is an active-low comparator input and specifically recommends connecting CE to VOUT for always-on reverse-current blocking. TI also states ST should be connected to GND when unused. KiCad must use **CE -> VOUT** and **ST -> GND**.

## LTC4365ITS8-1#TRMPBF — ADI TS8 8-pin TSOT-23

Source basis: Analog Devices LTC4365 Rev. B pin configuration and pin functions.

| Pin | Name | RoyalNode Rev A connection |
|---:|---|---|
| 1 | VIN | Solar input after 2 A fuse |
| 2 | UV | LTC threshold divider node |
| 3 | OV | LTC threshold divider node |
| 4 | GND | GND |
| 5 | SHDN | 100 kOhm to VIN for always-on operation with input-fault current limiting |
| 6 | FAULT | NC in Rev A; no solar-fault telemetry GPIO |
| 7 | VOUT | Sense protected output after the LTC-controlled MOSFET pair |
| 8 | GATE | Common gates of the LTC4365 back-to-back N-MOSFET pair |

The -1 variant gives the faster recovery behavior. The LTC4365 datasheet says an unused SHDN should be connected to VIN and recommends at least 100 kOhm series resistance where VIN may go negative or ring high; Rev A therefore uses 100 kOhm from SHDN to VIN rather than a direct short.

## ISA170170N04LMDSXTMA1 — Infineon PG-DSO-8 dual N-channel MOSFET

Source basis: Infineon ISA170170N04LMDS Rev. 2.0.

| Pin | Function |
|---:|---|
| 1 | Source 1 |
| 2 | Gate 1 |
| 3 | Drain 2 |
| 4 | Gate 2 |
| 5 | Drain 2 |
| 6 | Source 2 |
| 7 | Drain 1 |
| 8 | Drain 1 |

For every back-to-back pair implementation:

- Source 1 and Source 2 are tied together as the common-source node.
- Gate 1 and Gate 2 are tied together to the appropriate driver (`LTC4365 GATE`, `BQ25798 ACDRV1`, or `BQ25798 ACDRV2`).
- Drain 1 and Drain 2 form the two ends of the protected path.

The exact assignment of Drain 1 versus Drain 2 to connector-side/load-side does not alter the back-to-back common-source blocking function, but the same orientation should be used consistently in the schematic and layout to avoid footprint confusion.

## EBYTE E22-900M33S — 22 castellated pins

Source basis: current EBYTE product pin-definition table.

| Pin | Name | RoyalNode Rev A connection |
|---:|---|---|
| 1-5 | GND | Ground plane |
| 6 | RXEN | XIAO D6, active high |
| 7 | TXEN | Directly to module DIO2 pin 8, active high |
| 8 | DIO2 | Directly to TXEN pin 7; firmware enables SX1262 DIO2 RF-switch control |
| 9,10 | VCC | Regulated 5 V, local ceramic + polymer decoupling |
| 11,12 | GND | Ground plane |
| 13 | DIO1 | XIAO D1 |
| 14 | BUSY | XIAO D2 |
| 15 | NRST | XIAO D0, active low |
| 16 | MISO | XIAO D9 |
| 17 | MOSI | XIAO D10 |
| 18 | SCK | XIAO D8 |
| 19 | NSS | XIAO D3 |
| 20 | GND | RF ground immediately adjacent to ANT |
| 21 | ANT | Direct 50-ohm GCPW to SMA center |
| 22 | GND | RF ground immediately adjacent to ANT |

EBYTE specifies 3.3 V logic levels and warns that 5 V TTL can damage the module logic. XIAO nRF52840 logic is 3.3 V, so the interface is compatible.

The current EBYTE pin table does not specify mandatory external pull-down resistor values on RXEN/TXEN. Do not invent pull-downs solely because older concept notes mentioned them; the final firmware/power-off state will be handled in the net map after confirming SX1262/module startup behavior.

## XIAO nRF52840 exposed GPIOs

| XIAO pin | nRF52840 GPIO | RoyalNode function |
|---|---|---|
| D0 | P0.02 | E22 NRST |
| D1 | P0.03 | E22 DIO1 |
| D2 | P0.28 | E22 BUSY |
| D3 | P0.29 | E22 NSS |
| D4 | P0.04 | BQ25798 SDA |
| D5 | P0.05 | BQ25798 SCL |
| D6 | P1.11 | E22 RXEN |
| D7 | P1.12 | TPS61088 EN |
| D8 | P1.13 | E22 SCK |
| D9 | P1.14 | E22 MISO |
| D10 | P1.15 | E22 MOSI |

## Remaining pin-audit work

- Verify XIAO underside BAT/GND pad physical numbering/orientation for the two-wire harness drawing.
- Convert this audit into the final net-by-net KiCad capture map.
- Check the final imported KiCad symbols against this table before connecting any nets.
