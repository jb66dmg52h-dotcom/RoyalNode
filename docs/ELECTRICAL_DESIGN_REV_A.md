# 2Watt Project Electrical Design, Rev A

## Status

Locked for KiCad schematic capture. Battery physical packaging and enclosure design are outside this scope.

## System architecture

```text
SOLAR XT30
  -> 2 A fuse
  -> reverse-polarity P-FET
  -> 22 V TVS
  -> BQ25798 solar input

XIAO USB-C VBUS
  -> protected/current-limited branch
  -> BQ25798 USB input

PROTECTED 1S LIPO
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

### Locked parts

- J1: board-mounted AMASS XT30PW
- F1: Littelfuse 0483002.DR, 2 A, 75 V, 1206 fast-acting fuse
- Q1: Infineon BSL303SPE, P-channel -30 V MOSFET
- D1: Littelfuse SMBJ22A, unidirectional 22 V standoff TVS

### Supported panel class

- 12 V nominal
- 10 W supported
- 20 W recommended
- recommended deployment Voc at or below 24 V including cold-weather rise
- final silkscreen input limit to be confirmed during schematic review

## 2. Main charger and power path

### Charger

- U1: TI BQ25798RQMR
- cell count: 1S
- maximum programmed charge current: 2.0 A
- autonomous default charge current remains at the device default until firmware configures 2.0 A
- switching frequency: 750 kHz
- inductor: Coilcraft XAL7070-222MEC, 2.2 uH

### Startup configuration

- PROG: 4.7 kOhm, 1%, to GND for 1S default configuration
- /CE: tied low
- TS: equal 10 kOhm divider from REGN to GND, placing TS at 50% REGN
- D+ and D- on BQ25798: no connection
- SDA/SCL: shared 3.3 V I2C bus to XIAO D4/D5
- charger status: one hardware charge LED
- charger telemetry: polled over I2C

### Initial capacitor targets

- VBUS: 2 x 10 uF, 35 V, X7R plus 100 nF
- PMID: 2 x 10 uF, 35 V, X7R
- SYS: 4 x 22 uF, 10 V, X7R plus 100 uF bulk footprint
- BAT: 2 x 22 uF, 10 V, X7R
- REGN and SDRV parts: follow the latest TI reference schematic exactly

Selected capacitors must meet the required effective capacitance after DC-bias derating.

## 3. Battery interface

- J2: board-mounted AMASS XT30PW
- protected 1S flat LiPo
- capacity target: 10 Ah
- maximum voltage: 4.20 V
- design minimum input: 3.0 V
- discharge capability: at least 5 A continuous, 8 A transient preferred
- permitted charge current: at least 2 A
- no battery thermistor
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

The LM66100 blocks reverse current from the XIAO onboard charger into the main battery rail while adding very little voltage drop.

### Mechanical arrangement

- XIAO edge pins plug into socket headers
- short flexible power wires are soldered to XIAO BAT and GND underside pads
- disconnect the 2-pin JST before removing the XIAO
- no pogo contacts, SWD connector or multi-wire harness

## 5. TPS61088 5 V rail

### Locked parts and values

- U3: TI TPS61088RHLR
- inductor: Coilcraft XAL7030-222MEC, 2.2 uH
- output target: approximately 5.0 V
- continuous target: 2 A
- transient target: 3 A
- feedback: 178 kOhm top and 56 kOhm bottom, 1%
- frequency resistor: 300 kOhm, 1%, approximately 500 kHz starting point
- current-limit resistor: 140 kOhm, 1%
- soft-start capacitor: 10 nF
- EN: pulled high for automatic startup
- MODE: configurable footprint for PFM versus forced PWM testing

### Input capacitors

- 2 x 22 uF, 10 V, X7R
- 100 uF low-ESR bulk
- 100 nF local bypass
- 4.7 uF VCC bypass

### Output and E22 capacitors

Near TPS61088:

- 3 x 22 uF, 10 V, X7R

Near E22:

- 2 x 22 uF, 10 V, X7R
- 1 uF ceramic
- multiple 100 nF ceramics
- 330-470 uF low-ESR bulk

## 6. E22 interface

- E22 VCC pins connected directly to regulated 5 V
- no load switch and no eFuse
- TXEN and RXEN each receive pull-down resistors
- NRST, BUSY and DIO1 route directly to assigned XIAO pins
- DIO3 is reserved for the module TCXO function
- firmware must configure the TCXO and TX/RX switching correctly

### XIAO GPIO map

| XIAO | Function |
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

## 7. Fuel gauge

- U4: ADI MAX17048G+T10
- connected to protected 1S battery node
- shares I2C with BQ25798
- no alert pin required; firmware polls voltage and SOC
- place away from TPS61088 and charger switching loops

## 8. Charge LED

- one external charge LED only
- driven from BQ25798 status output
- LED current target: approximately 0.5-1 mA
- no full, fault or carrier system LEDs

## 9. RF path

- E22 ANT to board-edge SMA through a short 50-ohm controlled-impedance route
- include a 0-ohm series link and optional unpopulated pi tuning footprint
- solid ground reference directly below
- ground-via fence along route
- no digital or switching power route crossing RF keepout
- connector candidate: Molex 0732512440
- final RF geometry depends on fabricator stack-up

## 10. PCB stack-up

Recommended four-layer arrangement:

1. Top: components, RF and critical power loops
2. Inner 1: uninterrupted ground plane
3. Inner 2: power distribution and low-speed signals
4. Bottom: low-speed routing and ground copper

Keep the BQ25798 and TPS61088 hot loops compact. Place TPS61088 and its inductor away from the E22/SMA end.

## 11. Automatic startup

There is no power button. Connecting the protected battery powers the XIAO and enables TPS61088 automatically. The battery XT30 is the master disconnect.

## 12. KiCad entry criteria

All architecture-level choices are frozen. KiCad work may begin with these remaining implementation tasks:

- verify exact footprints against manufacturer drawings
- select specific capacitor manufacturer numbers after DC-bias review
- reproduce TI reference-layout constraints
- run ERC after schematic capture
- perform a schematic-level compatibility review before PCB layout
