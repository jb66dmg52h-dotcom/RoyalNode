# RoyalNode Rev A Footprint Source Links

## Purpose

This file records the manufacturer/primary sources needed before a footprint can move from `not_started` or `draft` to `checked` in:

```text
hardware/kicad/RoyalNode/lib_footprints/FOOTPRINT_RELEASE_MATRIX_REV_A.md
```

Do not create released footprints from product photographs, distributor screenshots, old mirrored PDFs, or memory.

## RF Path Sources

### MOD2 — EBYTE E22-900M33S

Primary product page:

```text
https://www.cdebyte.com/products/E22-900M33S
```

Primary PDF:

```text
https://www.cdebyte.com/pdf-down.aspx?id=4216
```

Local curl header check on 2026-07-24 returned:

```text
Content-Disposition: attachment;filename=E22-M+Series+Module_UserManual_EN.pdf
Content-Length: 1729331
```

Footprint release requirements:

- Extract the exact E22-900M33S mechanical drawing from the E22-M Series user manual.
- Confirm body size, castellated pad count, pad pitch, pin-1 orientation, ANT pin location, and keepout guidance.
- Pin 21 must align with the RF GCPW launch toward J5.
- Cross-check against the exact JLCPCB/LCSC PCBA part `C22399506`.
- Use JLCPCB DFM/PCBA review as the pre-order assembler check because no loose physical module is available before Rev A fabrication and MOD2 is planned as a factory-installed part.

Transcription status:

```text
docs/E22_FOOTPRINT_TRANSCRIPTION_REV_A.md
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD2_E22_900M33S_EBYTE_MANUAL_DRAFT.kicad_mod
docs/E22_ASSEMBLER_FOOTPRINT_CROSSCHECK_REV_A.md
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD2_E22_900M33S_JLC_C22399506_IMPORT_RC.kicad_mod
```

The physical module check is deferred to Rev A first-article inspection of the factory-assembled PCB. It is not a pre-order blocker.

### J5 — Molex 0732511150 / 732511150

Primary product page:

```text
https://www.molex.com/en-us/products/part-detail/732511150
```

The Molex product page identifies:

- Part number: `732511150`
- PCB mounting: edge mount
- Recommended PCB thickness: `1.60mm`
- Impedance: `50 ohms`
- Frequency: `18 GHz`
- Reverse polarity: no
- Packaging: tray

Required drawing before footprint release:

```text
Sales Drawing SD-73251-115-001
```

Current blocker:

```text
docs/MOLEX_SMA_FOOTPRINT_BLOCKER_REV_A.md
```

JLC/LCSC assembly/import reference:

```text
C841205
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/J5_SMA_MOLEX_732511150_C841205_IMPORT_RC.kicad_mod
```

The imported footprint is kept as a release-candidate source artifact only. It is not placed on the board because its `Edge.Cuts` launch geometry must be reviewed against the official Molex sales drawing and RoyalNode's final controlled-impedance stack-up.

2026-07-25 recheck: the official Molex product page for `732511150` confirms the selected connector class, 1.60 mm board-thickness recommendation, 18 GHz frequency rating and 50 ohm impedance, but the released layout remains blocked until the sales drawing/recommended launch geometry is checked.

Footprint release requirements:

- Use the Molex sales drawing, not a generic SMA edge footprint.
- Confirm board-edge relationship, center-contact pad, shell/ground pads, ground tabs, plated/non-plated holes if any, and courtyard.
- Merge the connector launch with the final fabricator-controlled GCPW geometry after the 4-layer stack-up is selected.

## Power and Charger Sources

### F1 — Littelfuse 0483005.DR

Primary product family:

```text
https://www.littelfuse.com/products/fuses-overcurrent-protection/fuses/surface-mount-fuses/thin-film-chip-fuses/483
```

Specific candidate product page:

```text
https://www.littelfuse.com/products/fuses-overcurrent-protection/fuses/surface-mount-fuses/thin-film-chip-fuses/483/0483005-dr
```

2026-07-25 recheck: Littelfuse's official product page and 483-series datasheet identify `0483005.DR` as a 5 A, 1206, surface-mount, fast-acting 483-series fuse. The page also lists 65 V rating, 50 A interrupt current, 0.027 ohm nominal resistance and -55 C to +125 C operating temperature. These facts support the 6 V / 20 W solar-input current target, but the exact selected panel `Isc`, thermal derating and time-current coordination must still be reviewed before fabrication release.

Release requirement:

- Confirm the exact `0483005.DR` ordering code belongs to the Littelfuse 483 series 1206 chip-fuse package.
- Verify land pattern against the current Littelfuse 483 package drawing before release.
- Confirm the fuse current rating and interrupt behavior against the selected solar panel `Isc` and the upstream wiring.
- Current project footprint: `F1_LITTELFUSE_483_1206_RC`.

### C503 — Panasonic 10SVPC330M

Required source:

