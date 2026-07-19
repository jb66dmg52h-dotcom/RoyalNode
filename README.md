# 2Watt Project

The 2Watt Project is a rugged, solar-powered 915 MHz LoRa repeater platform built around the Seeed XIAO nRF52840 and EBYTE E22-900M33S high-power radio module.

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
- XIAO USB-C for firmware updates, external power and battery charging
- BQ25798 buck-boost charger with MPPT, power path and dual-source support
- TPS61088 synchronous boost converter generating 5.0 V for the radio
- Dedicated regulated 5.0 V / 3 A radio rail
- Separate protected XIAO supply path
- MAX17048 single-cell fuel gauge
- XIAO onboard charger isolated by leaving BAT unconnected
- Low-temperature charge protection through battery NTC
- Push-button power control
- Charging and system-status LEDs
- Direct 50-ohm PCB RF path from the E22 ANT pin to a board-edge SMA connector
- Surface-mount JST-PH 2.0 service connector for SWD programming

A 1S pack operates from approximately 3.0 V to 4.2 V. At full radio load, the 5 V boost stage may draw roughly 2.0–2.6 A from the battery, so the pack, XT30 connection, fuse, copper and protection circuit must be designed for at least 5 A continuous capability with additional transient margin.

## Recommended deployment panel envelope

The project should not require one specific panel SKU. Deployment documentation should recommend a compatible panel envelope, for example:

- 12 V nominal monocrystalline panel
- approximately 10–20 W depending on site and battery reserve goals
- Vmp typically in the mid-to-high teens
- Voc comfortably below the charger input limit, including cold-weather rise
- XT30 cable connection

The installer must check the selected panel's Vmp, Voc, Imp and cold-weather Voc against the charger limits.

## Repository layout

```text
2Watt-Project/
├── docs/              Engineering specifications and calculations
├── hardware/          KiCad project, symbols, footprints and fabrication files
├── firmware/          Board support and hardware test firmware
├── bom/               Manufacturing and sourcing files
├── enclosure/         Mechanical and environmental design
├── production/        Assembly and manufacturing outputs
└── test/              Bring-up procedures and measurements
```

## Major project risks

1. Implementing MeshCore support for the module's external PA, RF switching and TCXO behavior.
2. Validating the TPS61088 5 V rail under repeated full-power transmission from a nearly discharged 1S pack.
3. Completing and validating the BQ25798 dual-input solar/USB reference design.
4. Selecting a low-quiescent-current XIAO supply path that cannot backfeed USB.
5. Mechanically supporting the board-mounted XT30 and SMA connectors so insertion force is not carried only by solder joints.
6. Configuring the XIAO NFC pads as GPIO for extra control signals.
7. Regulatory assessment for operation in Canada's 902–928 MHz band.

## Revision plan

- **Rev A:** Deployment-focused engineering-validation carrier using 1S power architecture.
- **Rev B:** Field deployment board after power, firmware and thermal validation.
- **Rev C:** Production-oriented release after environmental and regulatory review.

## Safety and regulatory note

The radio hardware may be capable of approximately 33 dBm output. Deployed settings must comply with applicable conducted-power, antenna-gain, EIRP, bandwidth and certification requirements. Lithium battery packs must include appropriate protection, fusing and temperature monitoring.
