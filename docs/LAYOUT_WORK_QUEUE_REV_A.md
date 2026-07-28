# Layout Work Queue Rev A

RoyalNode Rev A now has a clean generated-routing checkpoint with 4 expected unrouted ratsnest items. This work queue translates the generated summary into the next layout passes.

Use this sequence rather than routing random ratsnest lines.

Regenerate the PCB scaffold with:

```text
make generate-board
```

Do not run placement and route generation in parallel; both commands rewrite `RoyalNode.kicad_pcb`.

## Current Gate

```text
make layout-status
```

Current result:

- ERC: 0 violations
- DRC: 0 active violations/warnings; `lib_footprint_mismatch` is ignored by project policy for tracked local release-candidate footprints
- Unrouted: 4 ratsnest pairs

## Pass 1: Placement Blockers

Resolve these before routing more long traces:

1. Finalize or replace the edge-launch SMA footprint and RF launch geometry.
2. Preserve the accepted BQ25798 `BQ_REGN`/`ILIM_HIZ` local fanout during nearby charger rework.
3. Rework the protection-divider ground escape around `OV_NODE` and the accepted control-routing corridor.
4. Confirm XT30 connector polarity, board-edge access, and mating-plug clearance.
5. Re-route J6 only after confirming the new top-edge service clearance remains acceptable.

## Pass 2: Ground System

`GND` is now handled by generated top copper and Layer-2 reference pours. Do not replace the remaining ground/fanout work with skinny traces.

Planned work:

- Add functional stitching vias near grounded IC pads and connector grounds.
- Extend or shape local ground copper where it does not break RF or switch-node discipline.
- Keep Layer 2 as the uninterrupted ground reference.
- Add E22 ground via stitching only after the RF/SMA launch decision is stable.

## Pass 3: Charger Power Path

Route remaining charger/service power as deliberate copper after placement review:

- `BQ_VBUS`
- `SOLAR_PROTECTED`

Preserve the accepted `BQ_SYS`, `BQ_PMID` and `SOLAR_FUSED` routes unless a grouped power-stage refactor replaces them.

These nets should not be completed as narrow generated traces.

The 2026-07-25 `BQ_VBUS` Q2 and Q3 duplicate-drain islands are now joined with internal-layer bridges from each left D2 pad to the existing right-side `BQ_VBUS` backbone. An outside-left Q3 bridge trial was rejected because it crossed the accepted `BQ_ACDRV2` and `BQ_USB_SELECTOR_COMMON` routing corridors.

The 2026-07-25 `SOLAR_PROTECTED` Q1 duplicate-drain island is now joined with an internal-layer bridge from the left protected-output pad to the existing protected-output spine. The first right-side via location was rejected for crowding `SOLAR_PROT_COMMON`; the accepted via lands lower on the protected-output spine to clear both `SOLAR_PROT_COMMON` and `BOOST_EN`.

The 2026-07-25 `SOLAR_PROTECTED` U4 protected-output sense branch is now routed with a short top-layer fanout from U4 and an internal-layer bridge into the Q1 protected-output island. The first U4 via-in-pad location was rejected for no-net pad and hole-clearance issues; the accepted route moves the via off-pad and left of the `SOLAR_PROT_COMMON` via.

A 2026-07-25 `SOLAR_PROTECTED` U1-entry trial from the Q1 protected-output spine was rejected. The U1-side via crowded/shorted the `BQ_ACDRV2` lower-row pad, and the internal-layer approach crossed the accepted `BQ_VBUS` and I2C corridors. Keep the remaining `SOLAR_PROTECTED` U1 connection blocked until the U1 lower-edge fanout is reworked as a group.

A 2026-07-26 `SOLAR_PROTECTED` U1-entry retry from the accepted Q1/Q2 island
was rejected. The U1 fanout crossed/crowded `BQ_STAT`, the internal span
crossed the accepted `BQ_SYS` spine, and the selector-side approach shorted
against the `BQ_SOLAR_SELECTOR_COMMON` via. Keep this connection in the
lower-edge U1/input-selector placement pass.

A 2026-07-25 `BQ_VBUS` Q3-to-U1 bridge trial was rejected. The U1-side via/fanout crowded `BQ_STAT` and `BQ_BTST1`, while the back-layer route crossed accepted `BQ_STAT` and I2C paths. Keep the remaining `BQ_VBUS` U1 connection blocked until the U1 lower-left fanout is reworked as a group.

A 2026-07-26 `BQ_VBUS` cap-bank-to-U1 inner-layer retry was rejected. The U1
fanout shorted/crowded `BQ_STAT` and crossed `BQ_BTST1`; the cap-bank approach
crossed the `BQ_PMID` via, crossed the accepted `BQ_SYS` spine and left a
dangling inner segment. Rework the U1 lower-left pins and the VBUS/PMID cap
bank together rather than drawing another direct bridge.

