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
| `draft_envelope_only` | Mechanical outline exists with no electrical pads and must not be assigned to schematic symbols |
| `imported_unchecked` | Vendor/third-party CAD imported but not checked against package drawing |
| `conditional_release_candidate` | Checked against primary source plus intended assembler library; allowed for Rev A planning and DFM, pending final order review |
| `checked` | Pad numbering and package geometry checked against manufacturer drawing |
| `released_rev_a` | Approved for Rev A placement/routing |

## Matrix

| Ref | Part / footprint target | Risk | State | Release requirement |
|---|---|---|---|---|
| U1 | BQ25798RQMR, TI RQM0029A HOTROD VQFN-HR | High | `conditional_release_candidate` | Project-local copy of KiCad `Texas_RQM0029A`; verify against TI package drawing and JLC assembly before release |
| U2 | LM66100DCKR, TI DCK0006A SC-70-6 | Medium | `conditional_release_candidate` | Project-local SC-70-6 copy; verify against TI DCK0006A package drawing |
| U3 | TPS61088RHLR, TI RHL0020A VQFN-20 + EP pad 21 | High | `conditional_release_candidate` | Project-local copy of KiCad `Texas_VQFN-RHL-20_ThermalVias`; confirm exposed pad/via/paste strategy |
| U4 | LTC4365ITS8-1, ADI TS8 TSOT-23-8 | Medium | `conditional_release_candidate` | Project-local TSOT-23-8 copy; verify against ADI TS8 package drawing |
| Q1-Q3 | ISA170170N04LMDS, Infineon PG-DSO-8 | Medium | `conditional_release_candidate` | Project-local Infineon PG-DSO-8-27 thermal-via footprint; confirm duplicated drain/source pin mapping and orientation |
| MOD1 | Seeed XIAO nRF52840 socket assembly | Medium | `conditional_release_candidate` | Composite footprint uses two JLC/LCSC `C53202181` 1x7 socket strips; verify XIAO orientation, row spacing, and socket engagement before release |
| MOD2 | EBYTE E22-900M33S castellated module | High | `conditional_release_candidate` | Factory-installed PCBA item using EBYTE manual plus exact JLC/LCSC `C22399506` EasyEDA footprint cross-check; physical check deferred to assembled-board first article |
| J1/J2 | AMASS XT30PW-M right-angle male | Medium | `conditional_release_candidate` | Imported JLC/LCSC `C431092` EasyEDA geometry; confirm polarity from physical connector and add mating-plug clearance |
| J3 | JST-GH SM02B-GHS-TB 2-pin horizontal | Low | `conditional_release_candidate` | Project-local copy of KiCad JST-GH footprint; verify against JST drawing, harness retention and assembler source |
| J4 | JST-GH SM02B-GHS-TB 2-pin horizontal | Low | `conditional_release_candidate` | Same JST-GH footprint as J3; confirm NTC harness pin 1 marker and battery-pack cable mate |
| J5 | Molex 0732511150 SMA edge launch | High | `draft_envelope_only` | JLC/LCSC `C841205` import exists but is not placed; use Molex launch for 1.60 mm PCB and merge with final GCPW stack-up |
| F1 | Littelfuse 0483002.DR, 483 series 1206 chip fuse | Low | `conditional_release_candidate` | Project-local copy of KiCad 1206 fuse footprint; verify against Littelfuse 483 package drawing |
| L_BQ | Coilcraft XAL7070-222MEC | Medium | `conditional_release_candidate` | Project-local KiCad Coilcraft XAL7070 footprint; confirm against Coilcraft recommended land pattern |
| L_BOOST | Coilcraft XAL7030-222MEC | Medium | `conditional_release_candidate` | Project-local KiCad Coilcraft XAL7030-222 footprint; confirm against Coilcraft recommended land pattern |
| C_BULK | Panasonic 10SVPC330M | Medium | `not_started` | Use polarized SMD polymer footprint with clear polarity marking |
| Passives | 0402/0603/1206/1210 R/C | Low | `not_started` | Standard KiCad/JLC-compatible metric footprints acceptable after value/package review |

## First Footprint Work Order

1. E22-900M33S module footprint and RF-side geometry.
2. Molex 0732511150 SMA edge-launch footprint.
3. TPS61088 footprint and boost-inductor footprint.
4. BQ25798 HOTROD footprint and charger-inductor footprint.
5. Promote or reject the imported SMA footprint after RF/mechanical review.
6. Verify XIAO and XT30 first-article mechanical fit.

This order lets the board outline and high-risk RF/power placement stabilize before low-risk passives are assigned.