```text
Panasonic 10SVPC330M package drawing / SP-Cap datasheet
JLCPCB/LCSC assembly reference: C347574
```

Release requirement:

- Confirm body diameter/height and land pattern for the 8 x 6.9 mm SMD polymer can package.
- Confirm pad 1 is the positive terminal in the KiCad footprint and in the Panasonic/JLC assembly data.
- Maintain visible polarity marking in F.Fab and silkscreen.
- Current project footprint: `C503_PANASONIC_10SVPC330M_8X6P9_RC`.

### U1 — TI BQ25798RQMR

Required source:

```text
Texas Instruments BQ25798 datasheet, package drawing RQM0029A
```

Release requirement:

- TI RQM0029A HOTROD footprint or TI-provided ECAD checked dimension-by-dimension.
- Generic 4 mm x 4 mm QFN footprints are prohibited.

### U3 — TI TPS61088RHLR

Required source:

```text
Texas Instruments TPS61088 datasheet, package drawing RHL0020A
```

Release requirement:

- Exposed thermal/power pad must be pad `21`, matching the RoyalNode symbol and TI pin table.
- Thermal-via and paste strategy must be captured in footprint notes.

### L1 / L2 — Coilcraft XAL7070 / XAL7030

Required sources:

```text
Coilcraft XAL7070-222MEC datasheet and recommended land pattern
Coilcraft XAL7030-222MEC datasheet and recommended land pattern
```

Release requirement:

- Use Coilcraft recommended land patterns and courtyards.
- Keep body courtyards honest; these inductors drive power-stage spacing.

## Connector Sources

### J1 / J2 — AMASS XT30PW-M

Required source:

```text
AMASS XT30PW-M manufacturer drawing or trusted factory CAD from assembly supplier
```

Current JLC/LCSC import reference:

```text
C431092
MPN: XT30PW-M30.G.Y
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/J_POWER_XT30PW_M_C431092_RC.kicad_mod
```

JLC/LCSC identify `C431092` as a Changzhou Amass Elec XT30PW-M30.G.Y male right-angle connector with 2 pins, 15 A rated current, 500 VDC rated voltage, 1.2 milliohm contact resistance, 16/18/20 AWG recommended wire gauge, and wave-solder PCBA support.

Release requirement:

- Confirm pin polarity against the physical connector molding before Gerber release.
- Include mating plug clearance and clear `SOLAR` / `BATTERY` silkscreen.

RoyalNode's local release-candidate footprint moves imported decorative body art to `F.Fab` while preserving the imported electrical pad geometry. This keeps KiCad DRC focused on copper and assembly geometry rather than JLC library silkscreen art.

### MOD1 — XIAO socket strips

Current JLC/LCSC import reference:

```text
C53202181
MPN: LXWCONN 254PM-1x7P-V
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD1_XIAO_SOCKET_1X7_C53202181_RC.kicad_mod
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD1_XIAO_NRF52840_SOCKET_C53202181_RC.kicad_mod
```

JLCPCB identifies `C53202181` as a LXWCONN 254PM-1x7P-V 1x7, 2.54 mm through-hole female header with wave-solder PCBA support.

RoyalNode uses a composite MOD1 footprint containing two socket strips on 17.78 mm row spacing so the single XIAO schematic symbol maps to one board footprint.

### D1 — Charge LED

Selected part:

```text
Hubei KENTO Elec KT-0603R
JLCPCB/LCSC C2286
0603 red SMT LED
```

Source pages:

```text
https://jlcpcb.com/partdetail/C2286
https://www.lcsc.com/product-detail/C2286.html
```

JLCPCB lists C2286 as an SMT assembly part for Economic and Standard PCBA, with 0603 package and red 1.8 V to 2.4 V LED description. LCSC lists the same KT-0603R part in a 1.6 mm x 0.8 mm x 0.6 mm 0603 package.

Release requirement:

- Confirm physical XIAO nRF52840 orientation.
- Confirm USB-C edge access.
- Confirm BLE antenna clearance.
- Confirm socket engagement height with the selected XIAO header pins.

### J3/J4/J6 — JST-GH Connectors

Required source:

```text
JST GH series SM02B-GHS-TB(LF)(SN) drawing
JST GH series SM04B-GHS-TB(LF)(SN) drawing
KiCad Connector_JST footprint: JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal
KiCad Connector_JST footprint: JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal
```

Release requirement:

- Pin 1 marker required.
- Mate must be JST GHR-02V-S housing with verified crimp terminal before harness release.
- J3 carries only the XIAO underside BAT/GND internal harness.
- J4 carries only the battery-mounted 103AT-2 NTC safety harness.
- J6 carries only the optional MeshCore-supported environmental I2C interface: 3V3, GND, SDA and SCL.

## Footprint Policy

A project-local footprint may be added as `draft` for placement planning, but it must include `DRAFT_NOT_RELEASED` in its description and must not be used for release routing.

Only footprints checked against the sources above can be marked `checked` or `released_rev_a`.
