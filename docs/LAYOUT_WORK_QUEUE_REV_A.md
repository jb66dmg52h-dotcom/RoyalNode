# Layout Work Queue Rev A

RoyalNode Rev A now has a clean generated-routing checkpoint with 24 expected unrouted ratsnest items. This work queue translates the generated summary into the next layout passes.

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
- DRC: 3 known footprint/library warnings, `MOD2`, `U3` and `L2`
- Unrouted: 24 ratsnest pairs

## Pass 1: Placement Blockers

Resolve these before routing more long traces:

1. Finalize or replace the edge-launch SMA footprint and RF launch geometry.
2. Rework BQ25798 `BQ_REGN`/`ILIM_HIZ` local fanout around the inductor and I2C exits.
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

Route as copper pours after placement review:

- `BQ_SYS`
- `BQ_PMID`
- `BQ_VBUS`
- `SOLAR_FUSED`
- `SOLAR_PROTECTED`

These nets should not be completed as narrow generated traces.

The 2026-07-25 `BQ_VBUS` Q2 and Q3 duplicate-drain islands are now joined with internal-layer bridges from each left D2 pad to the existing right-side `BQ_VBUS` backbone. An outside-left Q3 bridge trial was rejected because it crossed the accepted `BQ_ACDRV2` and `BQ_USB_SELECTOR_COMMON` routing corridors.

## Pass 4: Switch Nodes

Route only after BQ25798 and TPS61088 placement is compact:

- `BQ_SW1`
- `BQ_SW2`
- `BOOST_SW`

The current layout ties the adjacent TPS61088 switch pins into L2 with compact local top-layer copper. C406 and R402 have been moved into the boost-stage neighborhood and their BOOT/FSW switch-node branches are routed. The remaining boost support passives still need a grouped placement pass.

C216 is now relocated below U1 with `BQ_BTST1` and the local capacitor side of `BQ_SW1` routed. The remaining `BQ_SW1` ratsnest item is the inductor/power-loop path, not the bootstrap-cap connection.

C217 is now staged beside the charger power stage and its local `BQ_SW2` side is tied to L1. The companion `BQ_BTST2` escape remains blocked: a top-layer trial crossed/crowded `BQ_TS`, and a back-layer/via trial crowded the accepted `BQ_ACDRV1`, `BQ_TS` and `BQ_PROG` corridors. Treat the remaining bootstrap work as a U1 right-side escape pass.

A direct 2026-07-25 `BQ_SW2` U1-to-L1 top-layer span was rejected because it crossed the U1 `I2C_SCL`/ground pad row and the accepted SCL fanout. The remaining `BQ_SW2` power-loop connection needs a coordinated U1 escape, not a vertical trace through the lower pad row.

A 2026-07-25 `BQ_PMID` U1-to-cap-bus bridge trial was rejected. The direct top-layer route crossed the accepted C216 `BQ_BTST1` escape and crowded U1 `BQ_STAT`; the bottom-layer via variant still violated clearance at the dense U1 lower pad row. Treat `BQ_PMID` as a U1 power-copper/fanout pass.

A later 2026-07-25 `BQ_PMID` inner-layer retry after the BAT_RAW/BQ_STAT reroutes still failed. Centering the U1-side via crowded the accepted `BQ_SW1` escape, moving it left shorted into `BQ_STAT`, and shifting `BQ_SW1` right starved the U1 ground thermal while crowding `BQ_SW2`. Keep `BQ_PMID` blocked until the U1 lower-edge fanout is reworked as a group.

A 2026-07-25 long `UV_NODE` bottom-layer route was rejected. It collided with the fused-solar U4 via, crossed the accepted I2C/SPI corridors, and clipped the XIAO through-hole row. Treat the protection-divider sense nets as a U4/divider placement pass rather than long board-spanning traces.

## Pass 5: Remaining Sense And Control Nets

Route after nearby placement is stable:

