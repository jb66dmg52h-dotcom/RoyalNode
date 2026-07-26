# RoyalNode Rev A System Architecture

## Proposed block diagram

```text
6 V / 20 W solar panel
          |
  XT30, fuse, reverse protection,
  TVS and input filtering
          |
  BQ25798 1S solar/USB charger
          |
  1S 15 Ah protected Li-ion battery
          |
      XT30 + main fuse
          |
          +-------------------------------+
          |                               |
 TPS61088 5.0 V radio boost       low-noise MCU supply
          |                               |
 EBYTE E22-900M33S                Seeed XIAO nRF52840
          |                               |
 50-ohm PCB trace to SMA          optional 4-pin JST-GH
                                  BME680 environmental
```

## Major subsystems

### Solar and charger subsystem

RoyalNode uses a one-cell charger architecture around the BQ25798RQMR charger and power-path controller.

The locked Rev A charger is BQ25798RQMR configured for one Li-ion cell. It provides the charger, power-path behavior, I2C configuration, charger telemetry and input-source handling used by the current KiCad schematic.

For a 6 V nominal panel, firmware and charger configuration must be validated against the actual panel maximum-power voltage/current rather than the printed nominal voltage alone.

Initial charging target:

- 1S Li-ion charge voltage: 4.20 V
- maximum charge current: approximately 2.0–2.5 A
- panel maximum-power current: approximately 3.3 A
- battery NTC charge-temperature protection enabled

### Battery subsystem

Target pack: protected 1S 15 Ah lithium-ion pack with a pack-mounted NTC.

The pack no longer needs cell balancing because all parallel cells operate as one series group. It still requires:

- over-charge protection
- over-discharge protection
- over-current and short-circuit protection
- at least 5 A continuous discharge capability
- transient capability above 5 A
- a main fuse near the XT30 connection

At a 6 W radio load and approximately 85–90% boost efficiency, the battery may supply roughly 1.6 A at 4.2 V and approximately 2.2–2.6 A near the low end of the allowed battery range. Copper, fuse, protection FETs and wiring are sized with substantial margin.

### Radio power subsystem

TPS61088 remains the preferred converter. It is suitable for single-cell lithium input and provides the switch-current capability required to create a stiff 5.0 V radio rail.

Required design targets:

- input range: approximately 3.0–4.2 V
- output: 5.0 V
- continuous output design target: 3 A
- programmed soft start
- controlled enable from the XIAO
- low-ESR local bulk and ceramic capacitance at the EBYTE supply
- hardware protection against abnormal output over-voltage

No current-shunt footprints, dedicated test pads or measurement links are included.

### MCU subsystem

The Seeed XIAO nRF52840 remains socketed on Rev A. It handles the SPI radio interface, boost enable and radio sequencing, battery telemetry, optional environmental telemetry, fault logging and the MeshCore hardware abstraction layer.

The XIAO must not use its onboard battery charger as the system charger. The BQ25798 charger path is the controlled battery-charging path. Programming uses the XIAO USB-C port; recovery uses SWD pads or Tag-Connect.

### Battery telemetry

Rev A omits a dedicated MAX17048 fuel gauge. Battery voltage and charger state are read from the BQ25798 over I2C. Firmware may later add an ADC cross-check if needed, but it is not part of the current KiCad capture.

### Radio and RF subsystem

The EBYTE E22-900M33S contains an SX1262-family transceiver and external high-power RF front end. Integration requires validated control of reset, BUSY, DIO1, RXEN, TXEN or DIO2 RF-switch control, and DIO3 TCXO behavior.

The board-mounted SMA is connected to EBYTE ANT pin 21 through a short 50-ohm controlled-impedance grounded coplanar waveguide. The module's alternate U.FL/I-PEX path must not be used simultaneously.

## MeshCore telemetry architecture

### Required

- battery voltage or state of charge
- MCU internal temperature where supported

### Optional

- BME680 temperature, humidity and pressure over one 4-pin JST-GH I2C connector

### Omitted

- solar current telemetry
- radio current telemetry
- battery current telemetry
- external PA or regulator temperature telemetry
- fan sensing or control
- generic accessory ports
- GPS hardware for a fixed repeater

## Parts changed by the 2S-to-1S conversion

### Removed or replaced

- 2S charger configuration: replaced by 1S BQ25798 configuration
- 2S 15 Ah battery pack: replaced by protected 1S 15 Ah pack
- 2S BMS and balancing function: replaced by 1S protection circuit
- any 2S voltage-divider values: recalculated for 1S
- any 2S fuel-gauge choice: removed from Rev A
- 2S low-voltage firmware thresholds: replaced by 1S thresholds

### Retained

- TPS61088 radio boost converter
- 5.0 V / 3 A radio-rail target
- Seeed XIAO nRF52840
- EBYTE E22-900M33S
- XT30 battery and solar connectors
- optional BME680 JST-GH connector
- PCB-mounted edge-launch SMA
- four-layer PCB and two-ounce outer copper preference

### Recalculation required during schematic capture

- BQ25798 1S charger configuration
- BQ25798 input-current and charge-current limits
- BQ25798 input-selector MOSFET ratings and gate behavior
- BQ25798 inductor current and saturation rating
- TPS61088 inductor, current limit, compensation and thermal design
- battery fuse rating
- 1S protection MOSFET resistance and trip threshold
- low-battery firmware thresholds
- BQ25798 telemetry integration in firmware

## Connector architecture

- Battery: XT30
- Solar: XT30
- Optional environmental sensor: 4-pin JST-GH
- Antenna: PCB-mounted edge-launch SMA
- Programming: XIAO USB-C
- Recovery/debug: Tag-Connect or SWD pads
- Mounting: four M3 non-plated corner holes

## Design philosophy

Rev A is deployment-focused. It omits bench-only test points and current shunts. Necessary EBYTE configuration resistors may remain where required for signal-routing flexibility. The XIAO and EBYTE modules remain serviceable.

## Current open decisions

1. Select exact 6 V / 20 W panel and confirm its Vmp and Voc.
2. Complete BQ25798 charger configuration and component review.
3. Complete TPS61088 1S-to-5 V power-stage calculations.
4. Select exact protected 1S 15 Ah battery pack and NTC specification.
5. Select hardware radio-rail over-voltage protection.
6. Verify exact E22 footprint, antenna-path selection and RF pin mapping.
7. Implement MeshCore driver changes required for the external PA and RF switch.
8. Confirm BQ25798 battery/charger telemetry integration.
9. Confirm BME680 support in the selected MeshCore repeater build.
10. Finalize enclosure, vent and cable-gland selections.
11. Finalize legal transmit-power configuration for Canadian deployment.
