# RoyalNode Rev A Sourcing Gaps

Generated from `bom/REV_A_LOCKED_CORE_BOM.csv` and `bom/REV_A_LOCKED_PASSIVES.csv`.

This report tracks ordering friction only. It does not change the electrical design.

| Area | Ref/group | Value/part | Missing | Notes |
|---|---|---|---|---|
| core | F1 | 5 A solar input fuse | status locked_candidate | Located immediately after solar XT30 positive; verify time-current behavior against selected 6 V / 20 W panel Isc |
| passive | R_LTC_UVOV_R3 | 1.78 MOhm 1% | manufacturer, MPN, status locked_candidate_value | Select stocked 1% or better part during sourcing |
| passive | R_LTC_UVOV_R2 | 180 kOhm 0.1% | manufacturer, MPN, status locked_candidate_value | Select stocked 0.1% or better part during sourcing |
| passive | R_LTC_UVOV_R1 | 40.2 kOhm 0.1% | manufacturer, MPN, status locked_candidate_value | Select stocked 0.1% or better part during sourcing |

Resolve these gaps before requesting a real PCBA quote. Values marked as locked still need exact stocked manufacturer parts when the manufacturer and MPN are `TBD`.