- `BQ_TS`
- `BATP_KELVIN`
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
- A 2026-07-25 `SOLAR_PROTECTED` U4-sense branch trial was rejected. The left-side route crossed the accepted `SOLAR_PROT_GATE` path; the right-side route crossed the fused-solar back-layer hop or collided with the XIAO battery-isolation route. Treat U4 protected-output sensing as a placement/pour-level follow-up, not a casual single-trace route.
- `BOOST_SS` is now locally routed after relocating C407 above U3 and shifting the BOOT route right to clear the capacitor ground pad.
- 2026-07-25 `BOOST_VCC` / C405 placement trials below U3 were rejected. The rotated trial put the VCC pad away from U3, starved the U3 top-ground thermal relief and introduced an extra library-mismatch warning. The non-rotated 0805 trial shorted against the FSW route and overlapped U3/L2 courtyards. Revisit C405 with a coordinated U3/L2/FSW placement pass instead of a quick shove below the IC.
- 2026-07-25 `BOOST_COMP` R404/C408 relocation beside U3 was rejected. The left-of-U3 corridor collided with the E22 module's SPI_MOSI pad/via and MOD2 courtyard, while the tighter vertical placement shorted the compensation RC node into adjacent pads. Keep TPS61088 compensation as part of a full U3/MOD2 corridor pass.
- A 2026-07-25 `BQ_SYS` U3-VIN-to-L2 input hop trial was rejected. It crossed the accepted BOOT branch and crowded the L2 BOOST_SW pad. Route this as a deliberate boost-input copper shape after the BOOT/VIN/passive strategy is reviewed.
- A 2026-07-25 `USB_VBUS_RAW` XIAO-to-Q3 right-side route trial was rejected. The outside path hit the XT30/J1 no-net mechanical pad; the inward path crossed I2C, XIAO_BAT_ISO or fused-solar back-layer tracks. Revisit USB_VBUS_RAW with a deliberate layer-transition plan.
- A BQ25798 right-side TS-divider relocation trial was rejected because it shorted `BQ_TS` to `BQ_REGN` and violated U1/capacitor courtyards. Treat `BQ_REGN`/`BQ_TS` as a compact HOTROD-package placement pass, not as a generic passive-grid cleanup.
- A 2026-07-25 `BQ_PROG`/`BQ_INT` direct top-layer routing trial was rejected because it crossed the lower charger/passive staging area and caused shorts, solder-mask issues and thermal relief starvation. Route these only after the lower charger support passives are placed deliberately.
- A 2026-07-25 lower-edge `BATP_KELVIN` route trial was rejected because the U1-side via crowded neighboring BQ25798 pads and the bottom route crossed existing lower sense/I2C routing. Treat `BATP_KELVIN` as requiring a deliberate U1 escape and sense-routing pass, not a casual bottom-edge route.
- A 2026-07-25 U4-side `UV_NODE`/`OV_NODE`/`LTC_SHDN` divider relocation trial was rejected because it crowded the LTC4365 pins, overlapped the L2 inductor courtyard and shorted the divider nodes into adjacent U4/L2 nets. Rework U4, L2 and the divider corridor together before pulling these protection passives closer.
- A 2026-07-25 `R204` 3.3 V pullup-feed trial was rejected because the bottom route crossed the existing I2C spine and crowded the XIAO USB/5 V through-hole geometry. Treat remaining 3.3 V distribution as a logic-power spine pass, not a one-off long trace.
- A 2026-07-25 `BQ_VBUS` Q2/Q3 left-drain loop trial was rejected because top-layer loops around the MOSFET bodies shorted or crossed the adjacent `BQ_ACDRV1`/`BQ_ACDRV2` gate pads. Route the remaining FET drain joins with deliberate copper shapes or a revised FET placement, not a simple around-body trace.
- A 2026-07-25 rectangular `BQ_VBUS` copper-zone trial around Q3 passed DRC but did not connect Q3 pad 3 to pad 5, so it was removed. The selector drain joins need shaped copper or MOSFET placement changes, not a broad rectangular fill.
- A 2026-07-25 `SOLAR_PROTECTED` Q1 drain-join trial was rejected. The outside bottom bridge required a top-layer escape that crossed the accepted Q1 gate U-shape; moving the gate U-shape to the right shorted against Q1's no-net thermal/mechanical pad. Treat the Q1 protected-drain join as a FET-footprint/copper-shape pass.
- A 2026-07-25 `BATP_KELVIN` bottom-layer sense-route trial was rejected. The R202-side via collided with the accepted `BAT_RAW` branch and `BQ_TS` route, the bottom span crossed `BQ_STAT`, and the U1-side via crowded `BQ_PROG`. Rework the BQ25798 support-passive fanout before retrying BATP.
- A 2026-07-25 R202 relocation trial for `BATP_KELVIN` was rejected. Moving R202 near U1 collided with the accepted I2C_SDA via corridor and crossed/shorted `BQ_TS`, `BQ_INT` and `BQ_PROG`; keep BATP as part of a coordinated right-side U1 fanout/sense-routing pass.
- A 2026-07-25 `SOLAR_FUSED` divider-to-U4-backbone bridge trial was rejected because the straight bottom-layer span crossed the accepted SPI_SCK and I2C_SDA backbones. The remaining `SOLAR_FUSED` island needs a placement-aware reroute, not a long bottom trace through the digital corridor.
- A 2026-07-25 local `BQ_REGN` U1 pin-to-pin wrap trial was rejected because the QFN escape crossed neighboring routes and starved nearby thermal relief. Keep the two remaining `BQ_REGN` items in the BQ25798 support-passive fanout pass.
- A 2026-07-25 `BQ_ACDRV2` top-side gate route trial was rejected because the upper Q3 corridor crossed the accepted I2C_SDA/I2C_SCL fanout near U1. Route the selector gate controls as part of a coordinated U1 lower-edge escape pass.
- Do not force ground traces where a pour/stitching plan is required.
