# RoyalNode Rev A Footprint Release Matrix

## Purpose

This matrix controls which footprints are allowed into the Rev A PCB layout. A symbol may exist before its footprint is released; a footprint is not released until the package drawing, pad numbering, polarity/orientation, courtyard, and assembly notes have been checked.

Source document:

```text
docs/FOOTPRINT_AUDIT_REV_A.md
docs/REFERENCE_DESIGNATORS_REV_A.md
docs/FOOTPRINT_SOURCE_LINKS_REV_A.md
```

## Release States

| State | Meaning |
|---|---|
| `not_started` | No project-local footprint exists yet |
| `draft` | Footprint exists but must not be used for release routing |
| `imported_unchecked` | Vendor/third-party CAD imported but not checked against package drawing |
| `checked` | Pad numbering and package geometry checked against manufacturer drawing |
| `released_rev_a` | Approved for Rev A placement/routing |

## Matrix

| Ref | Part / footprint target | Risk | State | Release requirement |
|---|---|---|---|---|
| U1 | BQ25798RQMR, TI RQM0029A HOTROD VQFN-HR | High | `not_started` | Use TI CAD or manually transcribe RQM0029A land pattern; generic QFN is not allowed |
| U2 | LM66100DCKR, TI DCK0006A SC-70-6 | Medium | `not_started` | Standard SC-70-6 acceptable only after DCK0006A pad check |
| U3 | TPS61088RHLR, TI RHL0020A VQFN-20 + EP pad 21 | High | `not_started` | Exposed pad must be pad 21; thermal via concept required |
| U4 | LTC4365ITS8-1, ADI TS8 TSOT-23-8 | Medium | `not_started` | Use ADI TS8 recommended pad layout |
| Q1-Q3 | ISA170170N04LMDS, Infineon PG-DSO-8 | Medium | `not_started` | Confirm duplicated drain/source pin mapping and consistent orientation |
| MOD1 | Seeed XIAO nRF52840 socket assembly | Medium | `not_started` | Verify XIAO row spacing and socket engagement before release |
| MOD2 | EBYTE E22-900M33S castellated module | High | `not_started` | Transcribe EBYTE mechanical drawing; verify pin 21 ANT launch geometry |
| J1/J2 | AMASS XT30PW-M right-angle male | Medium | `not_started` | Confirm polarity from physical connector and add mating-plug clearance |
| J3 | JST B2B-PH-SM4-TB(LF)(SN) | Low | `not_started` | Use JST official/verified KiCad PH-SM4-TB 2-pin footprint |
| J4 | CJT A2012WV-S-2P | Low | `not_started` | Use manufacturer/JLC footprint and pin-1 marker |
| J5 | Molex 0732511150 SMA edge launch | High | `not_started` | Use Molex launch for 1.60 mm PCB and merge with final GCPW stack-up |
| L_BQ | Coilcraft XAL7070-222MEC | Medium | `not_started` | Use Coilcraft recommended land pattern and body courtyard |
| L_BOOST | Coilcraft XAL7030-222MEC | Medium | `not_started` | Use Coilcraft recommended land pattern and body courtyard |
| C_BULK | Panasonic 10SVPC330M | Medium | `not_started` | Use polarized SMD polymer footprint with clear polarity marking |
| Passives | 0402/0603/1206/1210 R/C | Low | `not_started` | Standard KiCad/JLC-compatible metric footprints acceptable after value/package review |

## First Footprint Work Order

1. E22-900M33S module footprint and RF-side geometry.
2. Molex 0732511150 SMA edge-launch footprint.
3. TPS61088 footprint and boost-inductor footprint.
4. BQ25798 HOTROD footprint and charger-inductor footprint.
5. XT30 connector footprints.
6. XIAO socket footprint/placement.

This order lets the board outline and high-risk RF/power placement stabilize before low-risk passives are assigned.
