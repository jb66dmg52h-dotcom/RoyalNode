# 2Watt Project Solar Design Guide, Rev A

## Supported panel class

- Nominal panel class: 12 V
- Supported deployment size: 10-20 W
- Minimum recommended size: 10 W
- Preferred permanent-deployment size: 20 W
- Installer must verify Vmp, Voc, Imp and cold-weather Voc
- Board protection thresholds are approximately 7 V undervoltage and 25 V overvoltage at the LTC4365 stage

## Representative 10 W panel

A representative 12 V-class 10 W panel may have Vmp around 17 V and Imp around 0.6 A. Exact values depend on the selected panel and must be taken from its datasheet.

A 10 W panel is sufficient for normal repeater operation in good sun, but battery recovery margin is limited during heavy traffic, winter conditions, shading or prolonged cloud.

## Representative 20 W panel

A representative 12 V-class 20 W panel may have Vmp around 17-18 V and Imp around 1.1-1.2 A. Exact values depend on the selected panel.

20 W remains the preferred permanent-deployment size because it provides more margin for:

- winter and cloudy weather
- recovery after multiple poor-solar days
- battery charging while the radio is active
- achieving the configured charge-current ceiling when solar conditions permit

## Daily-energy context

A nominal 3.7 V, 10 Ah battery stores roughly 37 Wh; a 20 Ah pack stores roughly 74 Wh. Real usable energy depends on pack protection thresholds, temperature, age and discharge rate.

Solar yield depends strongly on season, panel angle, orientation, shading and weather. The board does not assume a fixed number of peak-sun-hours in its electrical design.

## Locked solar protection path

```text
Solar XT30
  -> Littelfuse 0483002.DR, 2 A fuse
  -> LTC4365ITS8-1#TRMPBF surge/reverse-input controller
  -> Infineon ISA170170N04LMDSXTMA1 back-to-back protection MOSFET pair
  -> BQ25798 solar input-selector MOSFET pair
  -> BQ25798 VBUS
```

### LTC4365 threshold network

Locked divider values:

- R3: 1.87 MOhm
- R2: 104 kOhm
- R1: 40.2 kOhm

Design thresholds:

- UV falling: approximately 6.98 V
- UV rising: approximately 7.33 V
- OV rising: approximately 25.05 V
- OV falling: approximately 23.80 V

The older SMBJ22A + BSL303SPE-only protection concept is superseded and must not be used for Rev A schematic capture.

## BQ25798 solar charging

- Solar is the primary charging source.
- BQ25798 MPPT is enabled by host firmware when solar charging is active.
- MPPT open-circuit measurement delay target: 300 ms.
- MPPT measurement interval target: 2 minutes.
- The final `VOC_PCT` setting must be selected from the actual production panel's Vmp/Voc ratio. It is not locked until the panel is selected.
- Firmware must restore MPPT configuration after charger-reset conditions that clear the relevant register state.

## Input-current considerations

The 2 A fuse is on the solar connector/protection input. A 20 W 12 V-class panel typically remains well below 2 A Imp, but the actual panel's short-circuit current and protection coordination must still be checked before deployment.

The BQ25798 input-current and charge-current limits determine how available solar power is split between system load and battery charging.

## Deployment verdict

- 10 W: supported for lower-demand or favorable-sun deployments
- 20 W: recommended for permanent outdoor deployments
- larger panels are not automatically compatible merely because the wattage is higher; Voc, cold-weather Voc, Imp/Isc and protection limits must all remain within the board design limits