A 2026-07-26 `BQ_VBUS` cap-bank-to-U1 route after the accepted REGN pin-5
route was also rejected. The U1 fanout shorted into the new `BQ_REGN` escape
and BAT_RAW inner trace, while the cap-bank side crossed `BQ_PMID` and the
accepted `BQ_STAT` back-layer corridor. Keep VBUS in the same U1 lower-edge
and capacitor-bank placement pass as PMID/STAT/REGN.

A 2026-07-26 `BQ_VBUS` U1-to-Q3 In2.Cu bridge trial after the larger outline
was rejected. The U1-side via and internal run shorted or crossed ACDRV2,
BTST1, SYS, STAT and I2C corridors. Do not retry this as a direct U1-to-Q3
internal bridge; it needs a grouped U1 lower-edge refactor.

A 2026-07-28 `BQ_VBUS` capacitor-bank-to-U1 route is accepted. The route uses
an allowed 0.50/0.25 mm via near U1, a B.Cu corridor back to the VBUS capacitor
bank, an In2.Cu detour for the low-current `BQ_STAT` return, and a slight
leftward jog of the local `BQ_BTST1` route. This removes the VBUS cap-bank
ratsnest item while keeping DRC clean. The remaining `BQ_VBUS` item is the
Q3 selector-side connection to U1.

The 2026-07-25 `BQ_SYS` capacitor-bank-to-U1 entry is now routed with an internal-layer spine from the SYS capacitor island and a short top-layer entry into U1 pad 25. The accepted via was nudged left to clear the nearby `BQ_SDRV` route.

The 2026-07-25 `BQ_SYS` L2-to-SYS-spine route is now routed with a short top-layer L2 fanout and a wider internal-layer branch into the accepted SYS spine. This leaves the U3 VIN/input-cap connection as the main remaining boost-input power-loop item.

The 2026-07-25 `BQ_SYS` U3 VIN-to-L2 spine branch is now routed with a compact top-layer U3 fanout and an In1 branch into the L2/SYS spine. Intermediate trials hit BOOST_EN, I2C/E22 internal routes, BOOT clearance and C407 ground thermal starvation; the accepted via lands lower/left enough to keep C407's ground thermal intact.

A 2026-07-25 `BQ_SYS` boost-input-cap-to-U3 spine corridor trial was rejected. In1 crossed `BOOST_FB` and crowded `BOOST_EN`; In2 avoided those but crossed E22 reset/RXEN and the XIAO/I2C service corridor; B.Cu crossed `SPI_SCK`, I2C and the XIAO through-hole row with solder-mask issues. Keep the remaining boost-input connection as a placement/copper-pour pass rather than a long straight corridor.

The 2026-07-25 TPS61088 input-cap placement pass moved C400, C401 and C404 from the remote placeholder boost row into the local U3/L2 input area. C400/C401 now form a local `BQ_SYS` bulk-cap bus below L2, and C404 is placed as the local high-frequency bypass. The accepted top-layer copper removes `BQ_SYS` from the unrouted list while keeping DRC clean.

## Pass 4: Switch Nodes

Route only after BQ25798 and TPS61088 placement is compact:

- `BQ_SW1`
- `BQ_SW2`
- `BOOST_SW`

The current layout ties the adjacent TPS61088 switch pins into L2 with compact local top-layer copper. C406 and R402 have been moved into the boost-stage neighborhood and their BOOT/FSW switch-node branches are routed. The remaining boost support passives still need a grouped placement pass.

C216 is now relocated below U1 with `BQ_BTST1` and the local capacitor side of `BQ_SW1` routed. The remaining `BQ_SW1` ratsnest item is the inductor/power-loop path, not the bootstrap-cap connection.

C217 is now staged beside the charger power stage and its local `BQ_SW2` side is tied to L1. The companion `BQ_BTST2` escape is now routed with a top-layer dogleg after straightening the local `BQ_PROG` route. Keep future C217 work focused on the remaining `BQ_SW2` U1-to-L1 span.

A direct 2026-07-25 `BQ_SW2` U1-to-L1 top-layer span was rejected because it crossed the U1 `I2C_SCL`/ground pad row and the accepted SCL fanout. The remaining `BQ_SW2` power-loop connection needs a coordinated U1 escape, not a vertical trace through the lower pad row.

A later 2026-07-25 `C217` move to the lower-right of U1 was rejected. It worsened the ratsnest count, overlapped the L1 courtyard, swapped the intended `BTST2`/`SW2` pad approach after rotation, and crossed/shorted the accepted `BQ_TS` via corridor. Keep `C217`, `BQ_TS`, `BQ_REGN` and the U1 right-side escape as one placement pass.

A later 2026-07-25 `BQ_SW2` trial that shifted the accepted `BQ_SYS` U1-entry via rightward was rejected. The SYS shift collided with `BQ_SDRV`, and the SW2 overpass/drop beside Q3 shorted or mask-bridged against the USB selector pads. Keep SW2 blocked until the SDRV/PROG/TS/Q3 service corridor is replanned as a group.

