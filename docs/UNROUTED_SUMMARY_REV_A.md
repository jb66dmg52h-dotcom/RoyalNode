# Unrouted Summary Rev A

Generated from `hardware/fabrication/RoyalNode_drc.rpt`.

This file is a layout planning aid, not a manufacturing release note. Counts are KiCad ratsnest-pair counts, so a net with several components can appear multiple times.

Total unrouted pairs: 11

| Net | Ratsnest pairs | Layout note |
|---|---:|---|
| `5V_RADIO` | 4 | Route as high-current power pour after boost/radio placement review. |
| `BQ_VBUS` | 2 | Route as input-selector power copper after Q2/Q3/U1 placement review. |
| `BOOST_VCC` | 1 |  |
| `BQ_SW2` | 1 | Switch node; keep compact and route only after BQ25798 power-loop placement. |
| `E22_RXEN` | 1 |  |
| `SOLAR_PROTECTED` | 1 | Route with protected solar path after Q1/Q2/U1 placement review. |
| `USB_VBUS_RAW` | 1 |  |
