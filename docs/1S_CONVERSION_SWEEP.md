# RoyalNode 1S Conversion Sweep

This document records every major design area affected by changing RoyalNode from a 2S battery architecture to a 1S battery architecture.

## Architecture decision

RoyalNode Rev A shall use:

- 6 V nominal solar input, with exact panel Vmp/Imp/Voc still to be selected
- BQ24650 solar MPPT buck charger configured for one Li-ion cell, pending input-headroom validation
- protected 1S flat LiPo battery pack
- board-mounted XT30 connectors for both solar and battery
- TPS61088 synchronous boost converter for the 5.0 V radio rail
- MAX17048 single-cell fuel gauge, with protected ADC-divider telemetry as fallback
- USB-C for firmware updates, external power and charging
- push-button power control
- charging and status LEDs
- direct 50-ohm PCB path from E22 ANT to board-edge SMA

## Component sweep

| Subsystem | Previous choice | Revised Rev A choice | Action |
|---|---|---|---|
| Solar charger | BQ25798 buck-boost multi-cell charger | BQ24650 standalone solar MPPT buck controller | Validate 6 V panel headroom before freezing |
| Battery | 2S pack | Protected 1S flat LiPo | Replace |
| Cell balancing | Required | Not required | Remove |
| Battery protection | 2S BMS | 1S protector/BMS rated at least 5 A | Replace |
| Radio regulator | 5 V buck from 2S | TPS61088 5 V boost from 1S | Recalculate and validate |
| Fuel gauge | 2S-capable gauge/ADC | MAX17048 plus optional ADC cross-check | Standardize |
| Low-voltage thresholds | 2S thresholds | 1S thresholds | Replace firmware values |
| Battery fuse | Lower current possible | Higher-current path required | Recalculate |
| Battery wiring | 18–20 AWG possible | 16–18 AWG preferred | Increase capacity |
| Battery connector | XT60 | Board-mounted XT30 | Replace footprint |
| Solar connector | XT60 | Board-mounted XT30 | Replace footprint |
| USB-C | Firmware only or undefined | Firmware, external power and charging | Add controlled power-path design |
| Power control | Undefined | Push-button latching/load-switch architecture | Add |
| Indicators | Undefined | Charging and system-status LEDs | Add |
| XIAO supply | Derived from battery/system rail | Separate low-noise regulated rail | Redesign |
| XIAO onboard charger | Present | Must be isolated or deliberately incorporated | Resolve conflict |
| Solar telemetry | Omitted | Omitted | No change |
| Current shunts/test points | Omitted | Omitted | No change |
| RF path | EBYTE ANT pin to remote connector | Direct short 50-ohm trace to board-edge SMA | Lock mechanically and electromagnetically |

## Charger-stage parts requiring selection

The BQ24650 is a controller, not an all-in-one power stage. The schematic must include and validate:

- BQ24650RVA controller
- high-side and low-side N-channel MOSFETs
- 600 kHz power inductor
- charge-current sense resistor
- input-voltage/MPPT divider
- battery-voltage feedback divider set for 4.20 V
- input and output ceramic capacitors
- local bulk capacitors
- battery NTC network
- charge-status outputs for LEDs and/or MCU sensing
- input fuse, reverse-polarity protection and TVS
- USB-C input OR-ing or ideal-diode path so solar and USB cannot backfeed one another

The BQ24650 accepts 5–28 V input, but a nominal 6 V panel may provide limited practical buck-converter headroom after hot-panel voltage drop, cable loss and weak sun. Exact panel Vmp and Voc must therefore be validated before this charger is frozen.

Initial charger target is 2.0–2.5 A maximum charge current, subject to the selected panel's actual Vmp, thermal limits and battery manufacturer's maximum charge rate.

## Radio boost-stage parts requiring selection or recalculation

- TPS61088RHLR
- approximately 1 uH shielded inductor with adequate saturation-current margin
- input ceramic and bulk capacitance sized for high pulsed battery current
- output ceramic and low-ESR bulk capacitance near the EBYTE module
- feedback divider for 5.0 V
- switching-frequency resistor
- current-limit resistor
- soft-start capacitor
- enable pull-down and MCU control
- output short-circuit/load-disconnect protection

The converter must be validated at:

- 4.2 V battery input
- 3.7 V nominal input
- 3.2 V low-battery input
- full radio load and repeated transmit transitions

## Battery-pack requirements

- protected 1S flat LiPo pack
- nominal voltage approximately 3.6–3.7 V
- full-charge voltage 4.20 V
- final capacity still to be selected
- at least 5 A continuous discharge capability
- higher transient discharge capability preferred
- integrated over-charge, over-discharge, over-current and short-circuit protection
- battery-mounted NTC compatible with charger network
- XT30 output
- main fuse located close to the pack

## USB-C and XIAO integration

The XIAO nRF52840 supports USB firmware updates and includes its own low-current LiPo charger. The custom board's main charger will be much higher current, so the two charging paths must not be tied to the battery without a deliberate architecture.

Rev A must choose one approach:

1. isolate the XIAO battery-charger path and use USB only for data/5 V input to the main charger, or
2. leave the XIAO charger connected only as a tightly current-limited backup path with verified no-backfeed behavior.

The preferred approach is to isolate the XIAO charger from the main battery while retaining USB data and 5 V sensing.

## Firmware changes

- change battery model from 2S to 1S
- initialize MAX17048 and report voltage plus state of charge
- optionally compare MAX17048 voltage with the XIAO ADC
- control system-status LED with low duty cycle
- read charger status outputs
- implement push-button shutdown behavior
- reduce transmit power as battery approaches approximately 3.5 V
- disable full-power transmission below approximately 3.3 V
- disable the radio boost near approximately 3.1–3.2 V
- retain charger temperature lockout behavior

Thresholds are provisional and must be tuned to the selected cell chemistry, load sag and protection-board cutoff.

## Mechanical and PCB consequences

- board-mounted XT30 connectors require through-hole anchoring and enclosure support
- the board-mounted SMA requires edge placement, ground stitching and enclosure clearance
- the E22 ANT-to-SMA trace must be controlled to 50 ohms using the final PCB stack-up
- 1S battery current is higher, so battery copper pours, vias, fuse and wiring require more current margin
- TPS61088 placement and switching-loop geometry are critical
- switching converters must be kept away from the RF path and antenna connector
- power button and LEDs must remain accessible through the enclosure

## Gate before schematic capture

Do not freeze the schematic until these are selected:

1. Exact solar panel with Vmp, Imp and Voc specifications.
2. Exact protected flat LiPo capacity, discharge rating, dimensions and NTC.
3. Exact BQ24650 MOSFETs, inductor and charge-current target.
4. Exact TPS61088 inductor and power-stage values.
5. Exact 1S protection arrangement and fuse.
6. Exact XT30 PCB part numbers, gender and orientation for battery and solar.
7. Exact board-edge SMA footprint and enclosure interface.
8. Exact push-button power-controller/load-switch circuit.
9. Final USB-C power-path architecture and XIAO charger isolation method.
