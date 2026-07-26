# Unrouted Summary Rev A

Generated from `hardware/fabrication/RoyalNode_drc.rpt`.

This file is a layout planning aid, not a manufacturing release note. Counts are KiCad ratsnest-pair counts, so a net with several components can appear multiple times.

Total unrouted pairs: 19

| Net | Ratsnest pairs | Layout note |
|---|---:|---|
| `5V_RADIO` | 4 | Route as high-current power pour after boost/radio placement review. |
| `BQ_REGN` | 2 | Hold for BQ25798 local fanout and inductor-area placement pass. |
| `BQ_VBUS` | 2 | Route as input-selector power copper after Q2/Q3/U1 placement review. |
| `USB_VBUS_RAW` | 2 |  |
| `BATP_KELVIN` | 1 |  |
| `BOOST_COMP` | 1 |  |
| `BOOST_VCC` | 1 |  |
| `BQ_BTST2` | 1 |  |
| `BQ_PMID` | 1 | Route as local charger power copper after capacitor placement review. |
| `BQ_SW1` | 1 | Switch node; keep compact and route only after BQ25798 power-loop placement. |
| `BQ_SW2` | 1 | Switch node; keep compact and route only after BQ25798 power-loop placement. |
| `BQ_SYS` | 1 | Route as system power pour after charger/boost placement review. |
| `SOLAR_PROTECTED` | 1 | Route with protected solar path after Q1/Q2/U1 placement review. |
