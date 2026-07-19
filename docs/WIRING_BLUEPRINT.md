# 2Watt Project Wiring Blueprint

## Core modules

- Seeed Studio XIAO nRF52840, standard version
- EBYTE E22-900M33S 33 dBm LoRa module
- BQ25798 1-4 cell buck-boost solar/USB charger with MPPT and power path
- TPS61088 5 V boost stage for the E22 radio rail
- MAX17048 1-cell fuel gauge
- Protected 1S flat LiPo without external temperature sensing
- Board-mounted XT30 for solar
- Board-mounted XT30 for battery
- Board-edge SMA female connector
- XIAO underside pads wired to a removable 8-pin JST-PH 2.0 harness

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

Short flexible wires are soldered directly to the XIAO underside pads. The wires terminate in an 8-position JST-PH plug. The carrier PCB contains the matching board-mounted JST-PH receptacle.

| Bottom pad | nRF52840 pin | JST pin | Assignment | Notes |
|---|---|---:|---|---|
| SWDIO | SWDIO | 1 | SWDIO | Debug and recovery |
| SWCLK | SWCLK | 2 | SWCLK | Debug and recovery |
| 3V3 | 3V3 | 3 | 3V3_REF | Debug reference only, not an external power input |
| GND | GND | 4 | GND | Signal/debug ground |
| NFC1 | P0.09 | 5 | POWER_BUTTON_SENSE | Configure UICR for GPIO rather than NFC |
| NFC2 | P0.10 | 6 | CHARGER_INT | Configure UICR for GPIO rather than NFC |
| RESET | P0.18 | 7 | RESET_N | Recovery/reset connection |
| Spare | TBD | 8 | RESERVED | Leave unconnected until needed |
| BAT | charger output | none | NC | XIAO onboard charger remains isolated |

## JST-PH 2.0 underside harness

Recommended connector: 8-position, 2.0 mm-pitch JST-PH family, keyed, surface-mount or through-hole board receptacle selected for mechanical access.

Harness rules:

- use thin, flexible stranded wire suitable for repeated XIAO removal
- keep wires short enough to avoid loops over the RF section
- add strain relief at the XIAO end with flexible adhesive or heat-shrink where practical
- do not let the harness carry mechanical load when unplugging the XIAO
- label pin 1 on the board and cable
- the XIAO and harness are removed together as one assembly

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

## Battery interface

- XT30 carries battery positive and negative only.
- No battery thermistor or battery-temperature signal is used in Rev A.
- Battery must include internal protection for over-charge, over-discharge, over-current and short circuit.
- Deployment instructions must state the battery manufacturer's permitted charging-temperature range.

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
- Power button: hardware latch/controller plus NFC1 button-sense input through the underside harness
- Provide a hard-off path that does not depend solely on firmware

## Unused or reserved

- XIAO BAT: no connection
- XIAO onboard battery ADC circuit: unused
- E22 DIO2: reserved unless firmware later adopts DIO2-based RF-switch control
