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
- [x] E22-900M33S 22-pin electrical pin table verified against EBYTE current product documentation
- [x] TPS61088RHLR electrical pin table verified against TI Rev. D
- [x] LM66100DCKR electrical pin table verified against TI Rev. A
- [ ] BQ25798RQMR full 29-pin connection map entered and checked against TI Rev. C
- [ ] LTC4365ITS8-1 full 8-pin connection map entered and checked against ADI Rev. B
- [ ] ISA170170N04LMDSXTMA1 dual-MOSFET pin orientation entered and checked against Infineon Rev. 2.0

## Important audit correction

The LM66100 hookup previously documented as `CE tied high` / `ST NC` is incorrect for the intended always-on reverse-current-blocking function. TI specifies:

- pin 3 CE must not float; connecting CE to VOUT enables always-on reverse-current blocking
- pin 5 ST should be connected to GND when the status output is not used

The canonical electrical/net-map documents must use CE -> VOUT and ST -> GND. This correction is mandatory before schematic capture.

## Remaining before schematic capture

1. Finish the BQ25798, LTC4365 and dual-MOSFET pin-level audit.
2. Correct all canonical LM66100 connection references to CE -> VOUT and ST -> GND.
3. Verify every custom footprint pad number and courtyard against manufacturer mechanical drawings.
4. Verify XIAO male-header pin engagement with the selected sockets.
5. Produce a final net-by-net pin map suitable for direct KiCad capture.
6. Run a final contradiction search across repository design documents.

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
