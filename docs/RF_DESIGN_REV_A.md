# RoyalNode Rev A RF Design

## Status

RF architecture is frozen for schematic capture. Transmission-line dimensions remain dependent on the final PCB fabricator stack-up.

## Radio interface

- Radio module: EBYTE E22-900M33S.
- E22 pin 21 ANT is the module's nominal 50-ohm antenna interface.
- E22 pins 20 and 22 are the adjacent RF ground pins and must connect into the RF ground region with very short paths and nearby ground vias.
- Carrier does not add an RF matching network between the module ANT pin and the SMA.

## Locked RF schematic

```text
E22 pin 20 GND ---- local RF ground

E22 pin 21 ANT ===== 50-ohm grounded coplanar waveguide ===== SMA center

E22 pin 22 GND ---- local RF ground
```

The ANT-to-SMA path contains no series resistor, no pi matching/tuning network and no series DC-block capacitor.

## Transmission line

- Structure: grounded coplanar waveguide (GCPW/CPWG) on the component layer.
- Nominal impedance: 50 ohms.
- Reference: continuous Layer-2 ground plane directly beneath the complete RF route.
- Trace width and coplanar gap are NOT fixed generic dimensions. They must be calculated from the actual production stack-up, including dielectric thickness, dielectric constant and finished copper thickness.
- Fabrication drawing shall call out controlled impedance and the fabricator's stated tolerance.

## Routing rules

- Keep the route as short and straight as practical.
- Avoid 90-degree corners; use a straight route where placement permits and gentle/mitered direction changes only when necessary.
- Do not route digital, charger or boost-converter signals beneath the RF route.
- Do not place Layer-2 plane splits, slots or voids beneath the RF route.
- Keep BQ25798 and TPS61088 high-di/dt loops and switching nodes away from the E22 ANT/SMA end of the board.
- Keep SPI, I2C and radio-control traces from running parallel beside the RF route for unnecessary distance.

## Grounding and via fence

- Maintain grounded coplanar copper on both sides of the RF trace where the SMA launch and board geometry permit.
- Stitch the coplanar ground to Layer 2 with a ground-via fence.
- Target RF-region ground-via pitch: no greater than 1.5 mm where practical.
- Add dense ground stitching at the E22 ANT transition and around the SMA ground tabs/launch.
- The SMA shell/ground tabs connect directly into the RF ground structure and Layer-2 ground plane through short, low-inductance paths.

## SMA connector

- Connector class: standard-polarity 50-ohm SMA female, board-edge/edge-launch style.
- Exact manufacturer part remains dependent on final PCB thickness, launch geometry and enclosure/mechanical arrangement.
- Do not lock an SMA footprint until its manufacturer drawing is checked against the selected board thickness and controlled-impedance launch.

## RF power

- E22-900M33S maximum module output is approximately 33 dBm class.
- A properly designed 50-ohm PCB transmission line and normal SMA connector are not power-limited by this approximately 2 W RF level; the controlling concerns are impedance discontinuity, insertion loss, grounding and EMI.

## ESD protection

No shunt RF ESD/TVS device is locked into Rev A at this stage.

Reason: an antenna-line protection diode must be verified not only for capacitance and ESD rating but also for acceptable insertion loss, nonlinear/harmonic behavior and operation with the E22's approximately 33 dBm RF output. Parts such as Nexperia PESD24VF1BBSF and Semtech RF-oriented low-capacitance TVS families demonstrate that suitable antenna-protection devices exist, but the presently reviewed manufacturer data do not provide enough explicit 915 MHz / 2 W continuous-RF validation to freeze one without assumption.

Therefore Rev A does not insert an unverified TVS into the RF path. This is a deliberate production-design choice rather than an unpopulated test option.

## Schematic exclusions

The following are intentionally absent from Rev A:

- 0-ohm RF series link
- pi tuning/matching footprint
- external module matching components
- series RF DC-block capacitor
- RF test connector
- RF jumper
- unverified antenna-line TVS/ESD diode

## PCB release dependency

Before PCB routing is considered final:

1. Select the production fabricator and 4-layer stack-up.
2. Select the exact SMA connector for that board thickness and mechanical layout.
3. Calculate the 50-ohm GCPW geometry using the production stack-up.
4. Confirm the connector launch geometry against the connector manufacturer's recommended footprint.
5. Apply the RF keepout and via-fence rules above.
