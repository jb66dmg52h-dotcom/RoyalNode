# RoyalNode Rev A Footprint / Package Audit

## Status

This file records the package drawing that each KiCad footprint must match. It does not authorize using a generic footprint merely because the package name sounds similar. Before PCB release, pad numbers, land dimensions, exposed pads, mechanical keepouts, and connector board-edge geometry must be checked against the cited manufacturer drawing/CAD.

## U1 — BQ25798RQMR

- Manufacturer: Texas Instruments
- Package: RQM, 29-pin VQFN-HR / HOTROD
- TI package drawing: `RQM0029A`
- Nominal body: 4.0 mm x 4.0 mm
- Body tolerance shown by TI: 3.9-4.1 mm x 3.9-4.1 mm
- Height: 0.8-1.0 mm
- This is not a generic symmetric 29-pin QFN. The HOTROD land pattern has mixed pad geometries and must follow TI's `RQM0029A` recommended board layout.

KiCad rule:

- Prefer TI-provided CAD/Ultra Librarian footprint if the downloaded footprint is checked against `RQM0029A`.
- Otherwise build a project-local custom footprint from the TI land pattern.
- Do not substitute a generic 4x4 QFN footprint.
- Pin numbers must exactly match `PIN_AUDIT_REV_A.md`.

## U2 — LM66100DCKR

- Manufacturer: Texas Instruments
- Package: DCK, 6-pin SOT-SC70
- TI package drawing: `DCK0006A`
- JEDEC family: MO-203 variation AB
- Body envelope from current TI drawing: about 1.8-2.4 mm long x 1.1-1.4 mm wide
- Lead pitch: 0.65 mm
- Maximum package height: 1.1 mm

KiCad rule:

- A standard SOT-SC70-6 footprint is acceptable only if its pad geometry is checked against current `DCK0006A`.
- Pin 1 orientation must be visually marked on F.Silk/F.Fab.
- Electrical pin mapping is VIN=1, GND=2, CE=3, NC=4, ST=5, VOUT=6.

## U3 — TPS61088RHLR

- Manufacturer: Texas Instruments
- Package: RHL, 20-pin VQFN plus exposed thermal pad
- TI package drawing: `RHL0020A`
- Body: 3.4-3.6 mm x 4.4-4.6 mm
- Maximum height: 1.0 mm
- Signal-pad pitch: 0.5 mm where specified by drawing
- Exposed thermal/power pad exists and is electrically PGND.

KiCad rule:

- The exposed pad must be **pad 21**, matching the device pin table even though the package is described as 20-pin.
- Use the TI recommended land pattern, including thermal-via concept under the exposed pad.
- Do not use a generic 3.5 x 4.5 QFN footprint unless it has been dimension-by-dimension checked against `RHL0020A`.

## U4 — LTC4365ITS8-1#TRMPBF

- Manufacturer: Analog Devices
- Package: TS8, 8-lead plastic TSOT-23
- LTC drawing: `05-08-1637 Rev A`
- JEDEC reference: MO-193
- Body length: 2.90 mm BSC
- Body width: 1.50-1.75 mm
- Lead pitch: 0.65 mm
- Maximum height: 1.00 mm

Analog Devices publishes a recommended solder-pad layout for this exact TS8 drawing. Use that pad layout rather than guessing from a generic SOT-23-8 library part.

## Q1/Q2/Q3 — ISA170170N04LMDSXTMA1

- Manufacturer: Infineon
- Package: PG-DSO-8 / SO-8 class
- Device: dual N-channel MOSFET
- Current product status: active/preferred

Electrical pad numbering is critical:

| Pad | Function |
|---:|---|
| 1 | Source 1 |
| 2 | Gate 1 |
| 3 | Drain 2 |
| 4 | Gate 2 |
| 5 | Drain 2 |
| 6 | Source 2 |
| 7 | Drain 1 |
| 8 | Drain 1 |

KiCad rule:

- Use Infineon's PG-DSO-8 land-pattern/CAD package, not a randomly chosen SOIC-8 symbol/footprint pairing.
- Symbol must expose the duplicated drain pins exactly as shown above.
- All three packages use the same orientation convention in Rev A.

## M1 — EBYTE E22-900M33S

- Manufacturer: EBYTE
- Module size verified by EBYTE: 38.5 mm x 24.0 mm
- Mount: castellated/stamp-hole SMD module
- Interface pitch listed by EBYTE: 2.54 mm
- Pin count: 22
- ANT interface: pin 21, nominal 50 ohms
- Adjacent RF grounds: pins 20 and 22

KiCad rule:

- Use an E22-900M33S-specific footprint. Do not substitute another E22-series footprint without checking the exact mechanical drawing.
- The module body courtyard must include the full 38.5 x 24 mm outline.
- Place the ANT end toward the SMA board edge.
- Pin 21 must launch directly into the RF GCPW without a long neck or detour.
- Rev A may use the JLCPCB/LCSC `C22399506` EasyEDA import as a conditional release candidate because no loose physical module is available before fabrication and MOD2 is planned as a factory-installed PCBA item.
- The imported footprint must remain traceable to the exact JLC/LCSC part ID and must pass JLCPCB DFM/PCBA review before order approval.

## J_RF — Molex 0732511150 / 732511150

- Manufacturer: Molex
- Type: standard-polarity SMA jack
- Mount: straight PCB edge mount
- Impedance: 50 ohms
- Frequency rating: 18 GHz
- Manufacturer recommended PCB thickness: 1.60 mm

KiCad rule:

- Use Molex's exact connector CAD/recommended launch, not a generic SMA-edge footprint.
- Board edge position is part of the footprint/mechanical definition.
- The final RF center-pad transition must be merged with JLCPCB's controlled-impedance GCPW geometry, not simply continued at arbitrary width under the connector.

## J3/J4/J6 — JST-GH Low-Current Connectors

- Manufacturer: JST
- Series: GH
- Circuits: 2 for J3/J4; 4 for J6
- Pitch: 1.25 mm
- Orientation: horizontal SMT
- Project-local release-candidate footprint: `J_LOW_JST_GH_SM02B_GHS_TB_RC`
- Project-local release-candidate footprint: `J_LOW_JST_GH_SM04B_GHS_TB_RC`
- Source geometry: KiCad `Connector_JST:JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal`
- Source geometry: KiCad `Connector_JST:JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal`
- Mating cable housing target: JST `GHR-02V-S`, with final crimp terminal selected during harness release
- J6 mating cable housing target: JST `GHR-04V-S`, with final crimp terminal selected during harness release

KiCad rule:

- Use the JST-GH family for J3, J4 and J6 so RoyalNode keeps one low-current connector family.
- Pin 1 silkscreen marker is mandatory because J3 pin 1 is `XIAO_BAT_ISO` and J4 pin 1 is `NTC_SENSE`.
- J3 is an internal two-wire XIAO underside BAT/GND harness, not a user-accessory port.
- J4 is a required battery charge-temperature safety input, not deployed MeshCore telemetry.
- J6 is limited to the optional MeshCore-supported BME680/environmental I2C interface: `3V3`, `GND`, `I2C_SDA` and `I2C_SCL`.

## J_BAT / J_SOLAR — AMASS XT30PW-M

- Manufacturer: AMASS
- Board side: male XT30PW-M
- Orientation: right-angle PCB mount
- Both connectors use the same part.
- JLC/LCSC import source: `C431092`, `XT30PW-M30.G.Y`
- Local release-candidate footprint: `J_POWER_XT30PW_M_C431092_RC`

KiCad rule:

- Use the imported JLC/LCSC geometry as the current release candidate, with final polarity and mating-clearance review before release.
- Add mechanical courtyard for the connector body and mating plug insertion/removal.
- Silkscreen must unambiguously read `BATTERY` and `SOLAR` because the connectors are mechanically interchangeable but electrically very different.
- Pin polarity must be checked against the physical connector molding before Gerber release.

## F1 — Littelfuse 0483005.DR

