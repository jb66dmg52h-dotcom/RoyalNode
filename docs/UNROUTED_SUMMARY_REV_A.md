# Unrouted Summary Rev A

Generated from `hardware/fabrication/RoyalNode_drc.rpt`.

This file is a layout planning aid, not a manufacturing release note. Counts are KiCad ratsnest-pair counts, so a net with several components can appear multiple times.

Total unrouted pairs: 145

| Net | Ratsnest pairs | Layout note |
|---|---:|---|
| `GND` | 52 | Route through ground pours/stitching after component placement is stable. |
| `5V_RADIO` | 11 | Route as high-current power pour after boost/radio placement review. |
| `BQ_SYS` | 11 | Route as system power pour after charger/boost placement review. |
| `BQ_VBUS` | 7 | Route as input-selector power copper after Q2/Q3/U1 placement review. |
| `BOOST_SW` | 6 | Switch node; keep compact and route only after TPS61088 power-loop placement. |
| `BAT_RAW` | 5 | Route as high-current battery path after XT30 and power-path review. |
| `BQ_PMID` | 4 | Route as local charger power copper after capacitor placement review. |
| `SOLAR_FUSED` | 4 | Route with solar protection power path after Q1/U4 placement review. |
| `SOLAR_PROTECTED` | 4 | Route with protected solar path after Q1/Q2/U1 placement review. |
| `BQ_REGN` | 3 | Hold for BQ25798 local fanout and inductor-area placement pass. |
| `3V3` | 2 |  |
| `BOOST_EN` | 2 | Hold for TPS61088/R405 local fanout placement pass. |
| `BOOST_FB` | 2 |  |
| `BQ_SW1` | 2 | Switch node; keep compact and route only after BQ25798 power-loop placement. |
| `BQ_SW2` | 2 | Switch node; keep compact and route only after BQ25798 power-loop placement. |
| `USB_VBUS_RAW` | 2 |  |
| `BATP_KELVIN` | 1 |  |
| `BOOST_BOOT` | 1 |  |
| `BOOST_COMP` | 1 |  |
| `BOOST_COMP_RC` | 1 |  |
| `BOOST_FSW` | 1 |  |
| `BOOST_ILIM` | 1 |  |
| `BOOST_SS` | 1 |  |
| `BOOST_VCC` | 1 |  |
| `BQ_ACDRV1` | 1 |  |
| `BQ_ACDRV2` | 1 |  |
| `BQ_BTST1` | 1 |  |
| `BQ_BTST2` | 1 |  |
| `BQ_INT` | 1 |  |
| `BQ_PROG` | 1 |  |
| `BQ_SDRV` | 1 |  |
| `BQ_SOLAR_SELECTOR_COMMON` | 1 |  |
| `BQ_TS` | 1 |  |
| `BQ_USB_SELECTOR_COMMON` | 1 |  |
| `LTC_SHDN` | 1 |  |
| `NTC_SENSE` | 1 |  |
| `OV_NODE` | 1 |  |
| `SOLAR_PROT_COMMON` | 1 |  |
| `SOLAR_PROT_GATE` | 1 |  |
| `SOLAR_RAW` | 1 | Route with input protection path after XT30/fuse placement review. |
| `UV_NODE` | 1 |  |
| `XIAO_BAT_ISO` | 1 |  |
