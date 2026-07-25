# RoyalNode Rev A Current Status

## Snapshot

Rev A is an active KiCad engineering scaffold, not a fabrication release.

Current architecture:

- XIAO nRF52840 socketed compute module.
- EBYTE E22-900M33S factory-installed radio module.
- Protected 1S Li-ion/LiPo battery pack.
- 6 V / 20 W class solar input.
- XT30 solar and battery connectors.
- BQ25798 1S solar/USB charger and power-path controller.
- TPS61088 5 V radio boost rail.
- Optional BME680/environmental I2C connector using JST-GH.
- PCB-mounted edge-launch SMA path from E22 ANT pin 21.

## Implemented In KiCad

- Generated root schematic with major active parts, connectors, inductors, fuse, off-board thermistor representation and 54 support passives.
- Project-local symbol library for the current Rev A major parts.
- Project-local release-candidate footprints for E22, XIAO socket, BQ25798, TPS61088, LM66100, LTC4365, Infineon power MOSFETs, XT30, JST-GH, inductors, solar fuse and E22 bulk capacitor.
- Net-aware PCB placement scaffold with 71 generated footprint anchors.
- KiCad net classes for high-current power, switching nodes, RF and sensitive sense nets.
- No dedicated test points, current shunts, probe loops or bench-only measurement links.

## Current Checks

Preferred local verification command:

```text
make full-check
```

This runs the repository validator, KiCad ERC, KiCad DRC and the report gate that confirms only the expected Rev A warning/unrouted state is present.

Expected command state:

```text
make validate
  passes

kicad-cli sch erc --exit-code-violations --severity-all
  0 violations

kicad-cli pcb drc --severity-all
  3 known footprint/library warnings: MOD2, U3 and L2
  72 expected unconnected/ratsnest items because the board is not routed
```

The known footprint warnings are tracked because MOD2 is a local JLC/LCSC release candidate for a factory-installed E22 module and U3/L2 are local release-candidate power footprints whose board instances are rotated for the accepted boost topology. These must be cleared by KiCad footprint update/save behavior or explicitly accepted through JLCPCB DFM/PCBA review before fabrication release.

J3 has been moved to the bottom service edge to clear the J6/SMA/C503 area. J6 has been moved to the top service edge and is currently an unrouted optional BME680/environmental connector until a clean serviceable fanout is added.

`BOOST_EN` remains intentionally unrouted until the TPS61088 local fanout and R405 placement are reviewed. A generated trial route was rejected because it crowded the exposed ground pad and solder-mask openings.

`BQ_REGN`/`ILIM_HIZ` and the protection-divider `GND` local link are also intentionally unrouted until their local placement/fanout is improved. Generated trial routes were rejected and retired because they crossed I2C/OV routes or crowded adjacent pads.

## Active Blockers

1. SMA launch is not released.
   The board still uses a draft SMA envelope. The Molex/JLC footprint and final 50-ohm GCPW geometry must be reviewed against the selected JLCPCB stack-up before routing release.

2. E22 first physical fit check happens after factory assembly.
   The user will not have a loose E22 module before ordering. Rev A therefore relies on JLCPCB/LCSC part `C22399506`, DFM/PCBA review and first-article inspection.

3. XT30 polarity and mating clearance still need mechanical review.
   The project uses XT30, not XT60.

4. XIAO socket orientation still needs physical USB-C, antenna and header-engagement review.

5. Power-stage placement still needs refinement before routing.
   U3/L2 are now rotated into the preferred topology, but the current support-passive locations are still staging anchors for ratsnest review, not final optimized high-di/dt loop placement.

## Authoritative Documents

Use these first:

- `docs/REQUIREMENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/DESIGN_FREEZE_REV_A.md`
- `docs/WIRING_BLUEPRINT.md`
- `docs/NET_MAP_REV_A.md`
- `docs/PIN_AUDIT_REV_A.md`
- `docs/FOOTPRINT_AUDIT_REV_A.md`
- `docs/PCB_PLACEMENT_STATUS_REV_A.md`
- `docs/UNROUTED_SUMMARY_REV_A.md`
- `docs/LAYOUT_WORK_QUEUE_REV_A.md`
- `docs/PCB_NET_CLASSES_REV_A.md`

Older conflict reviews and trace-path audits are retained as historical reasoning. Where they conflict with the files above, the current authoritative documents win.

## Next Useful Work

1. Unblock the SMA footprint and GCPW launch.
2. Refine power-stage placement from the ratsnest.
3. Confirm XIAO socket and XT30 mechanical orientation.
4. Begin actual routing only after the SMA/power placement questions are settled.
