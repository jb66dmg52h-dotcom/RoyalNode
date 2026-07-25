# RoyalNode Rev A KiCad Capture Status

## Current Milestone

Milestone `K1d` is in progress.

The root schematic is generated from:

```text
hardware/kicad/RoyalNode/SCHEMATIC_CAPTURE_SEED_REV_A.csv
hardware/kicad/RoyalNode/PASSIVE_CAPTURE_SEED_REV_A.csv
tools/generate_kicad_capture.py
hardware/kicad/RoyalNode/lib_symbols/RoyalNode.kicad_sym
```

The generated schematic places these references:

```text
MOD1, MOD2, U1, U2, U3, U4, Q1, Q2, Q3, J1, J2, J3, J4, J5, J6, F1, L1, L2
```

It also places 54 support passive references from `PASSIVE_CAPTURE_SEED_REV_A.csv` and 6 ERC-only power flags.

The capture uses deterministic UUIDs and embedded RoyalNode symbol definitions so KiCad can parse and ERC-check it without relying on an external symbol cache.

## Footprint Assignment Status

The generated schematic now assigns project-local release-candidate footprints to the major Rev A parts that already have local footprints:

- `MOD1` XIAO socket composite footprint
- `MOD2` E22-900M33S factory PCBA footprint
- `U1` BQ25798
- `U2` LM66100
- `U3` TPS61088
- `U4` LTC4365
- `Q1`-`Q3` Infineon power FET footprint
- `J1`/`J2` XT30 power connector footprints
- `L1`/`L2` Coilcraft power-inductor footprints

The SMA footprint remains intentionally unassigned in the schematic because the board still uses a draft placement envelope while the RF launch is reviewed. Low-risk passives remain generic two-terminal schematic placeholders until passive package assignments are generated.

The passive capture seed now assigns standard KiCad footprints to low-risk support passives:

- resistors: `Resistor_SMD:R_0603_1608Metric`
- small capacitors: `Capacitor_SMD:C_0603_1608Metric`
- medium ceramic capacitors: `Capacitor_SMD:C_0805_2012Metric` and `Capacitor_SMD:C_1206_3216Metric`
- high-current/energy ceramic capacitors: `Capacitor_SMD:C_1210_3225Metric`
- charge LED: `LED_SMD:LED_0603_1608Metric`

Unassigned footprints remain deliberate for `J5` because the SMA launch still requires final mechanical/RF review. `TH1` is intentionally off-board as the battery-mounted 103AT-2 thermistor. `J3` and `J4` use the same JST-GH 2-pin release-candidate footprint, `J6` uses the JST-GH 4-pin release-candidate footprint for optional BME680/environmental I2C telemetry, `F1` uses a Littelfuse 483-series 1206 release-candidate footprint, and `C503` uses a Panasonic 10SVPC330M 8 x 6.9 mm polymer-can release-candidate footprint.

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

Next milestone `K1e`:

1. Replace generic two-pin passive placeholders with resistor, capacitor, LED, thermistor, fuse, and inductor-specific project symbols where useful.
2. Resolve the remaining unassigned PCB footprint: SMA launch.
3. Start schematic-to-board synchronization after footprint status is clear.
4. Move from label-heavy generated capture toward sheet-level grouping if the flat root sheet becomes hard to review.

Do not add test points, current shunts or bench-only measurement links.
