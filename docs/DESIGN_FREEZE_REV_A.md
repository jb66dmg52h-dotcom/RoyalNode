# 2Watt Project Rev A Design Freeze

## Status

Rev A is frozen for KiCad schematic capture. This document is the primary source of truth. Earlier concept notes are superseded where they conflict with this file.

## Locked functions

- MeshCore-compatible repeater carrier
- Seeed Studio XIAO nRF52840, standard version
- EBYTE E22-900M33S high-power 915 MHz radio module
- Protected 1S flat LiPo, 10 Ah target
- Board-mounted XT30 battery input
- Board-mounted XT30 solar input
- USB-C firmware updates through the XIAO
- USB-C charging through the main charger
- 12 V nominal solar panel support
- 10 W panel supported; 20 W recommended
- Battery voltage and state-of-charge telemetry
- One external charge LED
- Direct 50-ohm PCB trace from E22 ANT to board-edge SMA
- Automatic startup when battery is connected
- Factory assembly for all pick-and-place-compatible parts

## Removed functions

- Power button
- eFuse
- Radio load switch
- Battery temperature sensing
- Pogo pins
- SWD connector
- Multi-wire XIAO harness
- Full/fault/system LEDs on the carrier
- Solar-present telemetry
- USB-present telemetry
- Battery reverse-polarity protection
- Radio-disable jumper
- Display, GPS and environmental sensors

## Locked power tree

```text
12 V nominal solar panel
  -> board-mounted XT30
  -> 2 A SMD fuse
  -> reverse-polarity MOSFET
  -> 22 V TVS
  -> BQ25798 solar input

XIAO USB-C VBUS
  -> protected current-limited path
  -> BQ25798 USB input

Protected 1S LiPo
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

## Locked interfaces

### XIAO to E22

| XIAO pin | Signal |
|---|---|
| D0 | E22 NRST |
| D1 | E22 DIO1 |
| D2 | E22 BUSY |
| D3 | E22 NSS |
| D4 | I2C SDA |
| D5 | I2C SCL |
| D6 | E22 TXEN |
| D7 | E22 RXEN |
| D8 | SPI SCK |
| D9 | SPI MISO |
| D10 | SPI MOSI |

All 11 exposed XIAO GPIO pins are allocated. Charger data and fuel-gauge data are polled over I2C.

### XIAO power connector

- 2-pin JST-PH, 2.0 mm pitch
- Pin 1: protected 1S supply after LM66100
- Pin 2: GND
- XIAO-side wires solder directly to underside BAT and GND pads
- XIAO remains socketed on its edge pins

## Locked electrical targets

- Battery: protected 1S, 10 Ah target
- Battery discharge: at least 5 A continuous; 8 A transient preferred
- Battery charge permission: at least 2 A
- Maximum charge current: 2.0 A
- E22 rail: 5.0 V nominal
- 5 V rail: 2 A continuous, 3 A transient design target
- TPS61088 switching frequency: approximately 500 kHz
- TPS61088 inductor: 2.2 uH
- BQ25798 switching frequency: 750 kHz
- BQ25798 inductor: 2.2 uH
- E22 local bulk capacitance: 330-470 uF plus ceramics
- No battery thermistor; BQ25798 TS is biased to normal with equal resistors

## Locked board assumptions

- 4-layer controlled-impedance PCB
- ENIG finish preferred
- Continuous ground plane directly below RF path
- TPS61088 and charger switching loops kept away from E22/SMA
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
