# JLCPCB Quote Result - RoyalNode Rev A Draft

Date checked: 2026-07-28

This is a quote-only result from the JLCPCB online quote flow. No order was placed.

## Uploaded PCB Package

Uploaded file:

`RoyalNode_RevA_JLCPCB_PCB_QUOTE_UPLOAD_DRAFT.zip`

JLCPCB detected:

- Board type: standard rigid PCB
- Material: FR-4
- Layers: 4
- Board size: 87 mm x 97 mm detected, fields shown as 97 mm x 87 mm
- Quantity: 5
- PCB color: green
- Silkscreen: white
- Via covering: plugged
- Electrical test: flying probe fully test

## Bare PCB Quotes Shown

### Baseline Default Quote

Settings:

- Surface finish: HASL with lead
- Outer copper: 1 oz
- Inner copper: 0.5 oz
- Build time: 3-4 days

Price shown:

- PCB price: USD 7.00
- Shipping estimate: USD 27.92, DHL Express DDP, 2-4 business days
- Weight: 0.27 kg

Approximate visible total before taxes/fees/coupons:

- USD 34.92

### Preferred ENIG Quote

Settings:

- Surface finish: ENIG
- Outer copper: 1 oz
- Inner copper: 0.5 oz
- Build time: 3-4 days

Price shown:

- PCB price: USD 24.40
- Surface finish charge: USD 17.40
- Shipping estimate: USD 27.92, DHL Express DDP, 2-4 business days
- Weight: 0.27 kg

Approximate visible total before taxes/fees/coupons:

- USD 52.32

### Rugged ENIG + 2 oz Outer Copper Quote

Settings:

- Surface finish: ENIG
- Outer copper: 2 oz
- Inner copper: 0.5 oz
- Build time: 3-4 days
- PCBA toggle enabled, top-side assembly, standard PCBA selected

Price shown:

- PCB price: USD 60.50 after enabling PCBA flow
- Surface finish charge: USD 17.50
- Outer copper charge: USD 36.00
- Shipping estimate: USD 27.92, DHL Express DDP, 2-4 business days
- Weight: 0.30 kg

Approximate visible total before taxes/fees/coupons:

- USD 88.42

The same rugged settings showed USD 60.10 immediately before enabling the PCBA quote section. The small difference appears to come from the PCBA flow's edge-rail/assembly handling.

## Assembly Quote Status

PCB assembly was enabled in the quote form:

- PCBA type: Standard
- Assembly side: top side
- PCBA quantity: 5
- Edge rails/fiducials: added by JLCPCB
- Parts selection: by customer
- Solder paste: high temp

JLCPCB did not provide component or SMT assembly pricing on the first quote screen. Pressing Next redirected to JLCPCB sign-in, so full BOM/CPL component matching and final PCBA price require a signed-in JLCPCB session.

The current draft BOM still has missing LCSC part numbers, so the assembly quote will also need part matching and likely manual substitutions before it can become a real manufacturing quote.

## Logged-In PCBA Attempt

After signing in to JLCPCB, the BOM/CPL flow was retried.

The original CPL export failed JLCPCB processing. A corrected sample-format CPL was generated with:

- `Designator`
- `Mid X`
- `Mid Y`
- `Layer`
- `Rotation`
- Coordinate values using `mm` suffixes
- Positive Y coordinates instead of KiCad's negative placement Y values

A corrected sample-format BOM was also generated using JLCPCB's sample headers:

- `Comment`
- `Designator`
- `Footprint`
- `JLCPCB Part #（optional）`

With those files, JLCPCB successfully processed the placement data and reported:

- 55 parts detected
- 36 parts confirmed
- 15 parts with inventory shortage
- 4 parts not selected

The four not-selected rows were:

- `C212,C213,C214` - 100 nF 50 V X7R, 0603
- `C404` - 100 nF 50 V X7R, 0603
- `F1` - Littelfuse `0483005.DR` SMD fuse
- `MOD1` - Seeed XIAO nRF52840 module

JLCPCB would not advance to a complete Quote & Order price while those unselected rows remained unresolved. Therefore the final assembled PCBA price was not available yet.

Generated retry files:

- `RoyalNode_RevA_JLCPCB_BOM_SAMPLE_FORMAT.csv`
- `RoyalNode_RevA_JLCPCB_CPL_SAMPLE_FORMAT.csv`
- `RoyalNode_RevA_JLCPCB_BOM_PROCESSABLE_QUOTE.csv`
- `RoyalNode_RevA_JLCPCB_CPL_PROCESSABLE_QUOTE.csv`

The processable quote pair excludes `MOD1` and `F1` and forces JLCPCB part `C14663` for the unmatched 100 nF capacitors, but it was not fully processed into a final quote during this session.

## Do Not Order Yet

This quote used draft fabrication files. The project currently has clean ERC/DRC/unconnected checks, but the package is still marked draft because these items need release review before fabrication:

- SMA RF launch and 50 ohm trace geometry
- Final JLCPCB stack-up selection
- Power supply layout review
- BOM LCSC part-number completion
- Assembly orientation review
