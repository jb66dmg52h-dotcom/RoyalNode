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
- Serviceable and testable Rev A hardware
- MeshCore board support, subject to firmware integration work

## Current proposed power architecture

- 6 V nominal, 20 W monocrystalline solar panel
- True-MPPT buck-boost multi-cell charger
- 2S 15 Ah protected Li-ion battery
- Dedicated regulated 5.0 V / 3 A radio rail
- Separate low-noise XIAO rail
- Battery, solar and radio-current telemetry
- Low-temperature charge protection

A 6 V / 20 W panel produces about 3.3 A at rated power. This matches the practical input-current ceiling of the current BQ25798 charger candidate. Panels above 20 W at 6 V require a different higher-current charger front end or multiple charger channels.

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
3. Validating the high-current 5 V radio rail under repeated full-power transmission.
4. Finalizing a charger architecture that safely supports a 6 V panel, 2S batteries, solar MPPT and cold-weather charging.
5. Regulatory assessment for operation in Canada's 902–928 MHz band.

## Revision plan

- **Rev A:** Engineering validation carrier with extensive test points and configurable routing.
- **Rev B:** Field deployment board after power, firmware and thermal validation.
- **Rev C:** Production-oriented release after environmental and regulatory review.

## Safety and regulatory note

The radio hardware may be capable of approximately 33 dBm output. Deployed settings must comply with applicable conducted-power, antenna-gain, EIRP, bandwidth and certification requirements. Lithium battery packs must include appropriate protection, fusing and temperature monitoring.
