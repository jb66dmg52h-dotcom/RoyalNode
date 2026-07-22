# 2Watt Project

The 2Watt Project is a solar-powered 915 MHz LoRa repeater carrier built around the Seeed Studio XIAO nRF52840 and EBYTE E22-900M33S high-power radio module.

> **Status:** Rev A design frozen for KiCad schematic capture

## Locked architecture

- Standard Seeed Studio XIAO nRF52840, socketed
- EBYTE E22-900M33S radio module
- Protected 1S 3.6/3.7 V Li-ion/LiPo pack, 10-20 Ah class
- Board-mounted XT30 battery connector
- Board-mounted XT30 solar connector
- BQ25798 buck-boost charger with MPPT and power path
- Battery-mounted Semitec 103AT-2 NTC connected to BQ25798 TS network
- TPS61088 5 V boost rail for the E22
- Battery voltage and charger telemetry read directly from the BQ25798
- XIAO powered through its underside BAT and GND pads using a two-wire JST-PH lead
- LM66100 ideal diode between the main battery/system node and the XIAO BAT lead
- USB-C firmware updates through the XIAO
- USB-C battery charging through the BQ25798
- One external charge LED
- Direct controlled-impedance RF path from E22 ANT to board-edge SMA
- XIAO-controlled TPS61088 enable for radio power sequencing
- 4-layer controlled-impedance PCB

## Solar guidance

- 12 V nominal panel class
- 10 W supported
- 20 W recommended for permanent deployment
- Installer must verify Vmp, Voc, Imp and cold-weather Voc

## Removed from Rev A

- MAX17048 fuel gauge and battery percentage estimation
- Power button
- eFuse
- Radio load switch
- Pogo pins
- SWD connector
- Multi-wire XIAO harness
- Extra LEDs beyond the charge LED
- Solar/USB-present telemetry
- Battery reverse-polarity circuit
- Radio-disable jumper
- Display, GPS and environmental sensors
- Bench-test jumpers, simulated-temperature bypass networks and mode-selection test footprints

## Power summary

- Battery: protected 1S 3.6/3.7 V nominal, 4.20 V maximum, 10-20 Ah class
- Battery discharge capability: at least 5 A continuous, 8 A transient preferred
- Maximum charge current: 2 A
- Charge temperature sensing: battery-mounted 10 kOhm NTC; target policy suspends charging below 0 C and at/above 45 C
- Battery telemetry: BQ25798 battery voltage and charger-state measurements; no dedicated SOC fuel gauge in Rev A
- E22 rail: 5.0 V nominal
- TPS61088 rail design target: 2 A continuous
- TPS61088 inductor: Coilcraft XAL7030-222MEC, 2.2 uH
- BQ25798 inductor: Coilcraft XAL7070-222MEC, 2.2 uH
- E22 local bulk capacitance: 330-470 uF plus ceramics

## Canonical documents

- `docs/DESIGN_FREEZE_REV_A.md`
- `docs/WIRING_BLUEPRINT.md`
- `docs/ELECTRICAL_DESIGN_REV_A.md`
- `docs/LOCKED_COMPONENTS_REV_A.md`
- `docs/FINAL_POWER_CALCULATIONS_REV_A.md`
- `docs/SOLAR_DESIGN_GUIDE_REV_A.md`

Earlier concept documents are superseded where they conflict with the design-freeze document.

## Repository layout

```text
2Watt-Project/
├── docs/              Engineering specifications and calculations
├── hardware/          KiCad project, symbols, footprints and fabrication files
├── firmware/          Board support and hardware test firmware
├── bom/               Manufacturing and sourcing files
├── production/        Assembly and manufacturing outputs
└── test/              Bring-up procedures and measurements
```

## Remaining work

1. Create or import verified KiCad symbols and footprints.
2. Capture the Rev A schematic.
3. Run ERC and a schematic-level compatibility audit.
4. Obtain the fabricator's 4-layer stack-up and calculate the 50-ohm RF geometry.
5. Place and route the PCB.
6. Run DRC and manufacturing review.
7. Order Rev A prototypes for production validation.

## Safety and regulatory note

The radio hardware may be capable of approximately 33 dBm output. Deployed settings must comply with applicable conducted-power, antenna-gain, EIRP, bandwidth and certification requirements. The battery pack must include suitable internal protection, and deployment must respect the battery manufacturer's permitted charging-temperature range.
