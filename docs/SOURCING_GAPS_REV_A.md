# RoyalNode Rev A Sourcing Gaps

Generated from `bom/REV_A_LOCKED_CORE_BOM.csv` and `bom/REV_A_LOCKED_PASSIVES.csv`.

This report tracks ordering friction only. It does not change the electrical design.

| Area | Ref/group | Value/part | Missing | Notes |
|---|---|---|---|---|
| core | F1 | 5 A solar input fuse | status locked_candidate | Located immediately after solar XT30 positive; verify time-current behavior against selected 6 V / 20 W panel Isc |
| core | D1 | Low-current red charge LED | manufacturer, MPN, status selected_class | Driven by BQ25798 STAT sink path |
| passive | R_LTC_UVOV_R3 | 1.78 MOhm 1% | manufacturer, MPN, status locked_candidate_value | Select stocked 1% or better part during sourcing |
| passive | R_LTC_UVOV_R2 | 180 kOhm 0.1% | manufacturer, MPN, status locked_candidate_value | Select stocked 0.1% or better part during sourcing |
| passive | R_LTC_UVOV_R1 | 40.2 kOhm 0.1% | manufacturer, MPN, status locked_candidate_value | Select stocked 0.1% or better part during sourcing |
| passive | C_E22_HF | 100 nF 16 V X7R | quantity | JLCPCB C710619 |
| passive | R_TS_UPPER | 5.23 kOhm 1% | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked 1% part during sourcing |
| passive | R_TS_LOWER | 30.1 kOhm 1% | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked 1% part during sourcing |
| passive | R_BATP | 100 Ohm | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked part during sourcing |
| passive | R_PROG | 4.70 kOhm 1% | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked 1% part during sourcing |
| passive | R_INT_PULLUP | 10 kOhm | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; not routed to MCU |
| passive | R_I2C_PULLUP | 10 kOhm | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked part during sourcing |
| passive | R_TPS_FB_TOP | 176 kOhm 0.1% | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked 0.1% part during sourcing |
| passive | R_TPS_FB_BOTTOM | 56.0 kOhm 0.1% | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked 0.1% part during sourcing |
| passive | R_TPS_FSW | 330 kOhm | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked part during sourcing |
| passive | R_TPS_ILIM | 100 kOhm | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked part during sourcing |
| passive | R_TPS_COMP | 20.0 kOhm | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked part during sourcing |
| passive | C_TPS_COMP | 4.7 nF | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked C0G/X7R part during sourcing |
| passive | C_TPS_SS | 47 nF | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked X7R part during sourcing |
| passive | C_TPS_VCC | 2.2 uF | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked X7R part during sourcing |
| passive | C_TPS_BOOT | 100 nF | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked X7R part during sourcing |
| passive | R_TPS_EN_PD | 100 kOhm | manufacturer, MPN, status locked_value | Footprint fixed by schematic capture; select stocked part during sourcing |

Resolve these gaps before requesting a real PCBA quote. Values marked as locked still need exact stocked manufacturer parts when the manufacturer and MPN are `TBD`.
