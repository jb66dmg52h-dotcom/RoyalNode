# RoyalNode KiCad Workspace

This folder contains the Git-tracked KiCad design for RoyalNode Rev A.

Open the project file:

```text
hardware/kicad/RoyalNode/RoyalNode.kicad_pro
```

Current status:

- KiCad 10.0 project scaffold created.
- Root schematic is intentionally a capture placeholder.
- PCB file contains the Rev A board outline, placement zones, RF corridor, and keepout notes.
- Project-local symbols have been started in `RoyalNode/lib_symbols/RoyalNode.kicad_sym`.
- Footprint release is controlled by `RoyalNode/lib_footprints/FOOTPRINT_RELEASE_MATRIX_REV_A.md`.
- Footprints, schematic nets, and routed copper still need to be captured from `docs/DESIGN_FREEZE_REV_A.md` and `docs/NET_MAP_REV_A.md`.

Design source of truth:

- `docs/DESIGN_FREEZE_REV_A.md`
- `docs/NET_MAP_REV_A.md`
- `docs/PIN_AUDIT_REV_A.md`
- `docs/RF_DESIGN_REV_A.md`
