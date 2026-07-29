# JLCPCB Quote Substitutions - RoyalNode Rev A

Date checked: 2026-07-28

This note records quote-time substitutions used to get the RoyalNode Rev A BOM through JLCPCB's PCBA part-selection flow. No order was placed.

## User-Supplied Part

| Designator | Part | Quote action | Reason |
|---|---|---|---|
| `MOD1` | Seeed Studio XIAO nRF52840 | Excluded from JLCPCB BOM/CPL | User will source and install the XIAO module separately |

## Forced JLCPCB Substitutions

| Designator(s) | Original intent | JLCPCB/LCSC part | Selected substitute | Reason |
|---|---|---|---|---|
| `C212,C213,C214` | 100 nF, 50 V, X7R, 0603 | `C14663` | Yageo `CC0603KRX7R9BB104` | Same value, voltage, dielectric and 0603 package; JLC-listed with high stock |
| `C404` | 100 nF, 50 V, X7R, 0603 | `C14663` | Yageo `CC0603KRX7R9BB104` | Same substitute as BQ25798 HF bypass group |
| `C215` | 4.7 uF, 25 V, X7R, 0805 | `C98195` | Samsung `CL21B475KAFNNNE` | Matches the actual KiCad 0805 footprint and REGN bypass electrical target |
| `C216,C217` | 47 nF, 50 V, X7R, 0603 | `C1622` | Samsung `CL10B473KB8NNNC` | Same value, voltage, dielectric class and mounted 0603 package |
| `C218` | 1 nF, 50 V, C0G, 0603 | `C163508` | Samsung `CL10C102JB8NNNC` | Same value, voltage, C0G dielectric and mounted 0603 package |
| `C405` | 2.2 uF, 25 V, X7R, 0805 | `C74690` | FH `0805B225K250NT` | Same value, voltage, dielectric class and mounted 0805 package |
| `F1` | 5 A solar input fuse, 1206 footprint | `C913282` | Bourns `SF-1206S500-2` | Drop-in 1206 quote substitute that lets JLC keep the fuse in PCBA |
| `J5` | Molex 0732511150 / 73251-1150 edge-launch SMA | `C841205` | Molex `73251-1150` | Exact Molex SMA connector LCSC/JLC part number for the selected footprint |
| `J6` | 4-pin right-angle JST-GH environmental connector | `C51940118` | XYECONN `XY-SM04B-GHS-TB` | GH-compatible quote substitute for optional BME680/I2C connector; footprint review required |
| `Q1,Q2,Q3` | Infineon `ISA170170N04LMDSXTMA1`, dual N-channel PG-DSO-8 | `C43317100` | Infineon `ISA250250N04LMDSXTMA1` | Same-family dual N-channel PG-DSO-8 candidate; lower-current substitute requiring power-path review |
| `R100` | 1.78 MOhm, 1%, 0603 | `C166890` | RALEC `RTT031784FTP` | Same resistance/tolerance/package quote substitute |
| `R102` | 40.2 kOhm, 0.1%, 0603 | `C4210499` | Vishay `TNPW060340K2BYEN` | Same resistance/tolerance/package precision divider substitute |
| `R200` | 5.23 kOhm, 0.1%, 0603 | `C4076829` | Vishay `TNPU06035K23BZEN00` | Same resistance/tolerance/package precision TS-network substitute |
| `R201` | 30.1 kOhm, 0.1%, 0603 | `C1709086` | Susumu `RG1608N-3012-B-T5` | Same resistance/tolerance/package precision TS-network substitute |
| `R400` | TPS61088 feedback top, 176 kOhm, 0.1%, 0603 | `C4074070` | KOA `RN731JTTD1803B50`, 180 kOhm | Paired quote substitution with R401 because exact 176 kOhm was short |
| `R401` | TPS61088 feedback bottom, 56.0 kOhm, 0.1%, 0603 | `C4106968` | SEI `RNCF0603BTE57K6`, 57.6 kOhm | Paired with 180 kOhm R400 for about 4.97 V nominal output |
| `U4` | ADI `LTC4365ITS8-1#TRMPBF` | `C688323` | ADI `LTC4365HTS8-1#TRMPBF` | Same TSOT-23-8 -1 overvoltage/undervoltage protection family, higher-temperature variant |

## Engineering Notes

- `F1` remains a release-review item. The Bourns substitute is useful for quote processing, but its voltage, interrupt rating, operating temperature and time-current behavior still need review against the final 6 V / 20 W panel before this becomes a fabrication release.
- `Q1,Q2,Q3` remain release-review items. `ISA250250N04LMDSXTMA1` appears to preserve the Infineon dual-N PG-DSO-8 family, but it has lower current rating than the original `ISA170170N04LMDSXTMA1`. The solar and USB selector dissipation must be reviewed before release.
- A Diodes `DMTH6016LSD-13` candidate was rejected for this quote pass because its SO-8 pinout does not match the current RoyalNode Q1-Q3 net assignment.
- `J6` is optional environmental telemetry hardware. The XYECONN connector is a GH-compatible quote candidate, not a release-approved JST part.
- The `R400`/`R401` pair is intentionally changed together. With the TPS61088 feedback reference of approximately 1.204 V, 180 kOhm / 57.6 kOhm gives roughly 4.97 V nominal output.
- `U4` remains a release-review item because the high-temperature `HTS8` variant should be checked against availability, cost and the intended operating temperature range.
- The capacitor substitutions are lower risk because they preserve capacitance, voltage rating, dielectric class and mounted package.
- `C215` is intentionally treated as an 0805 part because the KiCad footprint is `Capacitor_SMD:C_0805_2012Metric`, even though older sourcing notes described the original TDK candidate as a 1206 package.

## Generated Files

The reproducible quote files are produced by:

```sh
python3 tools/write_jlcpcb_processable_quote_files.py
```

The current processable quote files are:

- `hardware/fabrication/quote_draft_rev_a/assembly/RoyalNode_RevA_JLCPCB_BOM_PROCESSABLE_QUOTE.csv`
- `hardware/fabrication/quote_draft_rev_a/assembly/RoyalNode_RevA_JLCPCB_CPL_PROCESSABLE_QUOTE.csv`
