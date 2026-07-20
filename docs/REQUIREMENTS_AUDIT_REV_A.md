# 2Watt Project Requirements Audit, Rev A

## Status

Requirements frozen for KiCad schematic capture. `DESIGN_FREEZE_REV_A.md` is the primary source of truth.

## Fixed product requirements

### Radio and firmware

- EBYTE E22-900M33S radio module
- Standard Seeed Studio XIAO nRF52840 controller
- MeshCore repeater target
- Native USB-C firmware updates through the XIAO
- Radio signals: NSS, SCK, MOSI, MISO, BUSY, DIO1, NRST, TXEN and RXEN
- Correct E22 TCXO and external RF-switch control in firmware

### RF

- Direct E22 ANT to board-mounted SMA connection
- No u.FL intermediate connector
- Controlled 50-ohm route based on the final fabricator stack-up
- Continuous ground reference and switching-node separation

### Battery and charging

- Protected 1S flat LiPo
- 10 Ah capacity target
- At least 5 A continuous discharge capability
- At least 2 A permitted charge current
- Board-mounted XT30 battery connector
- Board-mounted XT30 solar connector
- 12 V nominal solar panel class
- 10 W panel supported; 20 W recommended
- USB-C charging through BQ25798
- Solar MPPT and power-path operation
- Maximum programmed charge current: 2.0 A
- Battery voltage and state-of-charge telemetry through MAX17048
- No battery-temperature monitoring
- Battery pack must include internal over-charge, over-discharge, over-current and short-circuit protection

### XIAO power and service

- XIAO remains socketed on its edge pins
- Carrier powers XIAO through underside BAT and GND pads only
- Short two-wire lead terminates in a keyed 2-pin JST-PH connector beside the XIAO socket
- LM66100 ideal diode prevents reverse current into the main battery rail
- Carrier does not drive XIAO 5V/VBUS
- No pogo pins, SWD connector or multi-wire underside harness
- Normal firmware and recovery use XIAO USB-C and onboard reset

### User interface

- One external charge LED only
- No power button
- Automatic startup when the protected battery is connected
- Battery XT30 serves as the master disconnect

### Mechanical and manufacturing

- Board-only design; enclosure design is outside Rev A scope
- First prototype quantity: five boards
- Four-layer controlled-impedance PCB
- Factory assembly for all pick-and-place-compatible components
- Socket headers, XIAO power lead and any unsuitable mechanical connectors may be hand-installed
- XT30 and SMA footprints must tolerate or transfer connector insertion force appropriately

## Electrical performance requirements

### 5 V radio rail

- Nominal output: 5.0 V
- Continuous design target: 2 A
- Transient design target: 3 A
- E22 connected directly to 5 V with no load switch or eFuse
- TPS61088 soft-start, current limit and local bulk capacitance must prevent rail collapse
- TXEN and RXEN default low during reset

### Battery path

- Copper, vias and connector path sized for at least 5 A continuous
- Full-power operation may be reduced near low battery voltage in firmware

### Charger

- TI BQ25798RQMR
- 1S startup configuration
- 750 kHz switching frequency
- 2.2 uH charger inductor
- /CE tied low for autonomous charging
- TS biased to the normal region using a fixed divider
- Charger telemetry polled over I2C

## Removed functionality

- Power button and latch controller
- Radio load switch
- eFuse
- Battery thermistor and NTC connector
- Full, fault and carrier status LEDs
- SWD connector
- Pogo contacts
- Eight-wire XIAO harness
- Solar-present and USB-present telemetry
- Radio-disable jumper
- Battery reverse-polarity circuit
- GPS, display and environmental sensors

## Resolved compatibility issues

### XIAO USB backfeed

Resolved by powering the XIAO through BAT/GND via LM66100. The carrier never drives XIAO VBUS.

### XIAO GPIO count

All eleven edge GPIOs are allocated to the E22 and shared I2C bus. No additional GPIO-dependent features remain.

### Radio surge

Resolved by the oversized TPS61088 stage, high-current inductor, controlled soft-start and 330-470 uF local E22 bulk capacitance.

### Solar panel flexibility

Resolved with a deployment envelope rather than a fixed panel SKU: 12 V nominal, 10 W supported, 20 W recommended.

## Remaining implementation work

No architecture-level decisions block KiCad. Remaining tasks are implementation and verification:

1. Verify symbols and footprints against manufacturer drawings.
2. Select exact capacitor MPNs after effective-capacitance and assembler-stock review.
3. Capture the schematic and run ERC.
4. Perform a schematic-level compatibility audit.
5. Obtain the PCB fabricator stack-up and calculate the RF geometry.
6. Place, route and run DRC.

## Audit verdict

The frozen Rev A requirements are coherent and suitable for KiCad schematic capture. Prototype testing remains required for charging behavior, USB source handling, converter temperature, 5 V transient response and RF noise.
