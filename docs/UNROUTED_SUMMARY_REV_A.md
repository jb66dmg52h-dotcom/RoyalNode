# Unrouted Summary Rev A

Generated from `hardware/fabrication/RoyalNode_drc.rpt`.

This file is a layout planning aid, not a manufacturing release note. Counts are KiCad ratsnest-pair counts, so a net with several components can appear multiple times.

Total unrouted pairs: 41

| Net | Ratsnest pairs | Layout note |
|---|---:|---|
| `5V_RADIO` | 4 | Route as high-current power pour after boost/radio placement review. |
| `BQ_SYS` | 4 | Route as system power pour after charger/boost placement review. |
| `BQ_VBUS` | 4 | Route as input-selector power copper after Q2/Q3/U1 placement review. |
| `BAT_RAW` | 3 | Route as high-current battery path after XT30 and power-path review. |
| `SOLAR_PROTECTED` | 3 | Route with protected solar path after Q1/Q2/U1 placement review. |
| `BOOST_EN` | 2 | Hold for TPS61088/R405 local fanout placement pass. |
| `BQ_REGN` | 2 | Hold for BQ25798 local fanout and inductor-area placement pass. |
| `BQ_SW1` | 2 | Switch node; keep compact and route only after BQ25798 power-loop placement. |
| `BQ_SW2` | 2 | Switch node; keep compact and route only after BQ25798 power-loop placement. |
| `USB_VBUS_RAW` | 2 |  |
| `BATP_KELVIN` | 1 |  |
| `BOOST_COMP` | 1 |  |
| `BOOST_FB` | 1 |  |
| `BOOST_VCC` | 1 |  |
| `BQ_ACDRV1` | 1 |  |
| `BQ_ACDRV2` | 1 |  |
| `BQ_BTST1` | 1 |  |
| `BQ_BTST2` | 1 |  |
| `BQ_PMID` | 1 | Route as local charger power copper after capacitor placement review. |
| `LTC_SHDN` | 1 |  |
| `OV_NODE` | 1 |  |
| `SOLAR_FUSED` | 1 | Route with solar protection power path after Q1/U4 placement review. |
| `UV_NODE` | 1 |  |
