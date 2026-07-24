# RoyalNode Rev A E22 Assembler Footprint Cross-Check

## Decision

RoyalNode Rev A will not require a physical E22-900M33S module before the first board order. The user will not have the module until the board is produced, so the release gate is changed to a controlled remote verification path:

1. Transcribe the EBYTE manufacturer drawing.
2. Import the exact JLCPCB/LCSC EasyEDA footprint for `C22399506`.
3. Compare pin count, pitch, body class, pin 21 ANT location, and RF-ground adjacency.
4. Use JLCPCB DFM/PCBA review before order submission.
5. Inspect the first assembled board or first received module as the physical first article.

This does not make the footprint risk disappear. It moves the physical-fit check from a pre-order blocker to a documented Rev A risk accepted for the first build.

## Sources Checked

### Manufacturer drawing

EBYTE E22-M Series module user manual:

```text
https://www.cdebyte.com/pdf-down.aspx?id=4216
```

Reviewed section:

```text
3.3 E22-170/400/900M30S(33S) Mechanical Dimensions and Pin Definitions
```

### Assembler and distributor part records

JLCPCB part page:

```text
https://jlcpcb.com/partdetail/Chengdu_Ebyte_ElecTech-E22900M33S/C22399506
```

JLCPCB identifies:

- Manufacturer part: `E22-900M33S`
- JLCPCB part: `C22399506`
- Package: `SMD,38.5x24mm`
- Antenna type: stamp-hole antenna and IPEX interface
- Interface: SPI
- Supply: 3.3 V to 5.5 V
- Transmit current: 1200 mA class
- EasyEDA symbol and PCB footprint available

LCSC product page:

```text
https://www.lcsc.com/product-detail/C22399506.html
```

LCSC identifies:

- Manufacturer: `EBYTE`
- MPN: `E22-900M33S`
- LCSC part: `C22399506`
- Packaging: `SMD,38.5x24mm`
- Key attributes: `868/915MHz 2W SPI Surface-Mount LoRa Module`
- Antenna type: IPEX interface and stamp-hole antenna

JLCPCB EasyEDA footprint export instructions:

```text
https://jlcpcb.com/help/article/how-to-export-footprints-from-easyeda
```

## Imported Library Artifact

The EasyEDA/JLC footprint was imported with:

```text
tmp/easyeda2kicad-venv/bin/easyeda2kicad --lcsc_id C22399506 --footprint --output tmp/easyeda_c22399506/e22 --overwrite --debug
```

The tool reported:

```text
Created Kicad footprint for ID: C22399506
Footprint name: COMM-SMD_22P-P2.54-L38.5-W24.0_E22-400M33S
```

The generated footprint name includes `E22-400M33S`, but the import source was the exact LCSC/JLCPCB ID `C22399506`, whose product record is `E22-900M33S`. Treat the name as an EasyEDA series-library artifact, not as a part substitution.

Repository artifact:

```text
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD2_E22_900M33S_JLC_C22399506_IMPORT_RC.kicad_mod
```

Status:

```text
NOT_RELEASED_RELEASE_CANDIDATE
```

## Geometry Comparison

| Check | EBYTE manual transcription | JLC/EasyEDA import | Result |
|---|---:|---:|---|
| Pin count | 22 | 22 | Match |
| Body class | 38.5 x 24.0 mm | 38.5 x 24.0 mm class | Match |
| Pitch | 2.54 mm | 2.54 mm | Match |
| Pin 21 | ANT | pad 21 present | Match |
| RF grounds | pins 20 and 22 | pads 20 and 22 adjacent | Match |
| Pad size | 1.25 x 1.50 mm | 1.50 x 2.20 mm | Difference |
| Pad X center | +/-11.375 mm | +/-11.650 mm | Difference |
| Pad Y centers | manual body-center origin | EasyEDA origin shifted by about +1.4 mm | Difference |

The JLC/EasyEDA import uses larger pads than the manual transcription. For Rev A, that is acceptable as a release-candidate direction because JLCPCB is the intended assembler and their library footprint is tied to the exact PCBA part number.

## Rev A Footprint Policy

Use the imported JLC/EasyEDA footprint as the preferred starting point for JLCPCB PCBA, with these constraints:

- Keep the footprint marked as a release candidate until schematic symbols and placement are complete.
- Do not hand-edit pad geometry without recording the reason in this document.
- Place pin 21 toward the SMA edge.
- Connect pins 20 and 22 to the RF ground structure with very short paths.
- Submit the Rev A design through JLCPCB DFM and PCBA review before ordering.
- Record any JLC footprint/placement feedback before approving the order.

If JLCPCB rejects or modifies the module footprint during DFM/PCBA review, their correction takes priority over this imported footprint and must be committed before Gerber release.

## First-Article Check

Because no physical E22-900M33S module is available before the board order, the first physical check happens after either:

- JLCPCB assembles MOD2 on the first Rev A board, or
- a separately ordered E22-900M33S module arrives.

First-article inspection must verify:

- all 22 pads visibly align with the module castellations
- pin 1 orientation
- pin 21 ANT side faces the board SMA
- no solder bridging at pins 20/21/22
- module sits flat
- SMA/RF corridor is not blocked by the module body
- RF output is tested only with a proper 50-ohm load or antenna attached

## Accepted Risk

Proceeding without a pre-order physical module carries real footprint risk. Rev A accepts that risk because:

- EBYTE provides a manufacturer drawing for the module family.
- JLCPCB/LCSC list the exact part `C22399506`.
- The exact part has a JLC/EasyEDA footprint available.
- The key electrical/RF pin identities match the manual audit.
- The first order is an engineering-validation build, not production.