A 2026-07-25 direct `BQ_SW1` U1-to-L1 top-layer route was rejected. It dropped the ratsnest count but ran down the U1 left pad row, shorting/crowding `BQ_STAT`, `BQ_VBUS`, `BQ_BTST1`, `BQ_REGN`, `USB_VBUS_RAW` and `SOLAR_PROTECTED` pads. Move/refactor the L1/U1 switch-node placement before retrying `BQ_SW1`/`BQ_SW2`.

A 2026-07-26 grouped `BQ_BTST2`/C217/R203 refactor was rejected. It briefly
reduced the ratsnest count, but placing C217 near the U1 right edge and moving
R203 into that same corridor produced `BQ_BTST2`/`BQ_PROG`, `BQ_PROG`/`BQ_TS`
and `BQ_SW2`/`BQ_PROG` crossings or shorts depending on the PROG escape layer.
The temporary C217/R203 placement and orphaned PROG stub are retired. Keep the
next BTST2 attempt as a broader right-side U1 refactor that includes TS, PROG,
INT, SW2 and the nearby selector/service routes.

A later 2026-07-26 `BQ_SW2` right-side spine from U1 pad 26 to the existing
C217/L1 island was also rejected. The vertical corridor beside U1 shorts or
mask-bridges against `BQ_SYS`, `BQ_TS`, `BQ_INT`, `BQ_PROG` and the accepted
I2C fanout. Do not route SW2 down the U1 right pad row without first moving
TS/PROG/INT/I2C support routing out of that channel.

A 2026-07-25 trial moving L1 above U1 was rejected. The topology would shorten the switch nodes, but in the current floorplan it collides with the accepted TPS61088 `BQ_SYS` input-cap cluster, C216/C218 support passives and the accepted U1 `BQ_SYS`/`BQ_SDRV` escape routes. Do not move only L1 upward; the charger power stage needs a broader floorplan change with the boost input-cap cluster and U1 support passives considered together.

A 2026-07-25 long `UV_NODE` bottom-layer route was rejected. It collided with the fused-solar U4 via, crossed the accepted I2C/SPI corridors, and clipped the XIAO through-hole row. Treat the protection-divider sense nets as a U4/divider placement pass rather than long board-spanning traces.

## Pass 5: Remaining Sense And Control Nets

Route after nearby placement is stable:

- `BQ_TS`
- `BQ_PROG`
- `BQ_INT`
- `LTC_SHDN`
- `UV_NODE`
- `OV_NODE`
- `NTC_SENSE`

These should avoid switch-node copper and RF launch copper.

`BQ_SDRV` is now locally routed after relocating C218 near U1 and sliding it left to clear the accepted 3.3 V pullup route.

## Hold Items

