# RoyalNode Rev A Requirements

## 1. Mission

RoyalNode Rev A is an engineering-validation platform for a rugged, solar-powered 915 MHz LoRa repeater using a Seeed XIAO nRF52840 and an EBYTE E22-900M33S radio module.

## 2. Functional requirements

- Operate as a continuously available LoRa repeater.
- Support the E22-900M33S SPI interface and external RF-control behavior.
- Expose sufficient test points for bench validation of every critical power and radio signal.
- Support firmware-controlled radio power, reset and receive/transmit control.
- Provide battery, solar-input and radio-rail telemetry.
- Permit safe reduced-power operation when battery charge or temperature is outside preferred limits.

## 3. Power requirements

- Primary energy source: 6 V class, 20 W monocrystalline panel.
- Energy storage: 2S protected Li-ion battery, 15 Ah target.
- **Standard power connector: XT60 for both battery and solar interfaces.**
- XT60-equivalent locking connectors may be used only if they meet or exceed XT60 current capability, contact reliability and environmental sealing.
- PCB-mounted XT60 connectors are preferred where enclosure space permits; otherwise use panel-mounted XT60 connectors with short 16–18 AWG pigtails.
- All external power wiring shall be 16–18 AWG silicone wire.
- Remaining requirements unchanged from Rev A.