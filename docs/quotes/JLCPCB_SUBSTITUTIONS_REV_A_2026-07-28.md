# JLCPCB Quote Substitutions - RoyalNode Rev A

Date checked: 2026-07-28

This note records quote-time substitutions used to get the RoyalNode Rev A BOM through JLCPCB's PCBA part-selection flow. No order was placed.

## Excluded From Final PCBA Quote

| Designator | Part | Quote action | Reason |
|---|---|---|---|
| `MOD1` | Seeed Studio XIAO nRF52840 | Excluded from JLCPCB BOM/CPL | User will source and install the XIAO module separately |
| `J5` | Molex edge-launch SMA | Excluded from final quote package | Recognized earlier as `C841205`, but absent from the successful JLC placement list |
| `Q1,Q2,Q3` | Dual N-channel PG-DSO-8 MOSFETs | Do not place / external sourcing required | No safe JLC in-stock dual N-channel substitute was found; N+P related parts are not acceptable |
| `R102` | 40.2 kOhm divider resistor | Do not place / sourcing required | JLC-source candidates remained short in the quote flow |
| `R200` | 5.23 kOhm TS-network resistor | Do not place / sourcing required | JLC-source candidates remained short in the quote flow |
| `R201` | 30.1 kOhm TS-network resistor | Do not place / sourcing required | JLC-source candidates remained short in the quote flow |
| `R400` | 176 kOhm TPS61088 feedback resistor | Do not place / sourcing required | JLC-source candidates remained short in the quote flow |
| `R401` | 56.0 kOhm TPS61088 feedback resistor | Do not place / sourcing required | JLC-source candidates remained short in the quote flow |
| `U4` | LTC4365 protection controller | Do not place / sourcing required | JLC-source candidates remained short in the quote flow |

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
| `R100` | 1.78 MOhm, 1%, 0603 | `C166890` | RALEC `RTT031784FTP` | Same resistance/tolerance/package quote substitute |
| `R102` | 40.2 kOhm, 0.1%, 0603 | `C1724666` | Vishay `TNPW060340K2BEEN` | Same value/package precision divider candidate; still shortage-blocked |
| `R200` | 5.23 kOhm, 0.1%, 0603 | `C1716516` | Yageo `RT0603WRD075K23L` | Same value/package precision TS-network candidate; still shortage-blocked |
| `R201` | 30.1 kOhm, 0.1%, 0603 | `C4041890` | Yageo `RT0603WRC0730K1L` | Same value/package precision TS-network candidate; still shortage-blocked |
| `R400` | TPS61088 feedback top, 176 kOhm, 0.1%, 0603 | `C2497648` | KOA `RN73R1JTTD1763D50` | Same value/package feedback candidate; still shortage-blocked |
| `R401` | TPS61088 feedback bottom, 56.0 kOhm, 0.1%, 0603 | `C4159977` | Vishay `TNPW060356K0BETA` | Same value/package feedback candidate; still shortage-blocked |
| `U4` | ADI `LTC4365ITS8-1#TRMPBF` | `C117259` | ADI `LTC4365HTS8-1#PBF` | Same -1 TSOT-23-8 protection-controller family, higher-temperature candidate; still shortage-blocked |

## Engineering Notes

- `F1` remains a release-review item. The Bourns substitute is useful for quote processing, but its voltage, interrupt rating, operating temperature and time-current behavior still need review against the final 6 V / 20 W panel before this becomes a fabrication release.
- `Q1,Q2,Q3` remain sourcing/release-review items. A safe JLC in-stock dual N-channel PG-DSO-8 substitute was not found during this quote pass.
- A Diodes `DMTH6016LSD-13` candidate was rejected for this quote pass because its SO-8 pinout does not match the current RoyalNode Q1-Q3 net assignment.
- JLC-listed related Infineon N+P parts were not used because the RoyalNode circuit requires dual N-channel MOSFETs.
- `J6` is optional environmental telemetry hardware. The XYECONN connector is a GH-compatible quote candidate, not a release-approved JST part.
- `J5` needs a sourcing or assembly decision before release. It was recognized as exact Molex `C841205` but did not appear in the final successful placement quote.
- `R102`, `R200`, `R201`, `R400`, `R401` and `U4` were recognized by JLCPCB but remained stock-short in the quote flow and were moved to do-not-place for the successful quote.
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