- Do not add test points, current shunts, probe loops, or bench-only measurement links.
- Do not route `RF_915` until the SMA footprint and stack-up are final per `docs/RF_STACKUP_PLAN_REV_A.md`.
- The 2026-07-25 Molex product-page recheck keeps `732511150` selected, but does not release the footprint. The sales drawing/recommended launch geometry is still required.
- `BOOST_EN` is now routed through the accepted control corridor. Two earlier R405 relocation trials near the TPS61088 EN pin were rejected: one collided with the E22 SPI pad/courtyard corridor and one collided with the E22_NSS route/via corridor.
- A TPS61088 small-passive relocation trial that moved C405/C406/C407/C408 and R400/R401/R402/R403/R404 into the immediate U3 top/left corridor was rejected on 2026-07-25. It shorted into the existing E22_NSS/SPI fanout, overlapped the E22 courtyard and collided with the L2 inductor courtyard. Treat the boost support network as requiring a U3/L2 placement shift or a bottom-side/local-via strategy, not a simple top-side shove toward the E22.
- Two 2026-07-25 `BOOST_FB` divider-only relocation trials were rejected. A left/below-U3 placement collided with the E22 SPI/MISO edge and MOD2 courtyard; a lower/right-U3 placement shorted against TPS61088 ground/exposed-pad geometry and the `5V_RADIO` side of R400. Keep `BOOST_FB` blocked until the TPS61088 small-passive strategy is reworked as a group.
- The accepted 2026-07-25 U3/L2 rotation puts TPS61088 VOUT toward the E22 5 V entry and BOOST_SW toward the XAL7030 inductor. Continue boost placement from this topology.
- A 2026-07-25 `BQ_SW1` left-wrap route from U1/C216 to L1 is accepted. It leaves the U1 top edge through the existing bootstrap corridor, wraps outside the left side of U1, and enters the L1 SW1 pad without new DRC violations.
- A 2026-07-25 `5V_RADIO` U3-to-E22 internal-layer branch trial was rejected. The In1 shortcut crossed/crowded the accepted `SPI_SCK` via and `BOOST_FB` tracks, the U3 top fanout crowded a no-net U3 pad, and the via collided with the accepted E22 `DIO1`/`BUSY` internal routing columns. Keep the radio rail as a deliberate high-current copper corridor or pour after the boost/passive placement is reviewed, not as a long internal trace shortcut.
- A later 2026-07-25 lower `5V_RADIO` corridor trial from U3 toward the E22 VCC pads was rejected. The E22-side entry shorted/crowded MOD2 GND pin 11, the lower corridor collided with accepted E22 `BUSY`/`RXEN` fanouts, and the U3-side via crowded `BOOST_FB`. The radio rail needs a deliberate E22/U3 power-copper placement pass, not a lower-layer shortcut.
- A 2026-07-25 C503 radio-bulk-cap relocation trial was rejected. Placing the polymer can left of MOD2 electrically reduced the ratsnest, but the body could not clear both the board edge and the E22 module courtyard; moving it into the lower capacitor bank collided with J4/edge silk or left a dangling route and did not improve the accepted count. Keep C503 at the legal scaffold location until the radio bulk-cap bank is mechanically replanned.
- A 2026-07-25 local `BQ_REGN` U1 pin-5-to-pin-17 bottom bridge trial reduced the ratsnest count by one but was rejected. The U1-side vias shorted/crowded the accepted `BAT_RAW`, `BQ_TS`, `BQ_BTST1` and I2C corridors around the HOTROD package. Rework the REGN/TS/BATP local passive and U1 escape cluster together instead of adding vias beside the existing U1 fanout.
- A 2026-07-25 top-layer `BQ_REGN` wrap around U1 was rejected. It connected the pins electrically but crossed/crowded `BQ_ACDRV1`, `BQ_ACDRV2`, I2C and `BQ_TS`, and starved U1 ground thermal relief. Keep REGN out of the existing U1 perimeter routes until that support-passive cluster is rearranged.
- A 2026-07-25 `SOLAR_PROTECTED` U4-sense branch trial was rejected. The left-side route crossed the accepted `SOLAR_PROT_GATE` path; the right-side route crossed the fused-solar back-layer hop or collided with the XIAO battery-isolation route. Treat U4 protected-output sensing as a placement/pour-level follow-up, not a casual single-trace route.
- `BOOST_SS` is now locally routed after relocating C407 above U3 and shifting the BOOT route right to clear the capacitor ground pad.
- 2026-07-25 `BOOST_VCC` / C405 placement trials below U3 were rejected. The rotated trial put the VCC pad away from U3, starved the U3 top-ground thermal relief and introduced an extra library-mismatch warning. The non-rotated 0805 trial shorted against the FSW route and overlapped U3/L2 courtyards. Revisit C405 with a coordinated U3/L2/FSW placement pass instead of a quick shove below the IC.
- A later 2026-07-25 C405 local-placement retry below U3 was rejected in both orientations. The 180-degree version shorted C405 ground into `BOOST_ILIM`; the 0-degree version shorted/crowded `BOOST_FSW`, R402 and the L2 courtyard. Keep `BOOST_VCC` in the grouped TPS61088 support-passive pass.
- A subsequent 2026-07-25 C405 offset-left retry was also rejected. It crowded the U3 exposed ground pad/thermal relief and collided with `BOOST_EN`, `BOOST_FSW`, R402 and the local solder-mask constraints. Do not keep searching the immediate U3 underside for C405; move the surrounding EN/FSW/ILIM support cluster or open a new bottom-side strategy.
- A later 2026-07-25 `BOOST_VCC` direct route trial from U3 to C405 was rejected. The U3-side fanout shorted/crowded U3 ground and exposed-pad geometry, the internal route crossed `BOOST_EN`, and the C405-side via collided with the accepted SPI corridor. Keep `BOOST_VCC` blocked until U3 support-passive placement is reworked.
- 2026-07-26 bottom-side C405/`BOOST_VCC` trial was rejected. Placing C405 below U3 created pad-orientation ambiguity, shorted/crowded U3 exposed ground and C405 ground geometry, starved the U3 ground thermal and introduced bottom-side text/footprint warnings. Do not use a bottom-side C405 exception at the current U3 location; solve BOOST_VCC with a broader U3 support-passive placement pass.
- A 2026-07-26 C405 local-bypass placement trial below U3 after the larger
  outline was rejected. Even with pad 1 aligned under U3 VCC, C405 crowded
  BOOST_EN, BOOST_ILIM, FSW/R402, L2 or U3 ground thermal depending on
  orientation. Keep `BOOST_VCC` in the grouped TPS61088 EN/ILIM/FSW/support
  passive placement pass.
- A later 2026-07-26 vertical C405 trial after the accepted compensation
  placement was also rejected. The 0805 body still overlapped U3/R402
  courtyards, the ground pad shorted or crowded `BOOST_EN`/`BOOST_FSW`, and
  the top ground thermal was starved. The generated trial segment is retired.
- A follow-up 2026-07-26 0603 C405 package trial briefly reduced the ratsnest
  count to 10, but no checked placement produced a clean layout. The upper
  pocket shorted/crowded the U3 ground pad and U3 courtyard; the lower pocket
  starved U3 ground thermal relief and overlapped R403; moving R403 downward
  hit the accepted `BOOST_COMP` and E22 `BUSY` corridors. Keep C405 as the
  locked 0805 part until the whole TPS61088 EN/FSW/ILIM/VCC support cluster is
  replanned.
