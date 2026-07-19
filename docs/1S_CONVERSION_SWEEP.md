# RoyalNode 1S Conversion Sweep

This document records every major design area affected by changing RoyalNode from a 2S battery architecture to a 1S battery architecture.

## Architecture decision

RoyalNode Rev A shall use:

- 6 V nominal, 20 W solar panel
- BQ24650 solar MPPT buck charger configured for one Li-ion cell
- protected 1S 15 Ah Li-ion battery pack
- TPS61088 synchronous boost converter for the 5.0 V radio rail
- MAX17048 single-cell fuel gauge or protected ADC-divider telemetry

## Component sweep

| Subsystem | Previous 2S choice | Revised 1S choice | Action |
|---|---|---|---|
| Solar charger | BQ25798 buck-boost multi-cell charger | BQ24650 standalone solar MPPT buck controller | Replace |
| Battery | 2S 15 Ah protected pack | 1S 15 Ah protected pack | Replace |
| Cell balancing | Required | Not required | Remove |
| Battery protection | 2S BMS | 1S protector/BMS rated at least 5 A | Replace |
| Radio regulator | 5 V buck from 2S | TPS61088 5 V boost from 1S | Replace topology; TPS61088 retained from earlier 1S concept |
| Fuel gauge | 2S-capable gauge/ADC | MAX17048 single-cell gauge | Standardize |
| Battery divider | Sized for 8.4 V | Sized for 4.2 V if ADC is used | Recalculate |
| Low-voltage thresholds | 2S thresholds | 1S thresholds | Replace firmware values |
| Battery fuse | Lower current possible | Higher-current path required | Recalculate |
| Battery wiring | 18–20 AWG possible | 16–18 AWG preferred | Increase capacity |
| XT60 battery connector | Retained | Retained | No change |
| XT60 solar connector | Retained | Retained | No change |
| XIAO supply | Derived from 2S rail | Separate regulated rail from 1S/system path | Redesign |
| Solar telemetry | Omitted | Omitted | No change |
| Current shunts/test points | Omitted | Omitted | No change |
| SMA RF path | EBYTE ANT pin to SMA | Same | No change |

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
- charge-status pull-ups or LEDs only if required
- input fuse, reverse-polarity protection and TVS

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
- hardware output over-voltage protection

The converter must be validated at:

- 4.2 V battery input
- 3.7 V nominal input
- 3.2 V low-battery input
- full radio load and repeated transmit transitions

## Battery-pack requirements

- 1S parallel-cell pack assembled from matched cells
- nominal voltage approximately 3.6–3.7 V
- full-charge voltage 4.20 V
- target capacity 15 Ah
- at least 5 A continuous discharge capability
- higher transient discharge capability preferred
- integrated over-charge, over-discharge, over-current and short-circuit protection
- battery-mounted NTC compatible with charger network
- XT60 output
- main fuse located close to the pack

## Firmware changes

- change battery model from 2S to 1S
- update voltage-to-percentage behavior
- initialize MAX17048 if selected
- reduce transmit power as battery approaches approximately 3.5 V
- disable full-power transmission below approximately 3.3 V
- disable the radio boost near approximately 3.1–3.2 V
- retain charger temperature lockout behavior
- update documentation and telemetry labels

Thresholds are provisional and must be tuned to the selected cell chemistry, load sag and protection-board cutoff.

## Mechanical and PCB consequences

- 1S battery current is higher, so battery copper pours, vias, fuse and wiring require more current margin.
- TPS61088 placement and switching-loop geometry become more critical.
- The charger changes from a highly integrated buck-boost IC to a controller with external MOSFETs, increasing charger-area component count.
- The battery pack may be physically simpler because parallel cells do not require balance leads.
- XT60, JST-GH environmental connector, SMA and mounting scheme remain unchanged.

## Items eliminated by the conversion

- second series cell group
- balance connection between series groups
- 2S BMS/balancer
- 8.4 V charger configuration
- BQ25798-specific I2C charger configuration
- 2S battery telemetry scaling
- 2S low-battery firmware thresholds

## Gate before schematic capture

Do not freeze the schematic until these are selected:

1. Exact solar panel with Vmp, Imp and Voc specifications.
2. Exact 1S 15 Ah battery pack or cell arrangement.
3. Exact battery NTC value and curve.
4. Exact BQ24650 MOSFETs, inductor and current target.
5. Exact TPS61088 inductor and power-stage values.
6. Exact 1S protection board or onboard protection design.
