# Layout Work Queue Rev A

RoyalNode Rev A now has a clean generated-routing checkpoint with 140 expected unrouted ratsnest items. This work queue translates the generated summary into the next layout passes.

Use this sequence rather than routing random ratsnest lines.

## Current Gate

```text
make layout-status
```

Current result:

- ERC: 0 violations
- DRC: 1 known warning, `MOD2` footprint/library mismatch
- Unrouted: 140 ratsnest pairs

## Pass 1: Placement Blockers

Resolve these before routing more long traces:

1. Finalize or replace the edge-launch SMA footprint and RF launch geometry.
2. Rework the TPS61088/R405/BOOST_EN local fanout area.
3. Rework BQ25798 `BQ_REGN`/`ILIM_HIZ` local fanout around the inductor and I2C exits.
4. Rework the protection-divider ground escape around `OV_NODE` and `BOOST_EN`.
5. Confirm XT30 connector polarity, board-edge access, and mating-plug clearance.

## Pass 2: Ground System

`GND` is the largest remaining unrouted group. Do not route it as skinny traces.

Planned work:

- Add functional stitching vias near grounded IC pads and connector grounds.
- Add local top/bottom ground copper where it does not break RF or switch-node discipline.
- Keep Layer 2 as the uninterrupted ground reference.
- Add E22 ground via stitching only after the RF/SMA launch decision is stable.

## Pass 3: Charger Power Path

Route as copper pours after placement review:

- `BQ_SYS`
- `BQ_PMID`
- `BQ_VBUS`
- `BAT_RAW`
- `SOLAR_FUSED`
- `SOLAR_PROTECTED`

These nets should not be completed as narrow generated traces.

## Pass 4: Switch Nodes

Route only after BQ25798 and TPS61088 placement is compact:

- `BQ_SW1`
- `BQ_SW2`
- `BOOST_SW`

The current layout only ties adjacent TPS61088 switch pins. The inductor loop remains intentionally unrouted.

## Pass 5: Remaining Sense And Control Nets

Route after nearby placement is stable:

- `BQ_TS`
- `BATP_KELVIN`
- `BQ_PROG`
- `BQ_INT`
- `BQ_SDRV`
- `LTC_SHDN`
- `UV_NODE`
- `OV_NODE`
- `NTC_SENSE`

These should avoid switch-node copper and RF launch copper.

## Hold Items

- Do not add test points, current shunts, probe loops, or bench-only measurement links.
- Do not route `RF_915` until the SMA footprint and stack-up are final.
- The 2026-07-25 Molex product-page recheck keeps `732511150` selected, but does not release the footprint. The sales drawing/recommended launch geometry is still required.
- Do not route `BOOST_EN` until the TPS61088/R405 fanout placement is fixed.
- Two R405 relocation trials near the TPS61088 EN pin were rejected: one collided with the E22 SPI pad/courtyard corridor and one collided with the E22_NSS route/via corridor. Treat `BOOST_EN` as a placement-corridor problem, not as a single missing short segment.
- Do not force ground traces where a pour/stitching plan is required.