- A 2026-07-28 C405 local-placement retry to the right of U3 removed the
  `BOOST_VCC` ratsnest but was rejected. The route crossed `BOOST_EN`,
  crowded `BOOST_FSW`, overlapped U3/L2 courtyards and solder-mask-bridged
  into the switch-node area.
- A later 2026-07-28 lower C405 retry below U3 briefly removed the
  `BOOST_VCC` ratsnest but was rejected. C405 still crowded `BOOST_EN`, R403
  and U3 silk/thermal geometry; moving `BOOST_EN` and R403 to compensate broke
  the accepted boost support routing and introduced new shorts.
- A later 2026-07-28 TPS61088 support-pocket refactor is accepted. C405 now
  sits below U3 with a short top-layer `BOOST_VCC` bypass route, R403 moves
  lower-left with an ILIM layer hop around `BOOST_COMP`, and R404 moves lower
  to preserve compensation clearances. The U3 reference field is hidden in the
  local release-candidate footprint to avoid silkscreen over the new bypass
  capacitor. This removes `BOOST_VCC` from the remaining ratsnest while
  keeping DRC clean.
- A 2026-07-28 `5V_RADIO` trial from U3 VOUT to the upper output-cap/sense
  island reduced the radio ratsnest count by one, but every tested internal
  layer crossed accepted routes: `In2.Cu` crossed E22 reset/DIO1 control,
  `In1.Cu` crossed `BOOST_EN`/`BOOST_FB`, and `B.Cu` crossed the SPI bus.
  Route the radio rail only after a grouped boost/E22 signal-corridor review.
- A 2026-07-25 `BOOST_COMP` internal-layer route trial from U3 to R404 was rejected. The U3-side via and top fanout crowded `BOOST_FB`, while shifted variants collided with the accepted E22 `BUSY`/`DIO1`/`NRST` internal routing columns or required tracks below the 0.15 mm rule. This is superseded by the accepted 2026-07-26 grouped compensation placement.
- A 2026-07-25 `USB_VBUS_RAW` right-edge service-route trial from MOD1 to Q3 was rejected on all tried layers. In1 crossed `BOOST_EN`; In2 crossed `BAT_RAW`, 3.3 V and I2C service routes; B.Cu crossed `XIAO_BAT_ISO`, `BQ_VBUS` and I2C. Keep `USB_VBUS_RAW` blocked until the right-edge service corridor is reworked or Q3/MOD1 placement changes.
- 2026-07-25 `BOOST_COMP` R404/C408 relocation beside U3 was rejected. The left-of-U3 corridor collided with the E22 module's SPI_MOSI pad/via and MOD2 courtyard, while the tighter vertical placement shorted the compensation RC node into adjacent pads. Keep TPS61088 compensation as part of a full U3/MOD2 corridor pass.
- 2026-07-26 `BOOST_COMP` bottom-layer route from U3 to R404 was rejected. The U3-side via violated clearance to the accepted `BOOST_FB` via, and the R404 entry crossed the existing `BOOST_COMP_RC` route, shorting the compensation pin to the RC node. Do not retry this corridor unless `BOOST_FB` and the compensation RC placement are reworked together.
- 2026-07-26 `BATP_KELVIN` right-side escape trials were rejected. The U1 escape via collided with nearby `BQ_REGN`, `I2C_SDA`, `BAT_RAW` and the accepted 3.3 V service corridor depending on layer and offset; B.Cu and In1/In2 long runs also crossed existing `BQ_SYS`, `BAT_RAW`, I2C or `BQ_TS` corridors. Keep BATP blocked until the U1 support-passive group and service routes are replanned together.
- 2026-07-26 post-REGN `BATP_KELVIN` left-escape retest was rejected. The route crowded the accepted REGN via/bridge, crossed BAT_RAW on B.Cu, shorted/crowded U1 SOLAR_PROTECTED/GND/ACDRV pads and left a dangling R202-side end. The later accepted BATP route uses a different U1 escape, B.Cu dogleg and In2.Cu hop around the existing BAT_RAW/NTC corridors.
- 2026-07-26 C217 near-U1 rotation trial was rejected. Pulling the BTST2/SW2 bootstrap cap into the U1 right-side gap shorted/crowded `BQ_SDRV`, `BAT_RAW`, `BQ_PROG`, R203/R204, Q3 and solder-mask rules, and increased the ratsnest count. C217 needs a broader U1-right-side refactor, not a simple local move into the existing support-passive gap.
- 2026-07-26 `BQ_REGN` C215/R200 island-to-U1-pin-5 route is accepted. The route leaves U1 pin 5 with a short left-side jog to avoid unused U1 pad 6, then runs on B.Cu back to C215/R200. This reduced the ratsnest from 16 to 15 and set up the later ILIM_HIZ top bridge.
- 2026-07-26 `BQ_REGN` ILIM_HIZ/U1-pin-17 bridge trial was rejected. A direct right-side via shorted/crowded the accepted `BQ_TS` via and I2C lane; shifting the TS via right then collided with R203/`BQ_PROG`, the 3.3 V service route and solder-mask rules. Keep ILIM_HIZ blocked until the TS/PROG/right-side U1 support cluster is replanned together.
- 2026-07-26 `BQ_REGN` ILIM_HIZ/U1-pin-17 top-layer bridge is accepted. The route ties U1 pin 17 to the accepted REGN pin-5 escape without adding vias, avoiding the TS via-hole conflict from the rejected right-side ILIM trial and reducing the ratsnest from 15 to 14.
- A 2026-07-25 `BQ_SYS` U3-VIN-to-L2 input hop trial was rejected. It crossed the accepted BOOT branch and crowded the L2 BOOST_SW pad. Route this as a deliberate boost-input copper shape after the BOOT/VIN/passive strategy is reviewed.
- A 2026-07-25 `USB_VBUS_RAW` XIAO-to-Q3 right-side route trial was rejected. The outside path hit the XT30/J1 no-net mechanical pad; the inward path crossed I2C, XIAO_BAT_ISO or fused-solar back-layer tracks. Revisit USB_VBUS_RAW with a deliberate layer-transition plan.
- A 2026-07-26 `BOOST_COMP` perimeter-route trial after adding the larger mechanical outline was rejected. The R404-side via collided with R405/GND, the bottom route crossed the existing SPI_SCK bus, and the U3-side via crowded BOOST_FB/E22_BUSY. This is superseded by the accepted 2026-07-26 grouped compensation placement.
- A later 2026-07-26 grouped compensation pass is accepted. R404 is now staged below-right of U3 at 60.2, 62.8 mm, C408 is staged at 63.6, 62.8 mm, the `BOOST_FB` U3-side via is nudged to 56.60, 55.55 mm, and `BOOST_COMP`/`BOOST_COMP_RC` are routed locally on top copper. This reduces the ratsnest from 12 to 11 without adding DRC errors.
- A 2026-07-26 top-edge `USB_VBUS_RAW` retry from MOD1 to Q3 reduced the
  ratsnest count but was rejected. The first horizontal exit crossed the 3.3 V
  pullup area; offset variants collided with the R204 3.3 V service spine,
  XT30/J1 mechanical PTHs or C503 ground/body clearance. Treat this as a
  placement/corridor issue around MOD1/J1/C503, not a simple edge trace.
