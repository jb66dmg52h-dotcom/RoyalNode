# 2Watt Project Power Input Decisions

## Issue 1: BQ25798 dual-input source mux

**Status: LOCKED**

Use the full BQ25798 dual-source mux topology:

```text
Solar source -> back-to-back ACFET/RBFET pair -> common VBUS
USB source   -> back-to-back ACFET/RBFET pair -> common VBUS
```

Requirements:

- Solar source is assigned to VAC1 control/sense.
- USB source is assigned to VAC2 control/sense.
- Each source receives its own back-to-back N-channel MOSFET pair.
- The BQ25798 controls the source-selection FETs through its source-driver outputs.
- No source may backfeed the other source or its connector.
- Exact MOSFET manufacturer part numbers remain to be selected during the input-stage schematic design.

This supersedes all earlier one-pair or direct-source concepts.

## Issue 2: Solar overvoltage and surge protection

**Status: OPEN**

The previously selected SMBJ22A is rejected because its clamping voltage can exceed the BQ25798 30 V absolute maximum. The next decision is whether to use an active overvoltage cutoff controller or impose a lower panel Voc envelope with a different clamp strategy.
