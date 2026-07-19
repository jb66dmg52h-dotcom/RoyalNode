# RoyalNode Rev A System Architecture

## Proposed block diagram

```text
6 V / 20 W solar panel
          |
  XT60, fuse, reverse protection,
  TVS and input filtering
          |
  BQ24650 1S solar MPPT buck charger
          |
  1S 15 Ah protected Li-ion battery
          |
      XT60 + main fuse
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

The previous BQ25798 buck-boost multi-cell charger is removed. RoyalNode now uses a one-cell charger architecture.

The preferred charger is BQ24650 configured for one Li-ion cell. It is a standalone synchronous buck charger controller with programmable solar input-voltage regulation, supports one to six cells, accepts 5 V to 28 V input and can control charge currents well above RoyalNode's requirement.

For a 6 V nominal panel, the final selected panel must maintain enough voltage above the battery and converter losses during charging. The MPPT input-voltage setpoint, charge-current resistor, external MOSFETs and inductor must be calculated from the actual panel maximum-power voltage rather than the printed nominal voltage alone.

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
- a main fuse near the XT60 connection

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

The XIAO must not use its onboard battery charger. The custom BQ24650 charger is the only battery-charging path. Programming uses the XIAO USB-C port; recovery uses SWD pads or Tag-Connect.

### Battery telemetry

MAX17048 is the preferred single-cell fuel gauge because it is intended for one Li-ion cell and does not require a current-sense resistor. A protected ADC divider remains an alternate implementation if MeshCore integration is simpler.

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

- BQ25798 multi-cell buck-boost charger: removed
- 2S 15 Ah battery pack: replaced by protected 1S 15 Ah pack
- 2S BMS and balancing function: replaced by 1S protection circuit
- any 2S voltage-divider values: recalculated for 1S
- any 2S fuel-gauge choice: standardized on MAX17048
- 2S low-voltage firmware thresholds: replaced by 1S thresholds

### Retained

- TPS61088 radio boost converter
- 5.0 V / 3 A radio-rail target
- Seeed XIAO nRF52840
- EBYTE E22-900M33S
- XT60 battery and solar connectors
- optional BME680 JST-GH connector
- PCB-mounted edge-launch SMA
- four-layer PCB and two-ounce outer copper preference

### Recalculation required during schematic capture

- BQ24650 MPPT divider
- BQ24650 battery-voltage divider for 4.20 V
- charge-current sense resistor
- charger external MOSFET ratings and gate behavior
- charger inductor current and saturation rating
- TPS61088 inductor, current limit, compensation and thermal design
- battery fuse rating
- 1S protection MOSFET resistance and trip threshold
- low-battery firmware thresholds
- battery telemetry divider if MAX17048 is not used

## Connector architecture

- Battery: XT60
- Solar: XT60
- Optional environmental sensor: 4-pin JST-GH
- Antenna: PCB-mounted edge-launch SMA
- Programming: XIAO USB-C
- Recovery/debug: Tag-Connect or SWD pads

## Design philosophy

Rev A is deployment-focused. It omits bench-only test points and current shunts. Necessary EBYTE configuration resistors may remain where required for signal-routing flexibility. The XIAO and EBYTE modules remain serviceable.

## Current open decisions

1. Select exact 6 V / 20 W panel and confirm its Vmp and Voc.
2. Complete BQ24650 charger calculations and component selection.
3. Complete TPS61088 1S-to-5 V power-stage calculations.
4. Select exact protected 1S 15 Ah battery pack and NTC specification.
5. Select hardware radio-rail over-voltage protection.
6. Verify exact E22 footprint, antenna-path selection and RF pin mapping.
7. Implement MeshCore driver changes required for the external PA and RF switch.
8. Confirm MAX17048 or ADC telemetry integration.
9. Confirm BME680 support in the selected MeshCore repeater build.
10. Finalize enclosure, vent and cable-gland selections.
11. Finalize legal transmit-power configuration for Canadian deployment.