- A follow-up 2026-07-26 B.Cu edge route for `USB_VBUS_RAW` was also rejected.
  It crossed accepted `BQ_VBUS`, `XIAO_BAT_ISO` and I2C_SDA service routes.
  Keep USB raw routing blocked until the right-edge service corridor is
  replanned.
- A 2026-07-28 `USB_VBUS_RAW` U1-to-Q3 bottom-edge service-route trial was
  rejected. It reduced the ratsnest count temporarily, but crossed or crowded
  `BQ_ACDRV2`, `BQ_VBUS`, `XIAO_BAT_ISO`, `NTC_SENSE`, `BATP_KELVIN` and
  `BQ_REGN`. The remaining U1 USB input connection needs the same grouped
  U1/Q3/service-connector refactor as `BQ_VBUS`.
- After moving the right-edge 3.3 V service leg to `In2.Cu`, a 2026-07-26
  top-edge `USB_VBUS_RAW` route from MOD1 5V to Q3 pads 7/8 is accepted. This
  removes the MOD1-to-Q3 USB ratsnest item; the remaining `USB_VBUS_RAW` item
  is the Q3-to-U1 sense/input connection.
- A 2026-07-26 Q3-to-U1 `USB_VBUS_RAW` bottom-layer sense-route trial was
  rejected. Lower routing crossed I2C_SCL, `BQ_ACDRV2` and
  `BQ_USB_SELECTOR_COMMON`; a farther-right variant crossed the `BAT_RAW`
  trunk and crowded `BQ_VBUS`. Keep the remaining USB raw U1 connection in the
  lower-edge U1 fanout refactor.
- A later 2026-07-26 top-layer Q3-to-U1 `USB_VBUS_RAW` service-corridor trial
  was also rejected. The U1 exit crossed `BQ_REGN`, `BQ_ACDRV1`,
  `BQ_ACDRV2`, I2C_SDA/SCL and the Q3-side `BQ_VBUS` via. The generated trial
  segment is retired.
- 2026-07-28 `USB_VBUS_RAW` U1-to-Q3 service trials briefly reduced the
  ratsnest count by one but were rejected. The U1 fanout crowded `BQ_REGN` or
  `SOLAR_PROTECTED`, while the tested `In1.Cu`, `In2.Cu` and `B.Cu`
  backbones crossed `BQ_ACDRV2`, `BQ_TS`, 3.3 V, `BAT_RAW`, `BATP_KELVIN`,
  `BQ_VBUS` or NTC routes.