- Manufacturer: Littelfuse
- Series: 483 thin-film chip fuse
- Function: solar input fuse
- Locked candidate value: 5 A
- Current official-page characteristics checked on 2026-07-25: 65 V rating, 50 A interrupt current, 0.027 ohm nominal resistance, -55 C to +125 C operating temperature
- Package target: 1206 / 3216 metric chip fuse
- Project-local release-candidate footprint: `F1_LITTELFUSE_483_1206_RC`

KiCad rule:

- Use a 1206 chip-fuse footprint only after confirming the current Littelfuse 483 package drawing for the exact `0483005.DR` ordering code.
- Place F1 immediately after the solar XT30 positive pin and before the LTC4365-controlled protection path.
- Maintain enough copper width for the expected 6 V / 20 W solar-panel current while preserving fuse function.

## XIAO sockets

- 2 x LXWCONN 254PM-1x7P-V
- 1x7, 2.54 mm pitch female sockets
- two rows spaced to match the Seeed XIAO 14-pin DIP geometry
- XIAO module body: 21 mm x 17.8 mm
- JLC/LCSC import source: `C53202181`
- Local composite release-candidate footprint: `MOD1_XIAO_NRF52840_SOCKET_C53202181_RC`

KiCad rule:

- Use the project-local combined XIAO socket footprint so the single MOD1 schematic symbol maps to one PCB footprint.
- Do not add carrier pads under the XIAO underside battery pads: battery power is through the separate JST harness, not through carrier pogo/SMD pads.
- Maintain access to the XIAO USB-C connector and reset button.

## XIAO underside battery pads

Seeed's current XIAO nRF52840 schematic names the dedicated battery-pad nets `BAT0` and `GND0`. Seeed separately publishes `XIAO nRF52840 Bottom Pad Data` for mechanical positioning.

RoyalNode uses these only as manually soldered harness endpoints:

- JST-GH positive -> XIAO `BAT0`
- JST-GH negative -> XIAO `GND0`

Because they are not carrier-board contacts, their geometry does not need to be duplicated in the RoyalNode PCB footprint. Their physical location matters only for wire exit/strain relief and XIAO removal clearance.

## Passives

- 0402, 0603, 1206, 1210 footprints may use verified KiCad standard metric/imperial land patterns where they match component datasheets and JLC assembly rules.
- The Panasonic 10SVPC330M polymer capacitor uses project-local release-candidate footprint `C503_PANASONIC_10SVPC330M_8X6P9_RC`, copied from KiCad `CP_Elec_8x6.9`.
- C503 pad 1 is positive and connects to `5V_RADIO`; pad 2 connects to GND.
- C503 polarity and the 8 x 6.9 mm can land pattern must be checked against Panasonic/JLC assembly data before release.
- Coilcraft XAL7030 and XAL7070 inductors require their exact Coilcraft recommended land patterns and body courtyards.

## Footprint release checklist

Before PCB placement begins, each non-generic footprint must have:

- [ ] manufacturer drawing/CAD source recorded in footprint properties or description
- [ ] pad numbering checked against `PIN_AUDIT_REV_A.md`
- [ ] pin-1 / polarity marking on F.Fab and appropriate F.Silk
- [ ] courtyard checked for actual body and connector mating space
- [ ] 3D model orientation checked where a verified model is available
- [ ] paste openings checked for exposed-pad/HOTROD parts
- [ ] no test-only pads or unpopulated experimental footprints added

## Current footprint audit status

Package families and major mechanical constraints are now identified. The remaining manual transcription/review work before release routing is concentrated in:

1. E22 JLC/LCSC footprint warning resolution or explicit manufacturing-review acceptance.
2. XT30PW-M polarity and mating-plug clearance.
3. XIAO socket orientation, USB-C clearance, antenna clearance, and socket engagement.
4. Molex SMA exact launch geometry.
5. TI/ADI/Infineon/Coilcraft power-stage footprints against package drawings.

These are footprint-construction tasks, not unresolved electrical architecture.
