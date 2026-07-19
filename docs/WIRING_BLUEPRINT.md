# 2Watt Project Wiring Blueprint

## Core modules

- Seeed Studio XIAO nRF52840, standard version
- EBYTE E22-900M33S 33 dBm LoRa module
- BQ25798 1-4 cell buck-boost solar/USB charger with MPPT and power path
- TPS61088 5 V boost stage for the E22 radio rail
- MAX17048 1-cell fuel gauge
- Protected 1S flat LiPo
- Board-mounted XT30 for solar
- Board-mounted XT30 for battery
- Board-edge SMA female connector
- XIAO underside SWD pads routed to a 4-pin JST-PH 2.0 service connector

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

## XIAO underside pad assignments

| Bottom pad | nRF52840 pin | Assignment | Notes |
|---|---|---|---|
| NFC1 | P0.09 | POWER_BUTTON_SENSE | Must configure UICR for GPIO rather than NFC |
| NFC2 | P0.10 | CHARGER_INT | Interrupt/status input from BQ25798; configure as GPIO |
| SWDIO | SWDIO | JST-PH service connector pin 1 | Debug and recovery |
| SWCLK | SWCLK | JST-PH service connector pin 2 | Debug and recovery |
| 3V3 | 3V3 | JST-PH service connector pin 3 | Debug reference only, not external power input |
| GND | GND | JST-PH service connector pin 4 | Debug ground |
| BAT | charger output | NC | XIAO onboard charger remains isolated |
| RESET | P0.18 | Optional test pad | Keep accessible for recovery |

## JST-PH 2.0 service connector

Recommended: 4-pin surface-mount JST-PH family connector.

Pinout:

1. SWDIO
2. SWCLK
3. 3V3 reference
4. GND

This connector is strictly for low-current programming/debugging. It is not a battery or solar connector.

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
XIAO USB-C VBUS -> XIAO 5V pad -> protection/current limit -> BQ25798 input 2
BQ25798 BAT -> protected 1S LiPo via XT30
BQ25798 SYS -> system rail
system rail -> TPS61088 -> 5.0 V radio rail -> load switch -> E22 VCC pins 9 and 10
system rail -> dedicated XIAO supply path -> XIAO 5V pin
```

Important: the XIAO BAT pad is left unconnected. USB data remains native to the XIAO USB-C connector, while VBUS is tapped from the documented 5V pad for the main charger input.

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

- Charge LED: driven from charger status output or charger-controlled logic
- Full/standby LED: charger status output where supported
- System status: XIAO onboard RGB LED to avoid consuming another external GPIO
- Power button: hardware latch/controller plus NFC1 button-sense input
- Provide a long-press hard-off path that does not depend solely on firmware

## Unused or reserved

- XIAO BAT: no connection
- XIAO onboard battery ADC circuit: unused
- E22 DIO2: reserved unless firmware later adopts DIO2-based RF-switch control
