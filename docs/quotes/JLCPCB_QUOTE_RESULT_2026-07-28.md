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

The first processable quote pair excluded `MOD1` and `F1` and forced JLCPCB part `C14663` for the unmatched 100 nF capacitors, but it was not fully processed into a final quote during that session.

After the user confirmed that the XIAO module will be sourced separately, the processable quote generator was updated to:

- exclude `MOD1` only as a user-supplied XIAO module
- keep `F1` in the PCBA set as Bourns `SF-1206S500-2`, JLCPCB/LCSC `C913282`
- force `C212,C213,C214` and `C404` to Yageo `CC0603KRX7R9BB104`, JLCPCB/LCSC `C14663`
- force `C215` to Samsung `CL21B475KAFNNNE`, JLCPCB/LCSC `C98195`

That post-XIAO BOM/CPL pair was processed by JLCPCB and reduced the issue set from unmatched parts to stock-shortage rows. JLCPCB showed:

- 54 parts detected
- 39 parts confirmed
- 15 parts with inventory shortage

The second substitution pass now also forces:

- `C216,C217` to `C1622`
- `C218` to `C163508`
- `C405` to `C74690`
- `J5` to exact Molex SMA `C841205`
- `J6` to GH-compatible XYECONN `C51940118`
- `Q1,Q2,Q3` to same-family Infineon candidate `C43317100`
- `R100` to `C166890`
- `R102` to `C4210499`
- `R200` to `C4076829`
- `R201` to `C1709086`
- `R400` to 180 kOhm `C4074070`
- `R401` to 57.6 kOhm `C4106968`
- `U4` to `C688323`

The processable quote files were regenerated with this second pass and then reprocessed in the signed-in JLCPCB SMT quote flow.

JLCPCB showed:

- 54 parts detected
- 45 parts confirmed
- 9 parts with inventory shortage

The remaining shortage rows were:

- `Q1`, `Q2`, `Q3` - Infineon dual N-channel PG-DSO-8 MOSFET candidates
- `R102`
- `R200`
- `R201`
- `R400`
- `R401`
- `U4`

The MOSFET rows were then excluded from the quote because no safe JLC in-stock dual N-channel PG-DSO-8 replacement was found. JLC-listed related Infineon parts included N+P devices, which are not acceptable substitutes for RoyalNode's back-to-back N-channel input selector/protection circuits.

The resistor and LTC4365 rows were retried with JLC-source alternatives, but still showed inventory shortage inside the SMT quote flow.

The successful quote path used JLCPCB's `Do not place` option for the remaining shortage rows.

## Final Successful Draft PCBA Quote

Date/time shown by JLCPCB autosave: 2026-07-28 22:14

No order was placed, and the quote was not saved to cart.

Final quote-page settings and prices shown:

- Quantity: 5 PCBAs
- PCB: 4-layer FR-4, green solder mask, white silkscreen
- Board size after JLC assembly rails: 97 mm x 97 mm
- Surface finish: ENIG
- Outer copper: 2 oz
- Inner copper: 0.5 oz
- Via covering: plugged
- PCBA type: Standard
- Assembly side: top side
- Solder paste: high temp
- PCB build time: 3 days
- Assembly build time selected: 5-6 days
- Weight shown: 1.12 kg

Charge details shown:

| Item | Price |
|---|---:|
| PCB price | USD 60.50 |
| Standard PCBA price | USD 260.29 |
| Setup fee | USD 25.56 |
| Stencil | USD 8.21 |
| Components, 32 items | USD 172.02 |
| Feeders loading fee | USD 47.43 |
| SMT assembly | USD 2.33 |
| Hand-soldering labor fee | USD 3.58 |
| Manual assembly | USD 0.66 |
| Packaging fee | USD 0.50 |
| Total price shown | USD 320.79 |

Shipping was not shown on the final PCBA quote page captured in this pass. An earlier rugged PCB+PCBA setup screen showed a shipping estimate around USD 26-28, but that should not be treated as the final shipped total.

## Excluded / Do-Not-Place Items In Final Quote

These items were not included in the successful JLC quote total:

- `MOD1` - Seeed XIAO nRF52840; user-supplied
- `J5` - Molex edge-launch SMA; recognized earlier but absent from the final placement list
- `Q1`, `Q2`, `Q3` - dual N-channel MOSFETs
- `R102`, `R200`, `R201`, `R400`, `R401` - shortage-blocked precision/feedback resistors
- `U4` - shortage-blocked LTC4365 input-protection controller

The final placement list did include major assembly items such as:

- `MOD2` EBYTE E22-900M33S, JLCPCB/LCSC `C22399506`
- `U1` BQ25798, `C2876593`
- `U2` LM66100DCKR, `C2869734`
- `U3` TPS61088RHLR, `C87357`
- `J1,J2` XT30 connectors, `C431092`
- `L1,L2` Coilcraft power inductors, `C3911470` and `C19191686`

See `docs/quotes/JLCPCB_SUBSTITUTIONS_REV_A_2026-07-28.md`.

## Do Not Order Yet

This quote used draft fabrication files. The project currently has clean ERC/DRC/unconnected checks, but the package is still marked draft because these items need release review before fabrication:

- SMA RF launch and 50 ohm trace geometry
- Final JLCPCB stack-up selection
- Power supply layout review
- BOM LCSC part-number completion
- Assembly orientation review
