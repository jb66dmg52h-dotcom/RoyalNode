# RoyalNode Rev A KiCad Capture Status

## Current Milestone

Milestone `K1c` is complete.

The root schematic is generated from:

```text
hardware/kicad/RoyalNode/SCHEMATIC_CAPTURE_SEED_REV_A.csv
hardware/kicad/RoyalNode/PASSIVE_CAPTURE_SEED_REV_A.csv
tools/generate_kicad_capture.py
hardware/kicad/RoyalNode/lib_symbols/RoyalNode.kicad_sym
```

The generated schematic places these references:

```text
MOD1, MOD2, U1, U2, U3, U4, Q1, Q2, Q3, J1, J2, J3, J4, J5, F1, L1, L2
```

It also places 52 support passive references from `PASSIVE_CAPTURE_SEED_REV_A.csv` and 6 ERC-only power flags.

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
- BQ25798 bulk, bypass, bootstrap, TS, BATP, PROG, INT, and I2C support passives
- TPS61088 VIN/VOUT/VCC/BOOT/SS/COMP/feedback/frequency/current-limit/enable support passives
- E22 local 5 V ceramic and bulk capacitors
- battery NTC representation `TH1`
- LTC4365 UV/OV divider and SHDN pullup network
- BQ25798 STAT charge LED path
- ERC-only power-source flags for source/input rails

## Current ERC State

The generated scaffold is ERC clean.

Current ERC result after generation:

```text
0 messages
0 errors
0 warnings
```

## Next Capture Work

Next milestone `K1d`:

1. Replace generic two-pin passive placeholders with resistor, capacitor, LED, thermistor, fuse, and inductor-specific project symbols where useful.
2. Assign only verified or intentionally draft footprints according to the footprint release matrix.
3. Start schematic-to-board synchronization after footprint status is clear.
4. Move from label-heavy generated capture toward sheet-level grouping if the flat root sheet becomes hard to review.

Do not add test points, current shunts or bench-only measurement links.
