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

Transcription status:

```text
docs/E22_FOOTPRINT_TRANSCRIPTION_REV_A.md
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD2_E22_900M33S_EBYTE_MANUAL_DRAFT.kicad_mod
```

This is still not released until a physical-module check is complete.

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

Footprint release requirements:

- Use the Molex sales drawing, not a generic SMA edge footprint.
- Confirm board-edge relationship, center-contact pad, shell/ground pads, ground tabs, plated/non-plated holes if any, and courtyard.
- Merge the connector launch with the final fabricator-controlled GCPW geometry after the 4-layer stack-up is selected.

## Power and Charger Sources

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

Release requirement:

- Confirm pin polarity against the physical connector molding before Gerber release.
- Include mating plug clearance and clear `SOLAR` / `BATTERY` silkscreen.

### J3 — JST B2B-PH-SM4-TB(LF)(SN)

Required source:

```text
JST B2B-PH-SM4-TB(LF)(SN) drawing
```

Release requirement:

- Use the official JST pad layout or a KiCad standard footprint checked against it.

### J4 — CJT A2012WV-S-2P

Required source:

```text
CJT A2012WV-S-2P manufacturer/JLC assembly footprint data
```

Release requirement:

- Pin 1 marker required.
- Mate must be CJT A2012H-2P housing with verified crimp terminal before harness release.

## Footprint Policy

A project-local footprint may be added as `draft` for placement planning, but it must include `DRAFT_NOT_RELEASED` in its description and must not be used for release routing.

Only footprints checked against the sources above can be marked `checked` or `released_rev_a`.
