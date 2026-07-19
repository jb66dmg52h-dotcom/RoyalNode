# 2Watt Project Compatibility and Conflict Audit, Rev 2

## Overall verdict

The core radio, MCU, telemetry and connector selections are compatible. The largest architecture change from this audit is replacing the earlier BQ24650 concept with BQ25798 for Rev A. BQ25798 better matches the actual requirement because it accepts both a 12 V-class solar source and 5 V USB, supports a 1S LiPo, includes buck-boost charging, MPPT, power-path management and optional dual-input selection.

The design is ready for detailed schematic capture after the remaining power-button and exact passive-component calculations are completed.

## Conflict findings

### 1. BQ24650 versus USB-C charging

Status: conflict resolved by architecture change.

BQ24650 is a buck-only charger. It is comfortable with a 12 V solar panel but leaves little margin when charging a 4.2 V battery from a 5 V USB source. Supporting solar and USB cleanly would require extra charger and source-selection circuitry.

Decision: use BQ25798 instead of BQ24650 for Rev A.

### 2. XIAO onboard charger

Status: resolved.

- XIAO BAT pad remains completely unconnected.
- Project battery connects only to the main charger/power path.
- USB D+/D- remain native to XIAO for firmware updates.
- USB VBUS is taken from the XIAO 5V pad and routed to the main charger input through protection/current limiting.

No two charger outputs are paralleled.

### 3. GPIO count

Status: resolved with underside pads.

All 11 edge GPIOs are consumed by E22 control and the shared I2C bus. NFC1/P0.09 and NFC2/P0.10 are repurposed as GPIO for power-button sense and charger interrupt. This requires a UICR configuration change and firmware validation.

### 4. Shared I2C bus

Status: compatible.

BQ25798 and MAX17048 can share D4/D5 provided their addresses do not collide. Pull-ups must be to the XIAO 3.3 V logic rail. Firmware should initialize the charger first, then the gauge, and tolerate either device being absent during bench testing.

### 5. E22 logic and power

Status: compatible.

- XIAO and E22 digital interface are 3.3 V logic.
- E22 high-power module is supplied from a dedicated 5 V rail.
- Radio rail must tolerate approximately 1.2 A transmit demand with transient margin.
- TXEN and RXEN require explicit firmware sequencing.
- TCXO setup must configure DIO3 to the module-required 2.2 V.

### 6. TPS61088 radio supply

Status: compatible, layout-critical.

TPS61088 supports single-cell input and 5 V output at the required power. The exact inductor, frequency, current-limit resistor, feedback divider, input/output capacitance and thermal copper remain calculation tasks. The radio branch should include load disconnect because TPS61088 itself does not provide true output isolation in every fault/off condition.

### 7. XIAO power source

Status: unresolved at component level, resolved at architecture level.

The XIAO must be powered through its documented 5V pin, not by treating 3V3 as an undocumented input. The carrier needs a dedicated low-current XIAO supply path from the BQ25798 system rail, with USB/system source isolation. Candidate implementations include a small 5 V buck-boost plus ideal-diode/power mux, or an approved use of the main 5 V converter with separate filtering and radio load switching.

Decision gate: choose the lower-quiescent-current implementation after idle-power calculations.

### 8. JST-PH 2.0 service connector

Status: compatible.

A 4-pin SMT JST-PH service connector can carry SWDIO, SWCLK, 3V3 reference and ground. It must not be used to power the product. Confirm chosen connector orientation and cable availability before footprint freeze.

### 9. XT30 connectors

Status: compatible with mechanical precautions.

- battery and solar must use different genders and/or opposite physical orientation
- both need clear silkscreen labels
- board and enclosure must absorb insertion/removal force
- solar input gets reverse-polarity protection and fuse/TVS
- battery input gets fuse and reverse-connection protection strategy

### 10. Direct SMA RF path

Status: compatible.

The direct board-edge SMA path is electrically preferred. The exact connector must match the selected board thickness. A 4-layer controlled-impedance PCB is recommended so the RF reference plane and power integrity are predictable.

### 11. BQ25798 firmware dependency

Status: new firmware requirement.

Unlike the standalone BQ24650, BQ25798 is I2C-controlled. Firmware must set and verify:

- 1S battery configuration
- charge voltage and charge-current limit
- input-current limits
- MPPT/VOC behavior for solar
- USB source detection behavior
- thermistor limits
- fault handling
- ship/shutdown mode policy

A safe autonomous/default configuration must be confirmed so the board cannot overcharge before firmware completes initialization.

## Remaining freeze blockers

1. Exact protected 1S flat LiPo specification and NTC curve.
2. Exact BQ25798 reference circuit values and input-selector implementation.
3. Exact TPS61088 power-stage calculations and load-disconnect circuit.
4. Exact XIAO supply implementation.
5. Exact push-button latch/controller.
6. Exact XT30, JST-PH and SMA manufacturer part numbers.
7. Final 4-layer stack-up and controlled-impedance calculation.
8. MeshCore board definition for TXEN, RXEN, TCXO and power mapping.
