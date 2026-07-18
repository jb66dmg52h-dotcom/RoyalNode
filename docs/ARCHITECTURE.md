# RoyalNode Rev A System Architecture

## Proposed block diagram

```text
6 V / 20 W solar panel
          |
  fuse, reverse protection,
  TVS and high-current filtering
          |
 true-MPPT buck-boost 2S charger
          |
  2S 15 Ah protected battery
          |
      main fuse
          |
          +-----------------------------+
          |                             |
  5.0 V / 3 A radio buck         low-noise MCU rail
          |                             |
 EBYTE E22-900M33S              Seeed XIAO nRF52840
          |                             |
          +------ SPI and controls -----+
                                        |
                              optional 4-pin JST-GH
                               BME680 environmental
```

## Major subsystems

### Solar and charger subsystem

The charger must accept a 6 V nominal panel, perform true MPPT operation, boost as required to charge a 2S lithium-ion pack, support battery temperature sensing and provide programmable current limits. BQ25798 is the current candidate because it supports a 3.6–24 V input range, 1–4 cells and buck-boost solar charging.

The current BQ25798 candidate regulates input current up to approximately 3.3 A. Therefore, the practical panel target is 6 V / 20 W. A larger 6 V panel cannot be fully harvested through a single BQ25798 input and would require a higher-current charger or multiple power-conversion channels.

### Battery subsystem

Target pack: protected 2S 15 Ah lithium-ion with balancing and a pack-mounted temperature sensor. The PCB shall not depend solely on the pack BMS; a serviceable main fuse is required near the pack connection.

Battery voltage is the required deployed power telemetry value. Charger and battery temperature sensing remain mandatory for safe charging but do not need to be transmitted through MeshCore.

### Radio power subsystem

The radio receives a dedicated 5.0 V rail sized for at least 3 A continuous operation with transient margin. The converter shall include a controlled enable input, soft start, local bulk capacitance and hardware over-voltage protection.

Permanent radio-current and regulator-temperature telemetry ICs are omitted. No current-shunt footprints, measurement links, dedicated test pads or probe loops are included.

### MCU subsystem

The Seeed XIAO nRF52840 is socketed on Rev A. It handles the SPI radio interface, radio power sequencing, battery voltage telemetry, optional environmental telemetry, fault logging and the MeshCore hardware abstraction layer.

Programming uses the XIAO USB-C port. Recovery uses a Tag-Connect or exposed SWD pads. No six-pin JST debug connector is fitted.

### Radio subsystem

The EBYTE E22-900M33S contains an SX1262-family transceiver and external high-power RF front end. Integration requires validated control of reset, BUSY, DIO1, RXEN, TXEN or DIO2 RF-switch control, and DIO3 TCXO behavior.

## MeshCore telemetry architecture

RoyalNode only includes deployed telemetry that the MeshCore ecosystem can represent.

### Required

- Battery voltage
- MCU internal temperature where supported by the XIAO nRF52840 board definition

### Optional

- BME680 environmental sensor over I2C
- Reported values: temperature, humidity and pressure
- Connector: one 4-pin JST-GH, 1.25 mm pitch
- Pinout: 3.3 V, GND, SDA, SCL

### Omitted

- solar current telemetry
- radio current telemetry
- battery current telemetry
- external PA temperature
- regulator temperature
- fan sensing or control
- generic analog sensor ports
- general-purpose accessory connectors
- GPS hardware for a fixed repeater

Fixed node coordinates should be configured in firmware rather than adding GPS hardware.

## 6 V panel power estimate

A 20 W panel at 6 V produces approximately 3.3 A at its maximum-power point. Using a conservative winter model of one equivalent full-sun hour and 55% net daily efficiency gives about 11 Wh per day of usable energy.

Expected RoyalNode consumption is approximately:

- light traffic: 6 Wh/day
- moderate traffic: 7–8 Wh/day
- heavy traffic: 13–15 Wh/day

Therefore, 20 W is appropriate for light-to-moderate traffic with battery reserve. Truly heavy sustained traffic in poor winter conditions would require either more panel voltage, a higher-current 6 V charger architecture, or additional panel/charger channels.

## Connector architecture

- Battery: XT60
- Solar: XT60
- Optional environmental sensor: 4-pin JST-GH
- Antenna: U.FL to SMA bulkhead
- Programming: XIAO USB-C
- Recovery/debug: Tag-Connect or SWD pads

No other low-current detachable connectors are planned for Rev A.

## Design philosophy

Rev A is deployment-focused and intentionally omits bench-only hardware. The board will not include dedicated test points, measurement loops, current-shunt footprints or removable links used only for probing. Necessary EBYTE configuration resistors may remain where required for signal-routing flexibility. The EBYTE module and XIAO remain replaceable during development.

## Current open decisions

1. Final MPPT charger and support circuitry for 6 V boost operation.
2. Final 5 V / 3 A synchronous buck regulator.
3. Battery-pack NTC specification.
4. Hardware radio-rail over-voltage shutdown method.
5. Exact E22 footprint and pin mapping from the manufacturer drawing.
6. MeshCore driver changes required for the external PA and RF switch.
7. Confirming XIAO nRF52840 MCU-temperature telemetry support.
8. Confirming the exact BME680 data path in the selected MeshCore repeater build.
9. Enclosure size, vent and cable-gland selections.
10. Final legal transmit-power configuration for Canadian deployment.
