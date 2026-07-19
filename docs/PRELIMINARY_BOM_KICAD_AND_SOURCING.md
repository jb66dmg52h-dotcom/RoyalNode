# 2Watt Project Preliminary BOM, KiCad and Sourcing Review

## Purpose

This is a Rev A engineering BOM, not an order-ready production BOM. Exact passive values and some protection/power-control parts remain subject to TI reference-design calculations, battery selection and PCB stack-up.

## Core parts

| Ref | Function | Preferred part | Package / form | Qty | Status |
|---|---|---|---|---:|---|
| U1 | MCU module | Seeed Studio XIAO nRF52840, standard | 21 x 17.8 mm module | 1 | Selected |
| U2 | 2 W LoRa radio | EBYTE E22-900M33S | 38.5 x 24 mm castellated module | 1 | Selected |
| U3 | Solar + USB charger and power path | TI BQ25798RQMR | 29-pin 4 x 4 mm VQFN-HR | 1 | Selected for Rev A |
| U4 | 1S-to-5 V radio boost | TI TPS61088RHLR | 20-pin 4.5 x 3.5 mm VQFN | 1 | Selected |
| U5 | Battery fuel gauge | ADI MAX17048G+T10 | 8-TDFN-EP 2 x 2 mm | 1 | Selected |
| U6 | Radio rail load disconnect | TBD eFuse/load switch | High-current SMD | 1 | Open |
| U7 | XIAO supply path | TBD low-Iq converter/power mux | SMD | 1-2 | Open |
| U8 | Push-button controller | TBD latch/controller | SMD | 1 | Open |

## Connectors and controls

| Ref | Function | Preferred class / candidate | Qty | Status |
|---|---|---|---:|---|
| J1 | Solar input | Board-mounted AMASS XT30, keyed/oriented for solar | 1 | Exact MPN open |
| J2 | Battery input | Board-mounted AMASS XT30, different gender/orientation | 1 | Exact MPN open |
| J3 | RF output | Board-edge 50-ohm SMA female; Molex 0732512440 is a sourcing candidate | 1 | Candidate |
| J4 | SWD service | JST-PH 2.0 mm, 4-pin SMT, side-entry preferred | 1 | Exact MPN open |
| SW1 | User power button | Sealed or enclosure-actuated momentary switch | 1 | Mechanical selection open |
| LED1 | Charging | Low-current LED from charger status logic | 1 | Generic |
| LED2 | Full/standby | Low-current LED from charger status logic | 1 | Generic |

## Charger power-stage support parts

BQ25798 integrates the main four-switch buck-boost power stage and battery FET, but still requires external parts. Final choices must follow the latest TI datasheet/EVM design.

- charger inductor, value/current rating per 1S 2-3 A target
- input capacitors rated for at least the selected solar maximum and transient margin
- system and battery ceramic/bulk capacitors
- thermistor network matched to the battery NTC
- solar input TVS
- solar input fuse or resettable fuse
- reverse-polarity/input blocking FET arrangement
- dual-input selector FETs if the optional selector is implemented
- I2C pull-ups to 3.3 V
- charger interrupt/status pull-ups and LED resistors

## TPS61088 support parts

- approximately 1 uH shielded power inductor, final Isat/DCR from TI calculation
- input ceramics plus low-ESR bulk capacitor near the converter
- output ceramics plus low-ESR bulk capacitor near E22 VCC pins
- feedback divider for 5.0 V
- switching-frequency resistor
- current-limit resistor
- soft-start capacitor
- compensation/layout parts per datasheet
- output load-disconnect/eFuse stage
- optional snubber footprint for EMI tuning

## RF and layout parts

- 0-ohm RF link or tuning footprint between E22 ANT and SMA
- optional unpopulated pi-matching footprints for RF tuning
- dense ground-via fence along the RF trace
- ESD protection only if a suitably low-capacitance RF device is selected and validated at 915 MHz
- 4-layer controlled-impedance FR-4 recommended

## KiCad library availability

| Part | Symbol availability | Footprint availability | Action |
|---|---|---|---|
| XIAO nRF52840 | Official Seeed symbol available | Official Seeed footprint and KiCad project available | Import Seeed library and verify bottom-pad mapping |
| E22-900M33S | Not expected in stock KiCad library | Custom castellated footprint required; EasyEDA/JLC model exists | Create and independently verify against EBYTE drawing |
| BQ25798RQMR | Not confirmed in stock KiCad library | Generic/custom 29-pin VQFN-HR footprint likely required | Import vendor ECAD or build from TI package drawing |
| TPS61088RHLR | Not confirmed in stock KiCad library | Generic 20-pin VQFN package can be adapted | Build/verify thermal pad and paste pattern from TI drawing |
| MAX17048G+T10 | May not be in stock library | Generic 2 x 2 mm 8-TDFN-EP footprint available or adaptable | Verify exposed pad and pin-1 orientation |
| XT30 PCB connector | AMASS connector footprints may exist depending on KiCad version | Exact board-mount variant must match selected MPN | Do not use a generic XT30 footprint without mechanical check |
| JST-PH 4-pin SMT | Generic symbol available | Official KiCad JST-PH footprints generally available | Select exact side/top-entry MPN first |
| Board-edge SMA | Generic connector symbol available | Several KiCad coax footprints exist, but exact launch geometry is stack-up specific | Build or modify footprint from connector datasheet |

## Current supplier check

Inventory changes constantly; these observations are a snapshot from July 2026.

- E22-900M33S: listed in JLCPCB's parts library as an extended part and available for SMT assembly.
- TPS61088RHLR: available from DigiKey Canada and Mouser Canada.
- BQ25798RQMR: available from Mouser Canada; also an active TI part.
- MAX17048G+T10: available from DigiKey Canada.
- XIAO nRF52840 standard: available as a Seeed 3-pack through DigiKey Canada.
- Board-edge SMA: Molex 0732512440 is currently stocked by DigiKey Canada and has vendor ECAD models.

## PCB manufacturer fit

### JLCPCB

Good fit for Rev A if the design uses standard assembly or a mixed strategy.

- E22-900M33S is already in the JLCPCB parts library.
- Standard PCBA supports single- or double-sided SMT/THT and fine-pitch parts.
- Controlled impedance is available on multilayer boards.
- XIAO, XT30 and SMA may be hand-installed or consigned if not machine-friendly/in-library.

Recommended JLC strategy:

1. JLC assembles BQ25798, TPS61088, MAX17048 and small passives.
2. JLC assembles the E22 if inventory remains available.
3. Hand-solder or consign the XIAO, XT30 connectors and SMA for the first five boards.

### PCBWay

Also a good fit, especially when consigned or mixed-source parts are needed.

- supports SMT, THT and mixed assembly
- supports turnkey, consigned and partial-turnkey sourcing
- can source from authorized distributors with approval
- useful if exact XT30/SMA/XIAO parts are difficult to match in JLC's library

## Recommended Rev A manufacturing route

Use a 4-layer impedance-controlled PCB with ENIG. Order five assembled boards with all fine-pitch/QFN and small SMD parts factory assembled. Keep the XIAO, XT30, SMA and possibly E22 as hand-soldered or consigned parts until their footprints and mechanical fit have been physically verified.

## Parts not ready to purchase

Do not order these until schematic calculations are complete:

- charger inductor and surrounding BQ25798 power-stage passives
- TPS61088 inductor/current-limit/frequency/soft-start parts
- radio rail eFuse/load disconnect
- XIAO supply converter/power mux
- power-button controller
- input TVS/fuse/reverse-protection parts
- exact XT30 and JST-PH connector variants
- battery pack and NTC
