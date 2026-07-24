# RoyalNode Rev A KiCad Symbol Audit

## Status

Initial project-local symbols have been created in:

```text
hardware/kicad/RoyalNode/lib_symbols/RoyalNode.kicad_sym
```

These symbols are intended to make schematic capture possible from the frozen Rev A architecture. They are not a footprint release by themselves.

## Source Documents

The symbol pins were generated from the current Rev A source-of-truth documents:

- `docs/DESIGN_FREEZE_REV_A.md`
- `docs/PIN_AUDIT_REV_A.md`
- `docs/LOCKED_COMPONENTS_REV_A.md`
- `docs/NET_MAP_REV_A.md`

The older `docs/PRELIMINARY_BOM_KICAD_AND_SOURCING.md` is not authoritative for symbol creation where it conflicts with the design freeze. In particular, it still references removed/open items such as a MAX17048 fuel gauge, eFuse/load switch, SWD connector, and power-button circuitry.

## Symbols Created

| Symbol | Intended reference | Source basis |
|---|---|---|
| `RoyalNode:RN_XIAO_nRF52840_SOCKET` | U | Final XIAO GPIO map from design freeze and pin audit |
| `RoyalNode:RN_E22_900M33S` | U | EBYTE 22-pin castellated module pin table |
| `RoyalNode:RN_BQ25798RQMR` | U | TI BQ25798 RQM 29-pin pin audit |
| `RoyalNode:RN_TPS61088RHLR` | U | TI TPS61088 RHL 20-pin plus exposed pad 21 pin audit |
| `RoyalNode:RN_LM66100DCKR` | U | TI LM66100 DCK 6-pin correction from pin audit |
| `RoyalNode:RN_LTC4365ITS8_1` | U | ADI LTC4365 TS8 pin audit |
| `RoyalNode:RN_ISA170170N04LMDS` | Q | Infineon dual N-MOSFET pin audit |
| `RoyalNode:RN_XT30PW_M` | J | AMASS XT30PW-M power connector class |
| `RoyalNode:RN_SMA_EDGE` | J | Molex 0732511150 edge-launch SMA class |
| `RoyalNode:RN_JST_PH_2` | J | Two-pin low-current connector class for XIAO power harness or NTC |

## Important Pin Decisions Captured

- TPS61088 exposed power-ground pad is symbol pin `21`, matching the TI device pin table.
- LM66100 exposes `CE` and `ST` separately so the schematic can enforce `CE -> VOUT` and `ST -> GND`.
- E22 pins `7` and `8` are exposed separately so the schematic can show the direct `TXEN <-> DIO2` connection.
- E22 pin `21` is a passive `ANT_50R` pin, separate from adjacent RF grounds on pins `20` and `22`.
- BQ25798 `D+`, `D-`, and `QON` are explicit no-connect pins.
- BQ25798 `INT` exists but is not assigned to a XIAO GPIO; charger state is polled over I2C.

## Remaining Symbol Review

Before schematic release:

- [ ] Open each project-local symbol in KiCad Symbol Editor and visually check pin order/orientation.
- [ ] Compare BQ25798, TPS61088, LM66100, LTC4365, ISA170170, E22, and XIAO pin numbers against `docs/PIN_AUDIT_REV_A.md`.
- [ ] Add datasheet/manufacturer URLs as symbol properties when the final ECAD source files are imported or manually transcribed.
- [ ] Assign footprints only after each footprint passes `docs/FOOTPRINT_AUDIT_REV_A.md`.

## Footprint Boundary

These symbols do not authorize PCB release. The following footprints still require manufacturer land-pattern transcription or CAD import before placement/routing:

- BQ25798 RQM0029A HOTROD VQFN-HR
- TPS61088 RHL0020A VQFN with exposed PGND pad 21
- EBYTE E22-900M33S castellated module
- AMASS XT30PW-M board connector
- Molex 0732511150 SMA edge launch
- Coilcraft XAL7030/XAL7070 inductors
- Panasonic 10SVPC330M polymer capacitor

