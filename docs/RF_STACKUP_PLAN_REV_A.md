# RoyalNode Rev A RF Stack-Up Plan

## Status

Planning document. This does not release the `RF_915` route.

The current Rev A board target is a JLCPCB four-layer, 1.6 mm, controlled-impedance PCB with Layer 2 as the continuous RF reference plane.

## Current Fabricator Stack-Up Candidate

Primary candidate:

```text
JLC04161H-3313
4 layers
1.6 mm nominal board class
1 oz outer copper
0.5 oz inner copper
3313 prepreg between F.Cu and In1.Cu
```

JLCPCB's official controlled-impedance page lists these relevant parameters for `JLC04161H-3313`:

- Top copper: 0.035 mm
- F.Cu-to-In1.Cu prepreg: 3313, 0.09940 mm
- 3313 prepreg dielectric constant: 4.1
- Inner copper: 0.0152 mm
- Core between inner layers: 1.265 mm
- Solder-mask model: C1 1.2 mil above substrate, C2 0.6 mil above trace, C3 1.2 mil between traces, solder-mask dielectric constant 3.8

Official source:

```text
https://jlcpcb.com/impedance
```

JLCPCB also provides an impedance calculator for trace-width confirmation:

```text
https://jlcpcb.com/pcb-impedance-calculator/
```

## RoyalNode RF Geometry

Target route:

```text
E22 pin 21 ANT
  -> short left-edge 50 ohm grounded coplanar waveguide on F.Cu
  -> Molex 0732511150 edge-launch SMA center contact
```

The current Rev A floorplan rotates the E22 module to 0 degrees at 42.0, 54.0
mm and places the J5 draft SMA envelope at the left board edge near E22 pin 21.
Do not return to the older far-right SMA corridor unless the final SMA footprint
or enclosure forces another RF-floorplan review.

Reference plane:

```text
In1.Cu / Layer 2: uninterrupted GND
```

Do not route `RF_915` until all of these are true:

1. The Molex sales drawing / recommended launch geometry is obtained.
2. The final JLCPCB stack-up is selected in the order options.
3. The JLCPCB impedance calculator is run for a 50 ohm single-ended grounded-coplanar structure on F.Cu over In1.Cu.
4. The resulting trace width and ground-copper gap are recorded in `docs/PCB_NET_CLASSES_REV_A.md`.
5. J5's footprint is replaced with a release footprint that includes the actual edge-launch copper geometry.

## Starting Geometry Notes

Do not treat these as release values.

With the very thin 0.09940 mm F.Cu-to-In1.Cu dielectric on the 3313 stack-up, a 50 ohm top-layer trace is expected to be narrow. The final RoyalNode route should therefore be calculated with JLCPCB's own calculator and reviewed with the SMA launch geometry before copper is drawn.

The RF route should remain:

- as short as practical
- no vias
- no 90-degree bends
- no series 0 ohm link
- no pi tuning footprint in Rev A
- ground via fence near both sides where it does not violate the SMA launch drawing
- no switch-node or high-current copper beneath or beside the RF corridor

## Open Release Items

- Molex `SD-73251-115-001` sales drawing still required.
- Exact grounded-coplanar trace width still required.
- Exact coplanar ground gap still required.
- SMA launch pad geometry still required.
- JLCPCB impedance-order notes still required.
