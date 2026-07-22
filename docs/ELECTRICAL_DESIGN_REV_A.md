# 2Watt Project Electrical Design, Rev A

## Status

Locked for KiCad schematic capture. Battery physical packaging and enclosure design are outside this scope.

## System architecture

```text
SOLAR XT30
  -> 2 A input protection chain
  -> BQ25798 solar input (VAC1 / ACDRV1, primary port)

XIAO USB-C VBUS
  -> BQ25798 USB input (VAC2 / ACDRV2, secondary port)

PROTECTED 1S LI-ION/LIPO
  <-> BATTERY XT30
  <-> BQ25798 BAT/SYS power path

BQ25798 SYS
  -> TPS61088 boost
  -> 5.0 V
  -> E22-900M33S directly

PROTECTED BATTERY/SYSTEM NODE
  -> LM66100 ideal diode
  -> 2-pin JST-PH
  -> XIAO BAT and GND underside pads
```

## 1. Solar input

The LTC4365-based solar protection architecture is authoritative. Final KiCad capture must use the current locked protection chain rather than the older P-FET/TVS-only concept.

Solar is assigned to BQ25798 port 1 (`VAC1` / `ACDRV1`). TI defines port 1 as the higher-priority port when both inputs appear simultaneously. Firmware must also explicitly prefer port 1 when solar becomes valid after USB is already active, because in dual-input mode the BQ25798 otherwise keeps the first-present valid source until host intervention or until that source becomes invalid.

USB-C is assigned to BQ25798 port 2 (`VAC2` / `ACDRV2`).

## 2. Main charger and power path

### Charger

- U1: TI BQ25798RQMR
- cell count: 1S
- battery class: protected 3.6/3.7 V nominal Li-ion/LiPo, 4.20 V maximum
- maximum programmed charge current: 2.0 A
- switching frequency: 750 kHz
- inductor: Coilcraft XAL7070-222MEC, 2.2 uH

### Startup configuration

- PROG: 4.7 kOhm, 1%, to GND for 1S / 750 kHz POR configuration
- /CE: tied low
- D+ and D- on BQ25798: no connection
- SDA/SCL: 3.3 V I2C bus to XIAO D4/D5
- charger status: one hardware charge LED
- battery voltage, charger telemetry and fault state: polled from BQ25798 over I2C
- watchdog: disabled by host firmware
- ADC: enabled by host firmware
- MPPT: enabled and restored by host firmware when solar charging is active
- Rev A has no dedicated fuel gauge and does not provide a ModelGauge-style battery percentage estimate

### Dual input

- VAC1 pin 9: solar protected-source sense node
- ACDRV1 pin 11: solar ACFET1/RBFET1 gates
- VAC2 pin 8: USB-C source-sense node
- ACDRV2 pin 10: USB ACFET2/RBFET2 gates
- each input uses its own back-to-back N-channel MOSFET pair
- the two paths meet only at common VBUS after their respective selector pair
- sources must not backfeed one another

### Battery temperature sensing

- Physical battery-mounted NTC required
- NTC: Semitec 103AT-2, 10 kOhm at 25 C
- RTOP: 5.23 kOhm from REGN to TS
- RBOT: 30.1 kOhm from TS to the NTC node
- NTC from NTC node to GND
- TS is not bypassed in normal operation
- Charge policy target: suspend below 0 C and at/above 45 C for generic 4.2 V 1S Li-ion/LiPo packs
- No bench-test jumper, simulated-temperature divider or alternate TS bypass network
- temperature connector: Molex 5037630291 board header + 5037640201 cable housing + 5037650098 contacts

### Locked BQ25798 supporting parts

- VBUS: 2 x 10 uF plus 100 nF
- PMID: 3 x 10 uF plus 100 nF
- SYS: 5 x 10 uF plus 100 nF
- BAT: 2 x 10 uF
- REGN: 4.7 uF
- BTST1: 47 nF
- BTST2: 47 nF
- SDRV: 1 nF to GND
- BATP: 100 Ohm series resistor on a dedicated Kelvin trace from battery positive
- ILIM_HIZ: tied to REGN
- INT: 10 kOhm pull-up to 3.3 V; not routed to MCU
- QON: no external connection; internal pull-up retained

Exact manufacturer parts are listed in `docs/LOCKED_COMPONENTS_REV_A.md` and `docs/RESISTOR_BOM_REV_A.md`.

## 3. Battery interface

