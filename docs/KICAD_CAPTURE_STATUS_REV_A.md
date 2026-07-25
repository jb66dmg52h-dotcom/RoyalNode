# RoyalNode Rev A KiCad Capture Status

## Current Milestone

Milestone `K1a` is complete.

The root schematic is generated from:

```text
hardware/kicad/RoyalNode/SCHEMATIC_CAPTURE_SEED_REV_A.csv
tools/generate_kicad_capture.py
hardware/kicad/RoyalNode/lib_symbols/RoyalNode.kicad_sym
```

The generated schematic places these references:

```text
MOD1, MOD2, U1, U2, U3, U4, Q1, Q2, Q3, J1, J2, J3, J4, J5, F1, L1, L2
```

The capture uses deterministic UUIDs and embedded RoyalNode symbol definitions so KiCad can parse and ERC-check it without relying on an external symbol cache.

## What Is Captured

- XIAO nRF52840 socket interface
- EBYTE E22-900M33S module interface
- BQ25798 charger/controller pins
- LM66100 XIAO battery-feed ideal diode
- TPS61088 boost converter pins
- LTC4365 solar protection controller
- three ISA170170N04LMDS MOSFET blocks
- solar and battery XT30 connectors
- XIAO battery harness connector
- battery NTC connector
- SMA RF connector symbol
- solar fuse `F1`
- charger inductor `L1`
- boost inductor `L2`

## Current ERC State

The generated scaffold is not ERC clean yet.

Current ERC result after generation:

```text
36 messages
16 errors
20 warnings
```

Expected remaining categories:

- `power_pin_not_driven`: power-driver symbols and final power-source handling are not yet added
- `pin_not_driven`: configuration/support networks are not yet expanded from the passive BOM
- `isolated_pin_label`: single-ended support nets are waiting for capacitors, resistors, LEDs or later RF handling
- `pin_to_pin`: repeated TPS61088 VOUT power-output pins share the same net and may require ERC pin-type cleanup

## Next Capture Work

Next milestone `K1b`:

1. Expand the grouped passive BOM into individual reference designators.
2. Add resistor/capacitor/LED schematic symbols for BQ25798 support networks.
3. Add TPS61088 support passives.
4. Add E22 local decoupling.
5. Add explicit power symbols or ERC treatment after reviewing which errors are real design issues versus multi-pin IC modeling noise.

Do not add test points, current shunts or bench-only measurement links.

