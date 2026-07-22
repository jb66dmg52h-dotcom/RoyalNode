# 2Watt Project Rev A Design Freeze

## Status

Rev A is frozen for KiCad schematic capture. This document is the primary source of truth. Earlier concept notes are superseded where they conflict with this file.

## Locked functions

- MeshCore-compatible repeater carrier
- Seeed Studio XIAO nRF52840, standard version
- EBYTE E22-900M33S high-power 915 MHz radio module
- Protected 1S 3.6/3.7 V Li-ion/LiPo pack, 10-20 Ah class
- Board-mounted XT30 battery input
- Board-mounted XT30 solar input
- USB-C firmware updates through the XIAO
- USB-C charging through the main charger
- 12 V nominal solar panel support
- 10 W panel supported; 20 W recommended
- Battery voltage and charger telemetry through BQ25798
- Battery-mounted NTC temperature sensing for charge protection
- One external charge LED
- Direct 50-ohm PCB trace from E22 ANT to board-edge SMA
- Automatic startup when battery is connected
- Factory assembly for all pick-and-place-compatible parts

## Removed functions

- Dedicated fuel gauge / MAX17048
- Battery state-of-charge percentage estimation
- Power button
- eFuse
- Radio load switch
- Pogo pins
- SWD connector
- Multi-wire XIAO harness
- Full/fault/system LEDs on the carrier
- Solar-present telemetry
- USB-present telemetry
- Battery reverse-polarity protection
- Radio-disable jumper
- Display, GPS and environmental sensors
- Bench-test configuration jumpers or bypass networks

## Locked power tree

```text
12 V nominal solar panel
  -> board-mounted XT30
  -> 2 A input protection chain
  -> BQ25798 solar input

XIAO USB-C VBUS
  -> protected current-limited path
  -> BQ25798 USB input

Protected 1S Li-ion/LiPo
  <-> board-mounted XT30
  <-> BQ25798 BAT / power path

BQ25798 SYS
  -> TPS61088
  -> regulated 5.0 V
  -> E22-900M33S directly

Protected battery/system node
  -> LM66100 ideal diode
  -> board-mounted 2-pin JST-PH
  -> short two-wire harness
  -> XIAO BAT and GND underside pads
```

The XIAO 5V/VBUS pad is not driven by the carrier board. The XIAO BAT pad is used for the two-wire carrier power connection. LM66100 blocks reverse current from the XIAO onboard charger into the main battery rail.

## Battery temperature protection

- Real battery-mounted NTC is required; TS is not bypassed in normal operation.
- Thermistor: Semitec 103AT-2, 10 kOhm NTC at 25 C.
- BQ25798 TS network: 5.23 kOhm from REGN to TS, 30.1 kOhm from TS to the NTC node, thermistor from NTC node to GND.
- Charging policy target for generic 4.2 V 1S Li-ion/LiPo packs: suspend charging below 0 C and at/above 45 C.
- No bench-test divider, TS bypass jumper, or alternate simulated-temperature network is included.

## Locked interfaces

### Final XIAO GPIO map

| XIAO pin | nRF52840 GPIO | Function |
|---|---|---|
| D0 | P0.02 | E22 NRST |
| D1 | P0.03 | E22 DIO1 |
| D2 | P0.28 | E22 BUSY |
| D3 | P0.29 | E22 NSS / SPI chip select |
| D4 | P0.04 | I2C SDA, BQ25798 |
| D5 | P0.05 | I2C SCL, BQ25798 |
| D6 | P1.11 | E22 RXEN, active high |
| D7 | P1.12 | TPS61088 EN |
| D8 | P1.13 | E22 SPI SCK |
| D9 | P1.14 | E22 SPI MISO |
| D10 | P1.15 | E22 SPI MOSI |

All eleven exposed XIAO GPIO pins are allocated.

### E22 RF switch control

- E22 DIO2 connects directly to E22 TXEN.
- TXEN is therefore controlled by the SX1262 DIO2 RF-switch function and does not consume a XIAO GPIO.
- E22 RXEN remains under XIAO control on D6.
- Firmware must enable the SX1262 DIO2 RF-switch control function and must not also configure a separate MCU TXEN pin.

### BQ25798 interrupt handling

- BQ25798 INT does not consume a XIAO GPIO.
- Charger status and fault registers are polled over I2C.
- INT retains the datasheet-recommended 10 kOhm pull-up to the 3.3 V logic rail but is not routed to the MCU.

### XIAO power connector

- 2-pin JST-PH, 2.0 mm pitch
- Pin 1: protected 1S supply after LM66100
- Pin 2: GND
- XIAO-side wires solder directly to underside BAT and GND pads
- XIAO remains socketed on its edge pins

## Locked electrical targets

- Battery: protected 1S 3.6/3.7 V nominal, 4.20 V maximum, 10-20 Ah class
- Battery discharge: at least 5 A continuous; 8 A transient preferred
- Battery charge permission: at least 2 A
- Maximum charge current: 2.0 A
- Battery telemetry: BQ25798 voltage/charger telemetry only; no dedicated SOC gauge
- E22 rail: 5.0 V nominal
- 5 V rail: 2 A continuous design target
- TPS61088 inductor: Coilcraft XAL7030-222MEC, 2.2 uH
- TPS61088 RFREQ: 330 kOhm from FSW to SW
- TPS61088 ILIM: 100 kOhm to AGND
- TPS61088 feedback: 176 kOhm top / 56.0 kOhm bottom, 0.1%
- TPS61088 compensation: 20.0 kOhm and 4.7 nF
- TPS61088 soft-start: 47 nF
- TPS61088 VCC bypass: 2.2 uF
- TPS61088 BOOT capacitor: 100 nF from BOOT to SW
- TPS61088 MODE: floating for PFM/light-load efficiency
- TPS61088 EN: XIAO D7 controlled; 100 kOhm pulldown keeps the 5 V radio rail off during MCU startup
- TPS61088 input capacitance: 2 x 22 uF plus 100 nF local VIN bypass
- TPS61088 output capacitance: 2 x 47 uF, 10 V ceramic; exact manufacturer part must be verified for effective capacitance at 5 V bias
- BQ25798 switching frequency: 750 kHz
- BQ25798 inductor: Coilcraft XAL7070-222MEC, 2.2 uH
- E22 local bulk capacitance: 330-470 uF plus ceramics

## Locked board assumptions

- 4-layer controlled-impedance PCB
- ENIG finish preferred
- Continuous ground plane directly below RF path
- TPS61088 and charger switching loops kept away from E22/SMA
- TPS61088 input/output capacitors, BOOT capacitor and inductor placed immediately around the converter to minimize high-di/dt loops
- SW copper kept as small as practical
- XT30 and SMA footprints require mechanical support
- Board-only design; enclosure design is outside Rev A scope

## Remaining work inside KiCad

- Build or import verified symbols and footprints
- Capture schematic
- Run ERC
- Perform schematic compatibility review
- Place components
- Obtain fabricator stack-up and calculate 50-ohm geometry
- Route power and RF
- Run DRC and manufacturing review
