# U1 Right-Side Refactor Rev A

This note captures the next charger-layout work package after the clean
17-unrouted checkpoint.

## Current Gate

```text
make layout-status
  ERC: 0
  DRC: 3 known footprint warnings only
  Unrouted: 17 ratsnest pairs
```

Known allowed DRC warnings remain `MOD2`, `U3` and `L2` footprint/library
warnings.

## Accepted State To Preserve

- `BQ_SW1` is routed from U1/C216 to L1 with a left-side wrap.
- `BQ_SYS` has an accepted entry via at 65.80, 71.80 mm.
- C216/`BQ_BTST1` is locally tied to U1 and the SW1 escape.
- C218/`BQ_SDRV` is now staged at 69.20, 71.20 mm, with a local top-layer
  SDRV trace from U1 pad 24. This keeps SDRV close to U1 while clearing more
  of the SW2/SYS escape lane than the earlier 67.20, 70.80 mm placement.
- R203/R204 provide local `BQ_PROG` and `BQ_INT` support at 70.5 mm x.
- R204's `3V3` feed now drops through a local via at 69.68, 72.80 mm and
  ties into the existing `In2.Cu` 3.3 V spine, leaving the top-side U1
  right corridor clearer for `BQ_SW2`, `BQ_BTST2` and C218/`BQ_SDRV` work.

## Blocked Nets In This Cluster

- `BQ_SW2`
- `BQ_BTST2`
- `BATP_KELVIN`
- `BQ_REGN`
- nearby `BQ_PMID`, `BQ_VBUS`, `USB_VBUS_RAW` and `SOLAR_PROTECTED` entries

## Exact Conflict Map

The relevant U1 pad centers are:

| Pad | Net | Center |
|---:|---|---|
| 16 | `BQ_TS` | 66.850, 76.600 |
| 17 | `BQ_REGN` | 66.850, 76.200 |
| 18 | `BATP_KELVIN` | 66.875, 75.800 |
| 19 | `BQ_BTST2` | 66.862, 75.400 |
| 20 | `BQ_PROG` | 66.900, 75.000 |
| 21 | `BQ_INT` | 66.900, 74.600 |
| 22 | `BAT_RAW` | 66.900, 74.200 |
| 23 | `BAT_RAW` | 66.900, 73.800 |
| 24 | `BQ_SDRV` | 66.862, 73.400 |
| 25 | `BQ_SYS` | 65.900, 73.300 |
| 26 | `BQ_SW2` | 65.450, 73.300 |

Nearby routed or placed blockers:

| Item | Net | Current role |
|---|---|---|
| C218 | `BQ_SDRV` | Shifted right after R204 3.3 V reroute; preserve its local SDRV trace |
| R203 | `BQ_PROG` | Blocks direct BTST2 top route |
| R204 | `BQ_INT` / `3V3` | Local 3.3 V via clears the previous upper right-side top trace |
| `BQ_TS` via | `BQ_TS` | Blocks lower BTST2 dogleg |
| Q3 left pads | selector nets | Block right-side SW2 drop toward L1 |

## Rejected Trials To Avoid

- Do not move only L1 upward; it collides with the accepted TPS61088 input-cap
  cluster and U1 support passives.
- Do not route SW2 straight down or through the U1 pad row.
- Do not shift the accepted SYS entry via rightward unless C218/SDRV is moved
  first.
- Do not route BTST2 directly through the R203/PROG corridor.
- A post-C218-move BTST2 dogleg trial still failed: the left pocket crowded
  `BQ_TS`/I2C_SDA, and the right pocket shorted into the accepted
  `BQ_PROG` local route. Move or reroute R203/`BQ_PROG` before retrying
  `BQ_BTST2`.
- A vertical R203 relocation at 72.8, 76.8 mm was rejected. The rotated pad
  order put the GND pad in the PROG feed path, added a solder-mask bridge and
  introduced an extra R203 footprint/library warning.
- Do not place a BTST2 via beside U1 pads 18-20; hole clearance and existing
  B.Cu/In1 corridors fail.
- Do not move C218 upward into the TPS61088/BQ_SYS input-cap area. A trial at
  69.2, 68.0 mm shorted `BQ_SDRV` into C401/`BQ_SYS`, overlapped C401's
  courtyard and starved C218's ground thermal.
- The C218 move to 69.2, 71.2 mm is now accepted after rerouting R204's
  3.3 V feed. Do not restore the earlier 67.2, 70.8 mm placement unless a
  later SW2/BTST2 pass proves it necessary.
- Do not route R204's 3.3 V feed on `In1.Cu` across x73.5 mm; that lane
  crosses the accepted `BQ_ACDRV1` route.

## Refactor Goal

Create a legal right-side escape corridor where:

1. `BQ_SYS` keeps a short, quiet U1 entry.
2. `BQ_SW2` leaves U1 without crossing SDRV, SYS, 3.3 V, Q3 or I2C.
3. `BQ_BTST2` stays close to C217 and avoids PROG/TS.
4. `BATP_KELVIN` remains a sense connection, not part of high-current BAT copper.
5. Q3 selector pads remain serviceable and do not mask-bridge to switch-node copper.

## Candidate Placement Strategy

Try as a grouped pass only:

- Keep R203/`BQ_PROG` clear of the BTST2 path or move it below/right as part of
  the same pass.
- Re-evaluate whether C217 should stay at 72.8, 82.0 mm or rotate/shift after
  SW2 has a legal exit.
- Do not move Q3 casually; if Q3 moves, update the input-selector route group
  and check XT30 connector clearance.

## Acceptance Test

Before accepting the pass:

```text
make generate-board
make layout-status
```

The pass is accepted only if:

- unconnected count decreases below 17, or a documented placement improvement is
  achieved without increasing it;
- ERC remains 0;
- DRC contains only the known `MOD2`, `U3` and `L2` footprint warnings;
- no test points, shunts or measurement links are added.