- A BQ25798 right-side TS-divider relocation trial was rejected because it shorted `BQ_TS` to `BQ_REGN` and violated U1/capacitor courtyards. Treat `BQ_REGN`/`BQ_TS` as a compact HOTROD-package placement pass, not as a generic passive-grid cleanup.
- A 2026-07-25 `BQ_PROG`/`BQ_INT` direct top-layer routing trial was rejected because it crossed the lower charger/passive staging area and caused shorts, solder-mask issues and thermal relief starvation. Route these only after the lower charger support passives are placed deliberately.
- A 2026-07-25 `BQ_BTST2` direct top route and a follow-up two-via escape trial were rejected. The top route shorted/crowded `BQ_PROG`; the via route crowded BATP/PROG pad clearance and crossed existing `I2C_SDA`, `BAT_RAW` and `BQ_TS` corridors. Keep `BQ_BTST2`, C217 and the U1 right-side support passives in the same placement pass.
- 2026-07-28 `BQ_BTST2` dogleg trials showed the top-layer lane between
  `BQ_TS` and `BQ_PROG` is too narrow at the current 0.15 mm minimum trace
  width. Moving the `BQ_TS` via left collided with the accepted `I2C_SDA` and
  `BQ_REGN` escape region, bending `BQ_PROG` below the lane crowded `BQ_INT`,
  and moving C217 near U1 collided with the surrounding `BAT_RAW`,
  `BATP_KELVIN`, `BQ_SDRV`, `BQ_PROG`, `BQ_INT`, R203/R204 and Q3 routes.
- A later 2026-07-28 `BQ_BTST2` pass is accepted. The `BQ_PROG` local trace
  was straightened into R203, and `BQ_BTST2` now uses a legal top-layer dogleg
  from U1 to C217 without new DRC violations.
- A 2026-07-25 lower-edge `BATP_KELVIN` route trial was rejected because the U1-side via crowded neighboring BQ25798 pads and the bottom route crossed existing lower sense/I2C routing. Treat `BATP_KELVIN` as requiring a deliberate U1 escape and sense-routing pass, not a casual bottom-edge route.
- A 2026-07-25 U4-side `UV_NODE`/`OV_NODE`/`LTC_SHDN` divider relocation trial was rejected because it crowded the LTC4365 pins, overlapped the L2 inductor courtyard and shorted the divider nodes into adjacent U4/L2 nets. Rework U4, L2 and the divider corridor together before pulling these protection passives closer.
- A 2026-07-26 `R204` 3.3 V pullup-feed reroute is accepted. It uses a short
  local via into the existing `In2.Cu` 3.3 V spine and clears the top-side U1
  right corridor. Earlier bottom-layer and `In1.Cu` attempts were rejected for
  I2C/USB crowding or crossing `BQ_ACDRV1`.
- The right-edge 3.3 V service leg has also been moved from top copper to
  `In2.Cu`, rejoining the top 3.3 V service route near 90.4, 36.7 mm. This
  removes the x102.4 top-layer 3.3 V spine that blocked USB edge-route trials.
- A 2026-07-25 `BQ_VBUS` Q2/Q3 left-drain loop trial was rejected because top-layer loops around the MOSFET bodies shorted or crossed the adjacent `BQ_ACDRV1`/`BQ_ACDRV2` gate pads. Route the remaining FET drain joins with deliberate copper shapes or a revised FET placement, not a simple around-body trace.
- A 2026-07-25 rectangular `BQ_VBUS` copper-zone trial around Q3 passed DRC but did not connect Q3 pad 3 to pad 5, so it was removed. The selector drain joins need shaped copper or MOSFET placement changes, not a broad rectangular fill.
- A 2026-07-28 RF floorplan correction is accepted. MOD2/E22 was rotated to
  0 degrees so pin 21 ANT faces the left board edge, and J5's draft SMA
  envelope moved to the left edge near the ANT pad. The old E22 digital bus
  fanouts were reworked for the new orientation.
- A 2026-07-28 `E22_RXEN` route is accepted. It uses a short top-layer fanout
  from MOD2 pin 6 to a local via, then a bottom-layer escape to the XIAO D6
  pad, clearing the TPS61088 support-passive pocket without new DRC violations.
- A 2026-07-28 `5V_RADIO` route pass is accepted. U3 VOUT now feeds the E22
  VCC pins through a short top-layer power spine, ties into the output
  feedback/capacitor island, reaches the lower E22 bulk capacitor bank down
  the right side of the module, and connects C503 through the upper
  protection-divider corridor. This removes `5V_RADIO` from the remaining
  ratsnest while keeping DRC clean.
- A 2026-07-28 `BQ_SW2` top-layer escape trial and an internal-layer via
  escape trial both reduced the ratsnest count temporarily but were rejected.
  The top route crowded U1 `BQ_SYS`, `BQ_SDRV`, `BQ_TS` and I2C pads; the
  internal route crossed `BQ_TS`, `BQ_VBUS`, 3.3 V and `BQ_ACDRV2`. A later
  via-in-pad/inner-layer escape also closed the net electrically, but a
  rule-compliant via at U1 pad 26 crowded the adjacent `BQ_SYS` and GND pads.
- A follow-up 2026-07-28 grouped `BQ_SYS`/`BQ_SW2` pocket refactor was also
  rejected. Moving the `BQ_SYS` entry right opened the SW2 ratsnest but
  crowded `BQ_SDRV` and I2C; moving the SW2 via lower-left restored SYS but
  shorted or crowded the accepted SYS spines and I2C lane.