- Board-mounted AMASS XT30PW-M power connector
- protected 1S 3.6/3.7 V nominal Li-ion/LiPo pack
- target capacity: 10-20 Ah class
- maximum voltage: 4.20 V
- design minimum system input: 2.7-3.0 V region, subject to battery protection cutoff
- discharge capability: at least 5 A continuous, 8 A transient preferred
- permitted charge current: at least 2 A
- battery-mounted Semitec 103AT-2 NTC required
- dedicated Molex Pico-Lock 2-pin temperature connection
- no carrier battery reverse-polarity protection

## 4. XIAO power path

### Locked connection

The carrier does not drive the XIAO 5V/VBUS pin.

- U2: TI LM66100DCKR ideal diode
- pin 1 VIN: protected battery/system node
- pin 2 GND: ground
- pin 3 CE: **connect to VOUT** for always-on reverse-current blocking
- pin 4 NC: no connection
- pin 5 ST: **connect to GND** because status is unused
- pin 6 VOUT: board-mounted JST B2B-PH-SM4-TB(LF)(SN) positive pin
- cable housing: JST PHR-2
- wire 1: positive to XIAO BAT underside pad
- wire 2: ground to XIAO GND underside pad
- 1 uF input capacitor
- 1 uF output capacitor

### LM66100 audit correction

Earlier notes stated `CE tied high` and `ST not connected`. Those instructions are superseded. TI specifies that CE can be connected to VOUT for always-on reverse-current blocking and must not float; TI also specifies connecting ST to GND when status is unused. Rev A therefore uses **CE -> VOUT** and **ST -> GND**.

The LM66100 blocks reverse current from the XIAO onboard charger into the main battery rail while adding very little forward voltage drop.

### Mechanical arrangement

- XIAO edge pins plug into two 1x7 socket headers
- short flexible power wires are soldered to XIAO BAT and GND underside pads
- disconnect the 2-pin JST before removing the XIAO
- no pogo contacts, SWD connector or multi-wire harness

## 5. TPS61088 5 V rail

### Production-locked parts and values

- U3: TI TPS61088RHLR
- input: BQ25798 SYS / 1S system rail, 2.7-4.2 V operating design range
- output target: approximately 5.0 V nominal
- continuous target: 2 A
- inductor: Coilcraft XAL7030-222MEC, 2.2 uH
- feedback divider: 176 kOhm top / 56.0 kOhm bottom, 0.1%
- frequency resistor: 330 kOhm from FSW to SW
- current-limit resistor: 100 kOhm to AGND
- compensation: 20.0 kOhm and 4.7 nF
- soft-start capacitor: 47 nF
- VCC bypass: 2.2 uF
- BOOT capacitor: 100 nF from BOOT to SW
- MODE: floating for PFM/light-load efficiency
- EN: XIAO D7 with 100 kOhm pulldown so radio 5 V is off during MCU startup
- TPS61088 package NC pins 11/12 connect to ground plane for thermal dissipation per TI
- exposed PGND thermal pad is symbol/footprint pad 21 and must connect to power ground with thermal vias
- no PFM/PWM selection jumper or bench-test configuration footprint

### Input capacitors

- 2 x Murata GRM31CZ71C226ME15L, 22 uF, 16 V, X7R, 1206
- 100 nF local VIN bypass placed immediately at the IC

### Output and E22 capacitors

Near TPS61088:

- 2 x TDK C3225X5R1A476MT000E, 47 uF, 10 V, X5R, 1210

Near E22:

- 2 x 22 uF / 16 V X7R
- 1 uF / 16 V X7R
- multiple 100 nF ceramics
- Panasonic 10SVPC330M, 330 uF / 10 V polymer, 19 mOhm ESR

### TPS61088 layout rules

- inductor immediately adjacent to converter
- BOOT capacitor immediately adjacent to BOOT/SW pins
- input and output capacitors immediately adjacent to their power/ground pins
- smallest practical SW copper area
- solid ground plane directly below converter area
- keep complete boost switching block away from E22 RF feed and SMA route

## 6. E22 interface

- E22 VCC pins 9/10 connected directly to regulated 5 V
- logic interface is 3.3 V from XIAO; do not use 5 V logic
- no load switch and no eFuse
- NRST, BUSY and DIO1 route directly to assigned XIAO pins
- E22 DIO2 pin 8 connects directly to E22 TXEN pin 7
- TXEN is active high and is driven by SX1262 DIO2 RF-switch function, not by a XIAO GPIO
- RXEN pin 6 is active high and controlled by XIAO D6
- firmware must enable SX1262 DIO2 RF-switch function and must not define a separate MCU TXEN pin
- current EBYTE pin documentation does not mandate an external RXEN/TXEN pull-down value; no such resistor is to be invented without a documented need

