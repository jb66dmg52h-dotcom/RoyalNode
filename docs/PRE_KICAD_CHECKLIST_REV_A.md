# RoyalNode Rev A Pre-KiCad Checklist

## Closed architecture items

- [x] One socketed Seeed XIAO nRF52840
- [x] EBYTE E22-900M33S
- [x] BQ25798 charger/power path
- [x] TPS61088 5 V radio supply
- [x] LM66100 XIAO BAT isolation
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

## Remaining before schematic capture

1. Freeze exact resistor manufacturer/JLC parts where tolerance matters.
2. Freeze charge LED and current-limiting resistor.
3. Freeze exact XIAO socket pair and mating pin-header geometry.
4. Freeze exact XT30 board gender/orientation for solar and battery.
5. Verify every custom symbol pin number against the manufacturer datasheet.
6. Verify every custom footprint pad number and courtyard against manufacturer mechanical drawings.
7. Produce a final net-by-net pin map suitable for direct KiCad capture.
8. Run a final contradiction search across repository design documents.

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
