# RoyalNode Rev A Manufacturing Export Workflow

## Status

Rev A can now generate a draft quote package, but it is not a fabrication release.

Use:

```text
make export-draft-quote
```

Output path:

```text
hardware/fabrication/quote_draft_rev_a/
```

The generated files are ignored by Git. They are build artifacts, not source files.

## Exported Artifacts

The export script creates:

- Gerber files
- Excellon drill files
- drill map and drill report
- KiCad BOM CSV
- richer JLCPCB-oriented draft BOM with manufacturer and known LCSC fields
- KiCad position/CPL CSV
- schematic netlist
- zipped Gerber, drill and assembly bundles
- `READ_ME_NOT_FOR_FABRICATION.txt`

## Current Release Gate

The draft quote package is useful for checking the manufacturer workflow and rough order screens. It must not be used to order boards yet.

Known blockers:

- `RF_915` is intentionally unrouted.
- J5 is still a draft SMA envelope, not a released Molex edge-launch footprint.
- Final 50 ohm GCPW width/gap still needs the JLCPCB stack-up calculation.
- High-current power rails and switching loops are not complete.
- Current DRC has 45 expected unconnected items.
- Current known footprint/library warnings are MOD2, U3 and L2.

## Intended Use

Run the export after:

```text
make layout-status
```

The export package becomes orderable only after the release blockers are closed and the blocker note is deliberately replaced with a proper release manifest.
