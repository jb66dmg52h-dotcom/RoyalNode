# RoyalNode Rev A Pre-KiCad Checklist

## Closed architecture items

- [x] One socketed Seeed XIAO nRF52840
- [x] EBYTE E22-900M33S
- [x] BQ25798 charger/power path
- [x] TPS61088 5 V radio supply
- [x] LM66100 XIAO BAT isolation architecture
- [x] 1S protected Li-ion/LiPo battery architecture
- [x] 12 V nominal solar input
- [x] Real battery NTC
- [x] No fuel gauge
- [x] No eFuse
- [x] No power button
- [x] One charge/status LED only
- [x] Direct E22-to-SMA 50-ohm RF architecture
- [x] JLCPCB fabricator and four-layer stack target

## Closed component blocks

- [x] Core ICs/modules
- [x] BQ25798 inductor
- [x] TPS61088 inductor
- [x] BQ25798 main capacitor BOM
- [x] TPS61088 main capacitor BOM
- [x] E22 ceramic decoupling
- [x] E22 330 uF polymer bulk capacitor
- [x] Battery NTC connector family
- [x] XIAO two-wire power JST
- [x] SMA connector class/part
- [x] Precision and generic resistor BOM for schematic capture
- [x] Charge/status LED and series resistor
- [x] XIAO socket pair selected
- [x] XT30 board-side gender/orientation selected

## Pin-audit status

- [x] XIAO D0-D10 GPIO map verified against Seeed documentation
- [x] XIAO dedicated battery nets verified in current Seeed schematic as `BAT0` and `GND0`; the carrier uses a wire harness rather than bottom-pad contacts
- [x] E22-900M33S 22-pin electrical pin table verified against current EBYTE documentation
- [x] TPS61088RHLR electrical pin table verified against TI Rev. D
- [x] LM66100DCKR electrical pin table verified against TI Rev. A
- [x] BQ25798RQMR full 29-pin connection map entered and checked against TI Rev. C
- [x] LTC4365ITS8-1 full 8-pin connection map entered and checked against ADI Rev. B
- [x] ISA170170N04LMDSXTMA1 dual-MOSFET pin orientation entered and checked against Infineon Rev. 2.0

The authoritative pin table is `docs/PIN_AUDIT_REV_A.md`.

## Important audit correction

The LM66100 hookup previously documented as `CE tied high` / `ST NC` was incorrect for the intended always-on reverse-current-blocking function. Rev A now uses:

- pin 3 CE -> VOUT
- pin 5 ST -> GND

This correction is incorporated into the current electrical design and net map.

## Net-map status

- [x] Final net-by-net schematic capture map created
- [x] Solar assigned to BQ25798 port 1 (`VAC1/ACDRV1`)
- [x] USB assigned to BQ25798 port 2 (`VAC2/ACDRV2`)
- [x] LTC4365 UV/OV divider topology explicitly mapped
- [x] BQ25798 charger switching nets explicitly mapped
- [x] TPS61088 switching/feedback/compensation nets explicitly mapped
- [x] E22 digital and RF nets explicitly mapped
- [x] XIAO header nets explicitly mapped

The authoritative capture map is `docs/NET_MAP_REV_A.md`.

## Footprint-audit status

- [x] BQ25798 package identified as TI `RQM0029A`, 4 x 4 mm VQFN-HR; generic QFN substitution prohibited
- [x] TPS61088 package identified as TI `RHL0020A`, including exposed PGND pad 21
- [x] LM66100 package identified as TI `DCK0006A`
- [x] LTC4365 TS8 package drawing identified as ADI `05-08-1637 Rev A`
- [x] Infineon PG-DSO-8 dual-MOSFET pad functions identified
- [x] E22 module body and 2.54 mm interface pitch verified
- [x] Molex SMA 1.60 mm edge-mount requirement verified
- [x] Pico-Lock NTC connector family mechanically identified
- [ ] E22 exact castellated-pad dimensions/centers transcribed from EBYTE mechanical drawing
- [ ] XT30PW-M exact AMASS land pattern/polarity drawing checked
- [ ] XIAO socket row spacing and male-pin engagement checked against Seeed mechanical files
- [ ] Molex SMA recommended PCB launch geometry transcribed/checked
- [ ] Imported TI/ADI/Infineon CAD footprints compared dimension-by-dimension with current package drawings

See `docs/FOOTPRINT_AUDIT_REV_A.md`.

## Remaining before schematic capture

Electrical definition is now sufficient to begin symbol creation and schematic capture. The remaining pre-capture work is mechanical/library hygiene rather than architecture:

1. Finish the remaining footprint-specific mechanical checks above.
2. Run a final contradiction scan across repository design documents.
3. Import/create the verified symbols and footprints in the project-local KiCad libraries.

Do not wait for the final RF controlled-impedance trace width to draw the schematic; that belongs to PCB routing after the production stack-up is reconfirmed.

## Remaining after schematic capture but before PCB routing

- ERC and schematic audit
- Production JLC04161H-3313 stack-up availability confirmation
- JLC controlled-impedance calculation for final 50-ohm GCPW width/gap
- SMA launch footprint verification
- Component placement/floorplan compression
- Power-loop placement audit
- RF keepout and via-fence definition

## Placement direction for compact Rev A

The board should not be sized from earlier concept renders. Mechanical size is to be minimized after real footprints are loaded.

Preferred zoning:

```text
SOLAR/BAT connectors -> protection + BQ25798 -> battery/system region
                                      |
                                      +-> XIAO + small-signal/control
                                      |
                                      +-> TPS61088 -> E22 -> very short RF -> SMA edge
```

- E22 ANT side faces the SMA edge.
- E22 and SMA are immediate neighbors.
- TPS61088 remains close enough to E22 for a short, low-impedance 5 V path but its SW node is kept away from the ANT/SMA launch.
- Charger and solar switching region remain on the opposite side of the RF launch where practical.
- Board outline is drawn only after real connector/module footprints are placed tightly enough to establish the actual minimum practical dimensions.