### Final XIAO GPIO map

| XIAO pin | nRF52840 GPIO | Function |
|---|---|---|
| D0 | P0.02 | E22 NRST pin 15 |
| D1 | P0.03 | E22 DIO1 pin 13 |
| D2 | P0.28 | E22 BUSY pin 14 |
| D3 | P0.29 | E22 NSS pin 19 |
| D4 | P0.04 | BQ25798 SDA pin 15 |
| D5 | P0.05 | BQ25798 SCL pin 14 |
| D6 | P1.11 | E22 RXEN pin 6 |
| D7 | P1.12 | TPS61088 EN pin 2 |
| D8 | P1.13 | E22 SCK pin 18 |
| D9 | P1.14 | E22 MISO pin 16 |
| D10 | P1.15 | E22 MOSI pin 17 |

All eleven exposed XIAO GPIOs are allocated. BQ25798 INT is not routed to XIAO; charger status/faults are polled over I2C.

### MeshCore/RadioLib integration requirements

The custom RoyalNode variant must use XIAO D8/D9/D10 for SPI, D3 as chip-select, D0 as reset, D2 as BUSY, D1 as DIO1, D6 as RXEN, and enable SX1262 DIO2 RF-switch function for TXEN. TPS61088 D7 enable is handled by RoyalNode board startup/power-management code before radio initialization.

## 7. Battery telemetry

Rev A does not include a dedicated fuel gauge. The BQ25798 ADC and status registers are the sole carrier-board source of battery and charger telemetry.

Firmware may report:

- battery voltage
- battery charge/discharge current when the relevant ADC is enabled
- charger state
- VBUS/VAC input measurements
- charger fault/status information
- TS percentage and charger die temperature if useful

Rev A does not claim an accurate battery state-of-charge percentage. Any UI battery indication derived only from voltage must be identified as an estimate rather than fuel-gauge SOC.

## 8. Charge LED

- one external red charge/status LED only
- LED: Everlight 19-217/R6C-AL1M2VY/3T, 0603
- BQ25798 STAT drives LED directly using open-drain output; no buffer transistor
- topology: 3.3 V -> LED -> 2.2 kOhm -> STAT
- nominal current around 0.6 mA
- charging: LED on
- charge complete / charging disabled / battery-only: LED off
- fault/suspend indication follows BQ25798 STAT blink behavior
- no full, fault or carrier system LEDs

## 9. RF path

- E22 pin 21 ANT to Molex 0732511150 board-edge SMA through short 50-ohm grounded coplanar waveguide
- E22 pins 20/22 are immediate local RF grounds
- solid Layer-2 ground reference directly below
- ground-via fence along route
- no digital or switching-power route crossing RF keepout
- no 0-ohm link, pi network, DC-block capacitor, test connector or unverified RF TVS
- E22 ANT side faces the SMA edge and is placed as close as practical to the connector

## 10. PCB stack-up

- fabricator: JLCPCB
- 4 layers
- 1.6 mm finished thickness
- preferred stack-up: JLC04161H-3313
- outer copper 1 oz target; inner copper 0.5 oz target

Layer intent:

1. Top: components, RF and critical power loops
2. Inner 1: uninterrupted ground plane
3. Inner 2: power distribution and low-speed signals
4. Bottom: low-speed routing and ground copper

Keep BQ25798 and TPS61088 hot loops compact. Place the RF launch at the opposite/quiet board edge and compress the board outline only after real footprints are loaded.

## 11. Automatic startup

There is no power button. Connecting the protected battery powers the XIAO through LM66100. The XIAO intentionally enables the TPS61088 radio rail on D7 after board initialization. The battery XT30 is the master disconnect.

## 12. KiCad entry criteria

Before electrical capture is considered ready:

- use `docs/PIN_AUDIT_REV_A.md` as pin-number authority
- verify exact custom footprints against manufacturer mechanical drawings
- verify XIAO socket/header engagement
- produce final net-by-net map
- run repository contradiction search

After schematic capture:

- run ERC and schematic compatibility audit
- reproduce manufacturer reference-layout constraints
- confirm JLC production stack and controlled-impedance geometry before PCB routing release
