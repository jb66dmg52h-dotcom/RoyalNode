# 2Watt Project Wiring Blueprint

## Core modules

- Seeed Studio XIAO nRF52840, standard version
- EBYTE E22-900M33S 33 dBm LoRa module
- BQ25798 buck-boost solar/USB charger with MPPT and power path
- TPS61088 5 V boost stage for the E22 radio rail
- MAX17048 1-cell fuel gauge
- Protected 1S flat LiPo without external temperature sensing
- Board-mounted XT30 for solar
- Board-mounted XT30 for battery
- Board-edge SMA female connector
- Socketed XIAO with a separate two-wire power lead terminating in a 2-pin JST-PH 2.0 plug

## XIAO radio pin map

| XIAO pin | nRF52840 pin | Connected device | Signal | Notes |
|---|---|---|---|---|
| D0 | P0.02 | E22 | NRST | Active-low radio reset |
| D1 | P0.03 | E22 | DIO1 | Radio interrupt |
| D2 | P0.28 | E22 | BUSY | Radio busy status |
| D3 | P0.29 | E22 | NSS | SPI chip select |
| D4 | P0.04 | Shared bus | SDA | BQ25798 + MAX17048 |
| D5 | P0.05 | Shared bus | SCL | BQ25798 + MAX17048 |
| D6 | P1.11 | E22 | TXEN | External RF switch transmit enable |
| D7 | P1.12 | E22 | RXEN | External RF switch receive enable |
| D8 | P1.13 | E22 | SCK | SPI clock |
| D9 | P1.14 | E22 | MISO | SPI radio-to-MCU |
| D10 | P1.15 | E22 | MOSI | SPI MCU-to-radio |

## XIAO power lead

Only two wires are soldered to the XIAO for the removable power connection.

| JST pin | Signal | XIAO connection |
|---:|---|---|
| 1 | +5V_XIAO | XIAO 5V/VBUS power pad |
| 2 | GND | XIAO ground pad |

The two wires terminate in a keyed 2-pin JST-PH 2.0 plug. The carrier PCB contains the matching board-mounted receptacle.

Rules:

- use flexible stranded wire
- keep the wires short
- add strain relief near the XIAO solder points
- mark polarity clearly
- never connect the project battery directly to the XIAO BAT pad
- the XIAO and two-wire lead are removed together

## Underside pads not used

The following underside pads are not connected to the carrier in Rev A:

- SWDIO
- SWCLK
- NFC1
- NFC2
- RESET
- BAT

Firmware updates and normal recovery use the XIAO USB-C connector and onboard reset button.

## I2C bus

Shared devices:

- BQ25798 charger/power-path controller
- MAX17048 fuel gauge

Requirements:

- 3.3 V pull-ups located on the carrier PCB
- short routing away from TPS61088 switch node
- confirm no I2C address collision
- include firmware recovery defaults if the charger fails to acknowledge

## Power tree

```text
12 V nominal solar panel -> XT30 -> fuse/TVS/reverse protection -> BQ25798 input 1
XIAO USB-C VBUS -> protected path -> BQ25798 input 2
BQ25798 BAT -> protected 1S LiPo via XT30
BQ25798 SYS -> TPS61088 -> regulated 5 V
regulated 5 V -> radio load switch -> E22
regulated 5 V -> 2-pin JST-PH lead -> XIAO 5V and GND
```

Important: the XIAO BAT pad remains unconnected. USB data stays native to the XIAO USB-C connector.

## Battery interface

- XT30 carries battery positive and negative only.
- No battery thermistor or battery-temperature signal is used in Rev A.
- Battery must include internal protection for over-charge, over-discharge, over-current and short circuit.

## E22 power and control

- E22 pins 9 and 10: 5.0 V radio rail
- E22 grounds: solid low-impedance ground plane
- DIO3: internally used by the E22 TCXO; firmware must configure 2.2 V TCXO control
- TXEN/RXEN logic:
  - TXEN=1, RXEN=0: transmit
  - TXEN=0, RXEN=1: receive
  - TXEN=0, RXEN=0: RF path closed
- Place bulk and ceramic capacitance directly beside E22 VCC pins

## RF path

```text
E22 ANT pad -> short 50-ohm controlled-impedance trace -> board-edge SMA female
```

Rules:

- no u.FL intermediate connector
- uninterrupted ground reference
- via fence beside RF trace
- no TPS61088 switch-node copper near radio or SMA
- calculate trace width from the final PCB stack-up
- enclosure must mechanically support the SMA

## LEDs and button

- Charge LED: driven directly from charger-status hardware
- Full/standby LED: driven directly from charger-status hardware where supported
- System status: XIAO onboard RGB LED
- Power button: handled by the hardware latch/controller, not by an extra XIAO GPIO
- hard-off must not depend solely on firmware

## Consequence of the two-wire-only XIAO lead

All 11 exposed XIAO GPIO pins remain allocated to the E22 and I2C bus. Rev A therefore does not route charger interrupt, power-button sense or SWD through the XIAO harness. Those functions must be autonomous in hardware or accessed through USB recovery.
