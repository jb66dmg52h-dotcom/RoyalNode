# RoyalNode Rev A E22 Footprint Transcription

## Status

A project-local E22 footprint transcription has been created:

```text
hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD2_E22_900M33S_EBYTE_MANUAL_DRAFT.kicad_mod
```

This footprint is **not released**. It is a manufacturer-manual draft used as one side of the Rev A footprint audit.

Because no loose physical E22-900M33S module is available before the first board order, physical module verification is no longer a pre-order blocker. MOD2 is intended to be factory-installed during PCBA, so the pre-order gate is now the assembler-footprint cross-check in:

```text
docs/E22_ASSEMBLER_FOOTPRINT_CROSSCHECK_REV_A.md
```

## Source

Manufacturer PDF:

```text
https://www.cdebyte.com/pdf-down.aspx?id=4216
```

Local reviewed file:

```text
tmp/pdfs/E22-M_Series_Module_UserManual_EN.pdf
```

Reviewed rendered pages:

```text
tmp/pdfs/e22_page-10.png
tmp/pdfs/e22_page-11.png
```

Relevant manual section:

```text
3.3 E22-170/400/900M30S(33S) Mechanical Dimensions and Pin Definitions
```

## Transcribed Dimensions

| Item | Value | Source note |
|---|---:|---|
| Body width | 24.0 +/- 0.1 mm | Drawing top dimension |
| Body length | 38.5 +/- 0.1 mm | Drawing side dimension |
| Module height | 3.87 +/- 0.1 mm | Drawing side view |
| Pad quantity | 22 | Drawing note |
| Bottom land width into module | 1.25 mm | Bottom pad detail |
| Bottom land height along edge | 1.50 mm | Bottom pad detail |
| Pad edge/castellation width | 0.80 mm | Pad detail |
| Pin pitch inside groups | 2.54 mm | Drawing side dimension |
| Upper-to-lower group gap | 7.60 mm | Drawing side dimension |
| Top edge to first upper pad center | 2.61 mm | Drawing side dimension |
| Last lower pad center to bottom edge | approximately 5.46 mm | Drawing side dimension |

## Footprint Coordinate Convention

Origin is at the module body center.

```text
Body left edge:   X = -12.000 mm
Body right edge:  X = +12.000 mm
Body top edge:    Y = -19.250 mm
Body bottom edge: Y = +19.250 mm
```

Pads are 1.25 mm x 1.50 mm SMD rectangles placed so their outer edge aligns with the module body edge:

```text
Left-side pad center X  = -11.375 mm
Right-side pad center X = +11.375 mm
```

Upper group first pad center:

```text
Y = -19.250 + 2.610 = -16.640 mm
```

Upper group pitch:

```text
2.54 mm
```

Lower group first pad center:

```text
Y = -16.640 + 7 * 2.540 + 7.600 = +8.740 mm
```

## Pin Placement

| Pin | X | Y | Note |
|---:|---:|---:|---|
| 1 | +11.375 | +13.820 | Right lower group |
| 2 | +11.375 | +11.280 | Right lower group |
| 3 | +11.375 | +8.740 | Right lower group |
| 4 | +11.375 | +1.140 | Right upper group |
| 5 | +11.375 | -1.400 | Right upper group |
| 6 | +11.375 | -3.940 | Right upper group |
| 7 | +11.375 | -6.480 | Right upper group |
| 8 | +11.375 | -9.020 | Right upper group |
| 9 | +11.375 | -11.560 | Right upper group |
| 10 | +11.375 | -14.100 | Right upper group |
| 11 | +11.375 | -16.640 | Right upper group |
| 12 | -11.375 | -16.640 | Left upper group |
| 13 | -11.375 | -14.100 | Left upper group |
| 14 | -11.375 | -11.560 | Left upper group |
| 15 | -11.375 | -9.020 | Left upper group |
| 16 | -11.375 | -6.480 | Left upper group |
| 17 | -11.375 | -3.940 | Left upper group |
| 18 | -11.375 | -1.400 | Left upper group |
| 19 | -11.375 | +1.140 | Left upper group |
| 20 | -11.375 | +8.740 | Left lower group, RF ground |
| 21 | -11.375 | +11.280 | ANT, 50 ohm stamp-hole interface |
| 22 | -11.375 | +13.820 | Left lower group, RF ground |

## Pin-Function Confirmation

The manual table confirms:

- Pin 6: RXEN
- Pin 7: TXEN
- Pin 8: DIO2
- Pins 9 and 10: VCC
- Pin 13: DIO1
- Pin 14: BUSY
- Pin 15: NRST
- Pin 16: MISO
- Pin 17: MOSI
- Pin 18: SCK
- Pin 19: NSS
- Pin 21: ANT, 50 ohm characteristic impedance
- Pin 22: GND
- DIO3 is internal and powers the 32 MHz TCXO when configured for 2.2 V

## Manual-Transcription Checklist

- [x] Transcribe body size, pad count, pitch, and pad-center pattern from the EBYTE manual.
- [x] Confirm Pin 21 is ANT and pins 20/22 are RF grounds.
- [x] Create a project-local manual-draft KiCad footprint.
- [x] Import the exact JLC/LCSC `C22399506` EasyEDA footprint for comparison.
- [x] Document the JLC/EasyEDA larger-pad land pattern and origin difference.
- [ ] Confirm paste/mask behavior with the PCB assembler during DFM/PCBA review.
- [ ] Run first-article physical inspection after the first factory-assembled Rev A board arrives.
