# RoyalNode Rev A Molex SMA Footprint Blocker

## Status

The Molex 0732511150 / 732511150 SMA remains selected for Rev A, but its **released footprint is blocked** until the official sales drawing is obtained and checked.

Current project footprint state:

```text
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/J5_SMA_0732511150_DRAFT_ENVELOPE.kicad_mod
```

That footprint is an envelope-only planning object with no electrical pads.

## Confirmed From Official Molex Product Page

Official product page:

```text
https://www.molex.com/en-us/products/part-detail/732511150
```

Rechecked on 2026-07-25. The official page confirms:

- Part number: `732511150`
- Category: RF / Coaxial Connectors
- Gender: jack
- Orientation: straight
- PCB mounting: edge mount
- Recommended PCB thickness: 1.60 mm
- Reverse polarity: no
- Frequency: 18 GHz
- Impedance: 50 ohms
- Voltage rating: 500 Vrms at sea level

These facts are sufficient to keep the component class and BOM selection, but not sufficient to create the PCB launch.

The page also reports limited catalog information for this part, so RoyalNode must still use the official sales drawing for released copper geometry rather than deriving pad dimensions from the product page alone.

## Required Drawing

Required official drawing:

```text
Sales Drawing SD-73251-115-001
```

The footprint cannot be promoted beyond envelope/draft state until this drawing is available from Molex or an authorized source and checked.

## Terminal Access Attempt

On 2026-07-24, direct terminal attempts to retrieve the official Molex product page and likely sales-drawing URLs timed out or returned no usable response from this environment.

Tested URL classes included:

```text
https://www.molex.com/en-us/products/part-detail/732511150
https://www.molex.com/content/dam/molex/.../salesdrawingpdf/.../732511150_sd.pdf
https://www.molex.com/pdm_docs/sd/732511150_sd.pdf
```

No release footprint was created from these failed fetches.

## 2026-07-25 Web Recheck

The official Molex product page was reachable from the Codex web tool and still supports the selected component class:

- `732511150`
- standard, non-reverse-polarity SMA jack
- edge-mount PCB connector
- 1.60 mm recommended PCB thickness
- 18 GHz, 50 ohm RF rating

However, the reachable page did not expose a usable recommended PCB-layout drawing in the accessible text. The imported JLC/LCSC footprint remains a comparison artifact only:

```text
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/J5_SMA_MOLEX_732511150_C841205_IMPORT_RC.kicad_mod
```

The placed board footprint remains the draft envelope:

```text
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/J5_SMA_0732511150_DRAFT_ENVELOPE.kicad_mod
```

## Release Requirements

Before J5 can be released:

- [ ] Obtain official `SD-73251-115-001`.
- [ ] Confirm board-edge location relative to connector body.
- [ ] Confirm center-contact pad dimensions.
- [ ] Confirm shell/ground pad dimensions.
- [ ] Confirm any plated or non-plated holes.
- [ ] Confirm soldermask and paste guidance.
- [ ] Merge the launch geometry with final fabricator GCPW stack-up.
- [ ] Run a 1:1 print check.

## Policy

Do not use SnapMagic, distributor preview images, mirrored PDFs, or a generic SMA edge footprint for the released Rev A RF launch unless a human explicitly accepts that risk in a design-review note.