- A 2026-07-28 `BQ_VBUS` U1-to-Q3 bottom-layer bridge trial reduced the
  ratsnest count temporarily but was rejected because it crossed/crowded
  `BQ_STAT`, `BAT_RAW`, I2C_SDA and `BQ_USB_SELECTOR_COMMON`.
- A later 2026-07-28 `BQ_VBUS` U1-to-Q3 internal-layer escape trial was
  rejected. The U1-side via crowded the accepted `BQ_STAT` escape, and the
  internal path crossed I2C, 3.3 V, `BQ_TS` and `BQ_ACDRV2` service routes.
- A follow-up 2026-07-28 grouped `BQ_STAT` slide plus `BQ_VBUS` lower escape
  was also rejected. It opened the U1 VBUS lane only partially and then
  crossed/crowded `BAT_RAW`, `BATP_KELVIN`, `BQ_ACDRV1`, `BQ_ACDRV2`,
  `BQ_BTST1` and the shifted `BQ_STAT` entry. The remaining `BQ_VBUS` route
  needs a broader U1/Q3/L1 support-passive placement refactor, not another
  one-off bridge.
- A 2026-07-25 `SOLAR_PROTECTED` Q1 drain-join trial was rejected. The outside bottom bridge required a top-layer escape that crossed the accepted Q1 gate U-shape; moving the gate U-shape to the right shorted against Q1's no-net thermal/mechanical pad. Treat the Q1 protected-drain join as a FET-footprint/copper-shape pass.
- 2026-07-28 `SOLAR_PROTECTED` U1-entry retry briefly reduced the ratsnest
  count by one but was rejected. The internal route crossed accepted `BAT_RAW`
  and `BQ_SYS`, and the Q2-side via solder-mask-bridged into the selector
  common pad.
- A later 2026-07-28 `SOLAR_PROTECTED` U1-to-Q1 left-side service-route trial
  was rejected. It crossed or crowded `BQ_REGN`, `BQ_ACDRV2`, `BQ_STAT`,
  `BQ_PMID`, `I2C_SDA`, U3 ground/thermal geometry and
  `SOLAR_PROT_COMMON`. The remaining solar-protected U1 entry belongs in the
  same grouped U1/input-selector refactor as `BQ_VBUS` and `USB_VBUS_RAW`.
- A 2026-07-25 `BATP_KELVIN` bottom-layer sense-route trial was rejected. The R202-side via collided with the accepted `BAT_RAW` branch and `BQ_TS` route, the bottom span crossed `BQ_STAT`, and the U1-side via crowded `BQ_PROG`. Rework the BQ25798 support-passive fanout before retrying BATP.
- A 2026-07-25 R202 relocation trial for `BATP_KELVIN` was rejected. Moving R202 near U1 collided with the accepted I2C_SDA via corridor and crossed/shorted `BQ_TS`, `BQ_INT` and `BQ_PROG`; keep BATP as part of a coordinated right-side U1 fanout/sense-routing pass.
- A 2026-07-26 two-layer `BATP_KELVIN` sense route is accepted. It uses a short U1 escape, small signal vias, a B.Cu dogleg around the U1/I2C exits, and an In2.Cu hop around the BAT_RAW and NTC corridors before entering R202. This reduced the ratsnest from 14 to 13 without adding DRC errors.
- A 2026-07-26 `BQ_PMID` bridge is accepted. It uses a short lower U1 fanout, a B.Cu route under the charger area, and a top-layer entry into the PMID capacitor bus. A 64.00, 72.45 mm U1-side via clears the accepted `BQ_SW1` escape and reduces the ratsnest from 13 to 12 without adding DRC errors.
- A later 2026-07-25 R202 tight-local relocation at U1 was rejected. The rotated 0603 orientation put the BATP/BAT_RAW pads opposite the intended side, and the placement still overlapped U1 while crowding the accepted `BQ_TS`, `BQ_INT` and `BAT_RAW` vias. Keep R202 out of the U1 pad row until the right-side support-passive cluster is reworked.
- A 2026-07-25 `SOLAR_FUSED` divider-to-U4-backbone bridge trial was rejected because the straight bottom-layer span crossed the accepted SPI_SCK and I2C_SDA backbones. The remaining `SOLAR_FUSED` island needs a placement-aware reroute, not a long bottom trace through the digital corridor.
- A 2026-07-25 local `BQ_REGN` U1 pin-to-pin wrap trial was rejected because the QFN escape crossed neighboring routes and starved nearby thermal relief. The final accepted REGN solution uses the C215/R200 island route plus a short ILIM_HIZ top bridge instead of this wrap.
- A 2026-07-25 `BQ_ACDRV2` top-side gate route trial was rejected because the upper Q3 corridor crossed the accepted I2C_SDA/I2C_SCL fanout near U1. Route the selector gate controls as part of a coordinated U1 lower-edge escape pass.
- Do not force ground traces where a pour/stitching plan is required.
