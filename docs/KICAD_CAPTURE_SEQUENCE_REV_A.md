# RoyalNode Rev A KiCad Capture Sequence

## Purpose

This sequence defines the next schematic-capture order for Codex and human review. It is meant to keep the design moving while preventing high-risk RF and power sections from being silently approximated.

## Current Inputs

- `docs/DESIGN_FREEZE_REV_A.md`
- `docs/REFERENCE_DESIGNATORS_REV_A.md`
- `docs/PIN_AUDIT_REV_A.md`
- `docs/NET_MAP_REV_A.md`
- `hardware/kicad/RoyalNode/SCHEMATIC_CAPTURE_SEED_REV_A.csv`
- `hardware/kicad/RoyalNode/lib_symbols/RoyalNode.kicad_sym`

## Capture Order

1. Place core symbols only:
   - `MOD1` XIAO nRF52840 socket
   - `MOD2` E22-900M33S
   - `U1` BQ25798
   - `U2` LM66100
   - `U3` TPS61088
   - `U4` LTC4365
   - `Q1` to `Q3` ISA170170N04LMDS
   - `J1` to `J5`
   - `L1`, `L2`, `F1`

2. Wire low-risk digital nets:
   - SPI
   - E22 reset/interrupt/busy
   - I2C
   - boost enable

3. Wire power-control logic nets:
   - LM66100 `CE -> VOUT`
   - LM66100 `ST -> GND`
   - BQ25798 CE/PROG/REGN/ILIM_HIZ
   - BQ25798 INT pull-up with no MCU connection

4. Wire power tree:
   - solar connector and LTC4365 protection
   - BQ25798 input selector MOSFETs
   - battery BAT/BATP/SYS/PMID/SW nodes
   - TPS61088 boost stage
   - E22 5 V rail

5. Wire RF only after footprint work starts:
   - E22 pin 21 `RF_915`
   - SMA center
   - adjacent RF grounds

6. Add passives from the locked passive BOM.

7. Run ERC after every subsystem is added.

## Stop Conditions

Stop schematic capture and resolve the conflict if any of these occur:

- A symbol pin number disagrees with `docs/PIN_AUDIT_REV_A.md`.
- A footprint appears to satisfy only the package name but not the manufacturer drawing.
- The RF route requires a matching network, test pad, or series link; Rev A explicitly removed those.
- A test point, current shunt, or bench-only bypass appears in the schematic.
- A stale preliminary BOM item reappears, such as MAX17048, SWD connector, eFuse/load switch, GPS, display, fan, or generic expansion sensor connector.

## Next KiCad Milestone

Milestone `K1`: schematic contains all core symbols and global labels from `SCHEMATIC_CAPTURE_SEED_REV_A.csv`, with no footprints assigned except released standard passives/connectors.

