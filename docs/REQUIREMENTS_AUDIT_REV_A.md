# 2Watt Project Requirements Audit, Rev A

## Purpose

This audit converts the conversation and prior engineering notes into a controlled set of Rev A requirements. It separates fixed requirements from preferences, recommendations and unresolved choices.

## Fixed product requirements

### Radio and firmware

- Use the EBYTE E22-900M33S 850-930 MHz module.
- Support up to the module's 33 dBm hardware capability, while deployed firmware settings must comply with local regulations.
- Use the standard Seeed Studio XIAO nRF52840 as the controller.
- Target MeshCore repeater operation.
- Preserve native USB firmware updates through the XIAO USB-C connector.
- Provide the radio signals NSS, SCK, MOSI, MISO, BUSY, DIO1, NRST, TXEN and RXEN.
- Configure the E22 TCXO correctly through the SX126x driver.

### RF

- Use a direct PCB connection from the E22 ANT pad to a board-mounted SMA female connector.
- Do not use a u.FL intermediate connector.
- Use a controlled 50-ohm trace based on the final PCB stack-up.
- Keep the RF trace short, ground-referenced and isolated from switching nodes.

### Battery and charging

- Use a protected 1S flat LiPo battery.
- Battery connector is board-mounted XT30.
- Solar connector is board-mounted XT30.
- Solar panel is not a fixed BOM item; deployment guidance recommends a compatible 12 V nominal panel class.
- USB-C must support both firmware updates and main-battery charging.
- Leave the XIAO BAT pad unconnected so its onboard charger remains isolated.
- Provide battery-voltage and state-of-charge telemetry.
- Provide battery-temperature charge protection using the battery NTC.

### User interface and service

- Provide a physical push-button power control.
- Provide charging and system-status indication.
- Provide a surface-mounted JST-PH 2.0 service connector for SWD access.
- Rev A XIAO should be socketed for replacement and debugging.
- E22 should be directly soldered to the carrier PCB.

### Mechanical and manufacturing

- First build quantity is five boards.
- Use factory assembly for QFN/DFN ICs and small SMD parts.
- Hand-install socketed XIAO, E22 module, XT30 connectors, SMA, button and service connector unless the assembler can place them safely at reasonable cost.
- Use a 4-layer controlled-impedance PCB.
- Mechanically support XT30 and SMA insertion forces through footprint choice and enclosure design.

## Performance requirements

### Radio power rail

- Nominal output: 5.0 V.
- Continuous design target: at least 2 A.
- Transient design target: 3 A class.
- Must tolerate repeated E22 transmit transitions without resetting the XIAO.
- Radio power must be independently switchable from the XIAO supply.

### Battery current path

- Design battery connector, fuse, copper, vias and protection for at least 5 A continuous capability.
- Account for higher current at low battery voltage.
- Disable or reduce full-power radio operation as the battery approaches low-voltage cutoff.

### Charging

- Charger must support one Li-ion/LiPo cell.
- Charger must accept approximately 5 V USB and a recommended 12 V nominal solar panel class.
- Charger must provide power-path operation so the unit can run while charging.
- Charger must provide solar MPPT behavior.
- Charge current must be configurable to the selected battery's permitted rate.
- Charge must stop outside the allowed battery-temperature range.

### Environmental

- Operating design target: outdoor Canadian conditions.
- Electronics target range should align with industrial-grade components where practical.
- Battery charging below the selected cell manufacturer's minimum charging temperature must be inhibited.

## Preferred architecture decisions

- Main charger and power-path IC: TI BQ25798.
- Radio boost converter: TI TPS61088.
- Fuel gauge: MAX17048.
- Radio load switch: TPS22990-class high-current load switch.
- Push-button latch: MAX16054-class controller.
- Shared I2C bus for BQ25798 and MAX17048.
- XIAO edge pins dedicated to radio plus I2C; underside NFC pads repurposed as extra GPIO.

## Requirements conflicts found

### USB-C charging versus XIAO onboard charger

Resolved by leaving XIAO BAT unconnected and routing USB VBUS into the main charger input.

### XIAO GPIO count

Resolved by using NFC1/P0.09 and NFC2/P0.10 as GPIO after UICR configuration.

### Radio surge versus MCU stability

Resolved architecturally by separating the radio branch with its own high-current boost stage, bulk capacitance and load switch.

### Fixed solar panel versus deployer choice

Resolved by defining a safe panel compatibility envelope rather than one required panel SKU.

## Open requirements that block final schematic freeze

1. Exact protected flat LiPo capacity, dimensions, maximum charge rate, discharge rating and NTC curve.
2. Whether the power button turns off only the XIAO/radio load or places BQ25798 into ship mode as well.
3. Exact USB source current target: conservative 500 mA default or BC1.2-detected higher current.
4. Exact recommended panel voltage envelope and maximum allowable cold-weather Voc.
5. Exact socket/header arrangement for the XIAO underside pads.
6. Exact enclosure dimensions and connector orientation.

## Audit verdict

The product requirements are coherent and the main architecture is compatible. The remaining unknowns affect component values and mechanical details, not the overall feasibility. Electrical schematic capture can begin as a Rev A draft, but the battery-specific charge and thermistor values must remain marked TBD until the battery pack is selected.
