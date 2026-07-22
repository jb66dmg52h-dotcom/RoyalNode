# 2Watt Project Electrical Design, Rev A

## Status

Locked for KiCad schematic capture. Battery physical packaging and enclosure design are outside this scope.

## System architecture

```text
SOLAR XT30
  -> 2 A input protection chain
  -> BQ25798 solar input

XIAO USB-C VBUS
  -> protected/current-limited branch
  -> BQ25798 USB input

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

The previously locked LTC4365-based solar protection architecture remains authoritative in the project design notes. Final KiCad capture must use the current locked protection chain rather than the older P-FET/TVS-only concept.

## 2. Main charger and power path

### Charger

- U1: TI BQ25798RQMR
- cell count: 1S
- battery class: protected 3.6/3.7 V nominal Li-ion/LiPo, 4.20 V maximum
- maximum programmed charge current: 2.0 A
- switching frequency: 750 kHz
- inductor: Coilcraft XAL7070-222MEC, 2.2 uH

### Startup configuration

- PROG: 4.7 kOhm, 1%, to GND for 1S default configuration
- /CE: tied low
- D+ and D- on BQ25798: no connection
- SDA/SCL: 3.3 V I2C bus to XIAO D4/D5
- charger status: one hardware charge LED
- battery voltage, charger telemetry and fault state: polled from BQ25798 over I2C
- watchdog: disabled by host firmware
- ADC: enabled by host firmware
- MPPT: enabled and restored by host firmware when solar charging is active
- Rev A has no dedicated fuel gauge and does not provide a ModelGauge-style battery percentage estimate

### Battery temperature sensing

- Physical battery-mounted NTC required
- NTC: Semitec 103AT-2, 10 kOhm at 25 C
- RTOP: 5.23 kOhm from REGN to TS
- RBOT: 30.1 kOhm from TS to the NTC node
- NTC from NTC node to GND
- TS is not bypassed in normal operation
- Charge policy target: suspend below 0 C and at/above 45 C for generic 4.2 V 1S Li-ion/LiPo packs
- No bench-test jumper, simulated-temperature divider or alternate TS bypass network

### Locked BQ25798 supporting parts from the latest audit

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
- INT: 10 kOhm pull-up to 3.3 V; not routed to the MCU because all exposed XIAO GPIOs are allocated

Selected capacitors must meet required effective capacitance after DC-bias derating.

## 3. Battery interface

- Board-mounted XT30 power connector
- protected 1S 3.6/3.7 V nominal Li-ion/LiPo pack
- target capacity: 10-20 Ah class
- maximum voltage: 4.20 V
- design minimum system input: 2.7-3.0 V region, subject to battery protection cutoff
- discharge capability: at least 5 A continuous, 8 A transient preferred
- permitted charge current: at least 2 A
- battery-mounted Semitec 103AT-2 NTC required
- dedicated small locking temperature connector to be selected during connector BOM finalization
- no carrier battery reverse-polarity protection

## 4. XIAO power path

### Locked connection

The carrier does not drive the XIAO 5V/VBUS pin.

- U2: TI LM66100DCKR ideal diode
- LM66100 input: protected battery/system node
- LM66100 output: board-mounted JST B2B-PH-SM4-TB(LF)(SN)
- cable housing: JST PHR-2
- wire 1: positive to XIAO BAT underside pad
- wire 2: ground to XIAO GND underside pad
- CE tied high
- ST not connected
- 1 uF input capacitor
- 1 uF output capacitor

The LM66100 blocks reverse current from the XIAO onboard charger into the main battery rail while adding very little voltage drop.

### Mechanical arrangement

- XIAO edge pins plug into socket headers
- short flexible power wires are soldered to XIAO BAT and GND underside pads
- disconnect the 2-pin JST before removing the XIAO
- no pogo contacts, SWD connector or multi-wire harness

## 5. TPS61088 5 V rail

### Production-locked parts and values

- U3: TI TPS61088RHLR
- input: 1S Li-ion/LiPo system rail, 2.7-4.2 V operating design range
- output target: 5.0 V nominal
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
- no PFM/PWM selection jumper or bench-test configuration footprint

### Input capacitors

- 2 x 22 uF, 10 V ceramic
- 100 nF local VIN bypass placed immediately at the IC

### Output and E22 capacitors

Near TPS61088:

- 2 x 47 uF, 10 V ceramic, 1210 target
- exact manufacturer part number must be verified for effective capacitance at 5 V DC bias

Near E22:

- 2 x 22 uF, 10 V ceramic
- 1 uF ceramic
- multiple 100 nF ceramics
- 330-470 uF low-ESR bulk

### TPS61088 layout rules

- inductor immediately adjacent to the converter
- BOOT capacitor immediately adjacent to BOOT/SW pins
- input and output capacitors immediately adjacent to their power/ground pins
- smallest practical SW copper area
- solid ground plane directly below converter area
- keep the complete boost switching block away from E22 RF feed and SMA route

## 6. E22 interface

- E22 VCC pins connected directly to regulated 5 V
- no load switch and no eFuse
- NRST, BUSY and DIO1 route directly to assigned XIAO pins
- DIO3 remains the module TCXO control function used by the SX1262 driver
- E22 DIO2 connects directly to E22 TXEN
- TXEN is active high and is driven by the SX1262 DIO2 RF-switch function, not by a XIAO GPIO
- RXEN is active high and is controlled by XIAO D6
- firmware must enable the SX1262 DIO2 RF-switch function and must not define a separate MCU TXEN pin

### Final XIAO GPIO map

| XIAO pin | nRF52840 GPIO | Function |
|---|---|---|
| D0 | P0.02 | E22 NRST |
| D1 | P0.03 | E22 DIO1 |
| D2 | P0.28 | E22 BUSY |
| D3 | P0.29 | E22 NSS / SPI chip select |
| D4 | P0.04 | I2C SDA, BQ25798 |
| D5 | P0.05 | I2C SCL, BQ25798 |
| D6 | P1.11 | E22 RXEN |
| D7 | P1.12 | TPS61088 EN |
| D8 | P1.13 | E22 SPI SCK |
| D9 | P1.14 | E22 SPI MISO |
| D10 | P1.15 | E22 SPI MOSI |

All eleven exposed XIAO GPIOs are allocated. BQ25798 INT is not routed to the XIAO; charger status/faults are polled over I2C.

### MeshCore/RadioLib integration requirements

The custom RoyalNode variant must use the XIAO nRF52840 SPI0 pins D8/D9/D10, define D3 as chip-select, D0 as reset, D2 as BUSY, D1 as DIO1, D6 as RXEN, and enable the SX1262 DIO2 RF-switch function for TXEN. TPS61088 D7 enable is handled by RoyalNode board startup/power-management code before radio initialization.

## 7. Battery telemetry

Rev A does not include the previously considered MAX17048 fuel gauge. The BQ25798 ADC and status registers are the sole carrier-board source of battery and charger telemetry.

Firmware may report:

- battery voltage
- charger state
- charge-current measurement available from the BQ25798 ADC/status interface
- input/solar voltage and input-current measurements when enabled
- charger fault/status information

Rev A does not claim an accurate battery state-of-charge percentage. Any user-interface battery indication derived only from voltage must be clearly identified as an estimate rather than fuel-gauge SOC.

## 8. Charge LED

- one external charge/status LED only
- BQ25798 STAT drives the LED directly using its open-drain output; no buffer transistor is used
- topology: 3.3 V -> LED -> RLED -> STAT
- no separate STAT pull-up is required for the LED path
- charging: LED on
- charge complete / charging disabled / battery-only operation: LED off
- charger fault or charge suspend indication follows the BQ25798 STAT blink behavior
- target LED current is approximately 0.5-1 mA to minimize repeater power consumption
- exact RLED value is selected after the exact LED part and its forward-voltage range are chosen
- no full, fault or carrier system LEDs

## 9. RF path

- E22 ANT to board-edge SMA through a short 50-ohm controlled-impedance route
- solid ground reference directly below
- ground-via fence along route
- no digital or switching power route crossing RF keepout
- final RF geometry depends on fabricator stack-up

## 10. PCB stack-up

Recommended four-layer arrangement:

1. Top: components, RF and critical power loops
2. Inner 1: uninterrupted ground plane
3. Inner 2: power distribution and low-speed signals
4. Bottom: low-speed routing and ground copper

Keep the BQ25798 and TPS61088 hot loops compact. Place TPS61088 and its inductor away from the E22/SMA end.

## 11. Automatic startup

There is no power button. Connecting the protected battery powers the XIAO. The XIAO then intentionally enables the TPS61088 radio rail on D7 after startup. The battery XT30 is the master disconnect.

## 12. KiCad entry criteria

Remaining implementation tasks:

- verify exact footprints against manufacturer drawings
- select specific capacitor and LED manufacturer numbers after DC-bias/forward-voltage review
- reproduce TI reference-layout constraints
- run ERC after schematic capture
- perform schematic-level compatibility review before PCB layout
