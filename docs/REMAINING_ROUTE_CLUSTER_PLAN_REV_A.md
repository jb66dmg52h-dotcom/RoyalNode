# RoyalNode Rev A Remaining Route Cluster Plan

This file groups the remaining generated KiCad ratsnest items after the clean
18-unrouted checkpoint. It is a layout planning aid, not a fabrication release.

Current gate:

```text
make layout-status
  ERC: 0
  DRC: 3 known footprint warnings only
  Unrouted: 18 ratsnest pairs
```

## Cluster A: TPS61088 5 V Radio Boost Output

Remaining nets:

- `5V_RADIO`
- `BOOST_VCC`
- `BOOST_COMP`

Current status:

- `BQ_SYS` input capacitance is now moved into the local U3/L2 input area and routed.
- U3/L2 topology is improved, but the output rail and support passives are still staged.
- Several C405/`BOOST_VCC` single-part moves were rejected around U3 because they collided with `BOOST_EN`, `BOOST_FSW`, `BOOST_ILIM`, U3 ground thermal relief or L2/R402 courtyards.
- Two `5V_RADIO` shortcut routes toward E22 were rejected because they crossed `BOOST_FB`, SPI/control fanouts and E22 ground pins.

Next strategy:

- Move the TPS61088 output capacitors and feedback divider as a group instead of one part at a time.
- Keep `5V_RADIO` as a deliberate high-current copper shape from U3 VOUT to E22 VCC and the local capacitor bank.
- Preserve the E22 control/SPI fanout corridors unless the whole radio/boost placement is reviewed.

Do not:

- Route `5V_RADIO` as a long skinny internal trace.
- Keep searching the immediate U3 underside for C405 without moving EN/FSW/ILIM support routing.

## Cluster B: BQ25798 Charger Power Stage

Remaining nets:

- `BQ_PMID`
- `BQ_VBUS`
- `BQ_SW1`
- `BQ_SW2`
- `BQ_BTST2`
- `SOLAR_PROTECTED`
- `USB_VBUS_RAW`

Current status:

- The existing L1 position leaves `BQ_SW1`/`BQ_SW2` too far below the U1 switch pins.
- A trial moving only L1 above U1 was rejected because it collided with the accepted TPS61088 input-cap cluster and U1 support passives.
- A direct `BQ_SW1` top route lowered the ratsnest count but failed badly by running down the U1 left pad row.
- `BQ_PMID` bridge retries lower the count but short/crowd `BQ_STAT`, `BQ_BTST1` and the accepted `BQ_SYS` spine.
- `BQ_SW2` and `BQ_BTST2` remain coupled to C217 placement and the U1 right-side escape.

Next strategy:

- Reposition L1 closer to the U1 switch pins before retrying `BQ_SW1`/`BQ_SW2`.
- Treat C216/C217 bootstrap capacitors, `BQ_TS`, `BQ_REGN`, `BQ_PMID` and switch-node escapes as a shared U1 fanout problem.
- Move BQ25798 VBUS/PMID capacitor banks nearer U1/Q2/Q3 only as part of a grouped capacitor/passive placement pass.

Do not:

- Run wide switch-node traces down the U1 pad row.
- Add one-off vias beside U1 pads 1-9 or 17-20.

## Cluster C: BQ25798 Local Regulation And Sense

Remaining nets:

- `BQ_REGN`
- `BATP_KELVIN`

Current status:

- `BQ_REGN` pin-to-pin bridge trials lowered the count but shorted/crowded `BAT_RAW`, `BQ_TS`, `BQ_BTST1` and I2C corridors.
- A top-layer REGN wrap also failed because the U1 perimeter is already occupied by ACDRV, I2C, TS and ground-thermal relief.
- `BATP_KELVIN` route trials failed because the U1-side via conflicts with the same dense right-side U1 escape area.
- R202 tight-local relocation at U1 was also rejected because the 0603 footprint overlaps/crowds the U1 right-side support-passive escape.

Next strategy:

- Rework C215/R200/R201/R202 as a local U1 support-passive group.
- Keep BATP as a sense route; do not merge it into the high-current battery copper.

Do not:

- Add test pads, shunts or measurement links.
- Treat BATP as a high-current battery rail.

## Cluster D: Connector And Service Power

Remaining nets:

- `USB_VBUS_RAW`
- portions of `BQ_VBUS`
- portions of `SOLAR_PROTECTED`

Current status:

- Previous USB right-edge route attempts crossed `BOOST_EN`, `BAT_RAW`, I2C, `XIAO_BAT_ISO`, `BQ_VBUS` or XT30 mechanical pads depending on layer.
- Solar protected U1-entry attempts crossed accepted input-selector and I2C routes.

Next strategy:

- Rework Q2/Q3/U1 input-selector placement or define a more deliberate service-power corridor.
- Keep XT30 and JST-GH connector access clear; do not rotate connectors back into the earlier blocked J3/J6 arrangement.

## Recommended Next Layout Pass

The highest-value next pass is:

```text
Refactor the BQ25798 power-stage placement:
  1. Move L1 closer to U1 switch pins.
  2. Re-stage C216/C217 around the new L1/U1 geometry.
  3. Re-test BQ_SW1, BQ_SW2 and BQ_BTST2.
  4. Only then retry BQ_PMID and BQ_REGN.
```

This should reduce several remaining unrouted items while improving the actual
charger power-loop geometry.
