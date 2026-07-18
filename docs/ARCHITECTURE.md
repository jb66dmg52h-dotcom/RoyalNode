# RoyalNode Rev A System Architecture

## Proposed block diagram

```text
18 V / 30 W solar panel
          |
  fuse, reverse protection,
  TVS and input filtering
          |
  true-MPPT 2S charger
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
```

## Major subsystems

### Solar and charger subsystem

The charger must accept an 18 V nominal panel, perform true MPPT operation, charge a 2S lithium-ion pack, support battery temperature sensing and provide programmable current limits. BQ25798 is the current candidate but remains subject to schematic-level validation and sourcing review.

### Battery subsystem

Target pack: protected 2S 15 Ah lithium-ion with balancing and a pack-mounted temperature sensor. The PCB shall not depend solely on the pack BMS; a serviceable main fuse is required near the pack connection.

### Radio power subsystem

The radio receives a dedicated 5.0 V rail sized for at least 3 A continuous operation with transient margin. The converter shall include a controlled enable input, soft start, current monitoring, local bulk capacitance and hardware over-voltage protection.

### MCU subsystem

The Seeed XIAO nRF52840 is socketed on Rev A. It handles the SPI radio interface, radio power sequencing, battery and solar telemetry, temperature monitoring, fault logging and the MeshCore hardware abstraction layer.

### Radio subsystem

The EBYTE E22-900M33S contains an SX1262-family transceiver and external high-power RF front end. Integration requires validated control of reset, BUSY, DIO1, RXEN, TXEN or DIO2 RF-switch control, and DIO3 TCXO behavior.

### Measurement subsystem

Rev A should measure:

- solar input voltage and current
- battery voltage and state of charge
- battery temperature
- 5 V radio voltage and current
- PCB or regulator temperature
- radio-area temperature

## Design philosophy

Rev A prioritizes testability over minimum size. Uncertain signal routes should use zero-ohm configuration resistors. Critical rails and controls require labeled test points. The EBYTE module and XIAO should remain replaceable during development.

## Current open decisions

1. Final MPPT charger and support circuitry.
2. Final 5 V / 3 A synchronous buck regulator.
3. Battery-pack connector and exact NTC specification.
4. Current-monitor architecture and shunt values.
5. Hardware radio-rail over-voltage shutdown method.
6. Exact E22 footprint and pin mapping from the manufacturer drawing.
7. MeshCore driver changes required for the external PA and RF switch.
8. Enclosure size, vent and cable-gland selections.
9. Final legal transmit-power configuration for Canadian deployment.
