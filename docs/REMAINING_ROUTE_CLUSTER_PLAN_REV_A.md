# RoyalNode Rev A Remaining Route Cluster Plan

This file groups the remaining generated KiCad ratsnest items after the clean
6-unrouted checkpoint. It is a layout planning aid, not a fabrication release.

Current gate:

```text
make layout-status
  ERC: 0
  DRC: 0 active violations/warnings; footprint-library mismatch is ignored by project policy for tracked local release-candidate footprints
  Unrouted: 5 ratsnest pairs
```

## Cluster A: TPS61088 5 V Radio Boost Output

Remaining nets:

- `BOOST_VCC`

Current status:

- `BQ_SYS` input capacitance is now moved into the local U3/L2 input area and routed.
- U3/L2 topology is improved, and the compensation RC pair is now staged locally below-right of U3.
- Several C405/`BOOST_VCC` single-part moves were rejected around U3 because they collided with `BOOST_EN`, `BOOST_FSW`, `BOOST_ILIM`, U3 ground thermal relief or L2/R402 courtyards.
- Two `5V_RADIO` shortcut routes toward E22 were rejected because they crossed `BOOST_FB`, SPI/control fanouts and E22 ground pins.
- The accepted 2026-07-28 `5V_RADIO` pass now connects U3 VOUT to E22 VCC, the feedback/output-cap island, C503 and the lower bulk capacitor bank with top-layer generated copper.
- `BOOST_COMP` is now routed locally after moving R404/C408 and nudging the `BOOST_FB` U3-side via.

Next strategy:

- Move the TPS61088 output capacitors and feedback divider as a group instead of one part at a time.
- Keep `5V_RADIO` as a deliberate high-current copper shape from U3 VOUT to E22 VCC and the local capacitor bank.
- Preserve the E22 control/SPI fanout corridors unless the whole radio/boost placement is reviewed.

Do not:

- Route `5V_RADIO` as a long skinny internal trace.
- Keep searching the immediate U3 underside for C405 without moving EN/FSW/ILIM support routing.

## Cluster B: BQ25798 Charger Power Stage

Remaining nets:

- `BQ_VBUS`
- `BQ_SW2`
- `SOLAR_PROTECTED`
- `USB_VBUS_RAW`

Current status:

- `BQ_SW1` is now routed with an accepted left-side wrap from U1/C216 to L1.
- A trial moving only L1 above U1 was rejected because it collided with the accepted TPS61088 input-cap cluster and U1 support passives.
- A direct `BQ_SW1` top route lowered the ratsnest count but failed badly by running down the U1 left pad row.
- `BQ_PMID` is now routed with a lower U1 fanout, B.Cu bridge and capacitor-bank entry; preserve it unless the full lower-edge charger fanout is replanned.
- `BQ_SW2` remains coupled to C217 placement and the U1 right-side escape.
- Recent `BQ_SW2` trials show that the accepted `BQ_SYS` entry, C218/`BQ_SDRV`, R203/R204, `BQ_TS` and Q3 selector pads must be replanned together; shifting only the SYS via or drawing a right-side overpass causes shorts or solder-mask bridges.
- `BQ_BTST2` is now routed with an accepted top-layer dogleg after straightening the local `BQ_PROG` route.

Next strategy:

- Keep the accepted L1 location unless the whole charger quadrant is replanned; moving only L1 upward has already failed.
- Treat C217, C218, R203/R204, `BQ_TS` and `BQ_SW2` as a shared U1 right-side fanout problem. `BQ_REGN`, `BQ_PMID` and `BQ_BTST2` are now routed and should be preserved during any grouped refactor.
- Move BQ25798 VBUS/PMID capacitor banks nearer U1/Q2/Q3 only as part of a grouped capacitor/passive placement pass.

Do not:

- Run wide switch-node traces down the U1 pad row.
- Add one-off vias beside U1 pads 1-9 or 17-20.

## Cluster C: BQ25798 Local Regulation And Sense

Remaining nets:

None in the current ratsnest list.

Current status:

- `BQ_REGN` C215/R200 island-to-U1-pin-5 routing and ILIM_HIZ/U1-pin-17 top bridge are now accepted; `BQ_REGN` is no longer in the remaining ratsnest list.
- Earlier `BQ_REGN` pin-to-pin bridge trials lowered the count but shorted/crowded `BAT_RAW`, `BQ_TS`, `BQ_BTST1` and I2C corridors.
- A top-layer REGN wrap also failed because the U1 perimeter is already occupied by ACDRV, I2C, TS and ground-thermal relief.
- `BATP_KELVIN` is now accepted as a routed low-current sense branch from U1 BATP to R202.
- R202 tight-local relocation at U1 was also rejected because the 0603 footprint overlaps/crowds the U1 right-side support-passive escape.

Next strategy:

- Preserve the accepted R202/BATP sense branch while reworking any adjacent TS/support-passive placement.
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
  1. Preserve the accepted BQ_SW1 left-wrap unless a full charger-quadrant refactor replaces it.
  2. Re-stage C217/C218/R203/R204 around the U1 right-side escape.
  3. Re-test BQ_SW2 while preserving the accepted BQ_BTST2 dogleg.
  4. Only then retry the U1-side service-power entries while preserving BQ_PMID, BQ_REGN and BATP_KELVIN.
```

This should reduce several remaining unrouted items while improving the actual
charger power-loop geometry.

Detailed coordinates and trial constraints for this pass are tracked in
`docs/U1_RIGHT_SIDE_REFACTOR_REV_A.md`.
