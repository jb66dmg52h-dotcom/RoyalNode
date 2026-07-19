# RoyalNode

RoyalNode is a rugged, solar-powered 915 MHz LoRa repeater platform built around the Seeed XIAO nRF52840 and EBYTE E22-900M33S high-power radio module.

> **Status:** Rev A architecture and engineering validation

## Primary goals

- Outdoor, unattended repeater operation
- EBYTE E22-900M33S support up to its 33 dBm hardware capability
- Seeed XIAO nRF52840 controller
- Solar charging with multi-day battery reserve
- Dedicated, oversized radio power rail
- Canadian climate considerations
- Serviceable Rev A hardware
- MeshCore board support, subject to firmware integration work

## Current proposed architecture

- Solar input designed around a recommended 12 V nominal panel class rather than one mandatory panel model
- Protected 1S flat LiPo battery pack
- Board-mounted XT30 connector for solar input
- Board-mounted XT30 connector for battery input
- USB-C for firmware updates, external power and battery charging
- BQ24650 standalone solar MPPT buck charger
- TPS61088 synchronous boost converter generating 5.0 V for the radio
- Dedicated regulated 5.0 V / 3 A radio rail
- Separate low-noise XIAO rail
- MAX17048 single-cell fuel gauge, with direct ADC voltage reading as a fallback
- Low-temperature charge protection through battery NTC
- Push-button power control
- Charging and system-status LEDs
- Direct 50-ohm PCB RF path from the E22 ANT pin to a board-edge SMA connector

A 1S pack operates from approximately 3.0 V to 4.2 V. At full radio load, the 5 V boost stage may draw roughly 2.0–2.6 A from the battery, so the pack, XT30 connection, fuse, copper and protection circuit must be designed for at least 5 A continuous capability with additional transient margin.

## Recommended deployment panel envelope

RoyalNode should not require one specific panel SKU. Deployment documentation should recommend a compatible panel envelope, for example:

- 12 V nominal monocrystalline panel
- approximately 10–20 W depending on site and battery reserve goals
- Vmp typically in the mid-to-high teens
- Voc comfortably below the charger input limit, including cold-weather rise
- XT30 cable connection

The final installer is responsible for checking the selected panel's Vmp, Voc, Imp and cold-weather Voc against the charger limits.

## Repository layout

```text
RoyalNode/
├── docs/              Engineering specifications and calculations
├── hardware/          KiCad project, symbols, footprints and fabrication files
├── firmware/          Board support and hardware test firmware
├── bom/               Manufacturing and sourcing files
├── enclosure/         Mechanical and environmental design
├── production/        Assembly and manufacturing outputs
└── test/              Bring-up procedures and measurements
```

## Major project risks

1. Confirming the exact E22-900M33S electrical interface and RF-control requirements.
2. Implementing MeshCore support for the module's external PA, RF switching and TCXO behavior.
3. Validating the TPS61088 5 V rail under repeated full-power transmission from a nearly discharged 1S pack.
4. Defining a safe and useful 12 V nominal solar-panel compatibility envelope for deployment documentation.
5. Preventing the XIAO onboard 50/100 mA charger from conflicting with the main solar/USB charging system.
6. Mechanically supporting the board-mounted XT30 and SMA connectors so insertion force is not carried only by solder joints.
7. Regulatory assessment for operation in Canada's 902–928 MHz band.

## Revision plan

- **Rev A:** Deployment-focused engineering-validation carrier using 1S power architecture.
- **Rev B:** Field deployment board after power, firmware and thermal validation.
- **Rev C:** Production-oriented release after environmental and regulatory review.

## Safety and regulatory note

The radio hardware may be capable of approximately 33 dBm output. Deployed settings must comply with applicable conducted-power, antenna-gain, EIRP, bandwidth and certification requirements. Lithium battery packs must include appropriate protection, fusing and temperature monitoring.
