# RoyalNode Rev A PCB Net Classes

## Status

This file defines the KiCad net-class policy for the Rev A PCB scaffold. It is a routing constraint document, not a fabrication release.

The active KiCad settings live in:

```text
hardware/kicad/RoyalNode/RoyalNode.kicad_pro
```

The PCB still needs RF, power and assembly review before routing is accepted.

## Classes

| KiCad class | Default width | Clearance | Intended nets |
|---|---:|---:|---|
| `Default` | 0.20 mm | 0.15 mm | MCU logic, SPI, I2C, low-current control |
| `HighCurrentPower` | 1.50 mm | 0.15 mm | battery, solar, charger power, radio 5 V |
| `RF_50OHM` | 0.50 mm placeholder | 0.25 mm | `RF_915` only |
| `SwitchNode` | 0.80 mm | 0.15 mm | BQ25798 and TPS61088 switching nodes |
| `SensitiveSense` | 0.20 mm | 0.15 mm | charger sense, thermistor, feedback and UV/OV divider nodes |

## Current Assignments

```text
BAT*        -> HighCurrentPower
SOLAR*      -> HighCurrentPower
BQ_VBUS     -> HighCurrentPower
BQ_SYS      -> HighCurrentPower
BQ_PMID     -> HighCurrentPower
5V_RADIO    -> HighCurrentPower
RF_915      -> RF_50OHM
BQ_SW*      -> SwitchNode
BOOST_SW    -> SwitchNode
BATP_KELVIN -> SensitiveSense
BQ_TS       -> SensitiveSense
BOOST_FB    -> SensitiveSense
BOOST_COMP* -> SensitiveSense
UV_NODE     -> SensitiveSense
OV_NODE     -> SensitiveSense
```

## RF Placeholder

`RF_50OHM` uses a 0.50 mm placeholder trace width so the net is visually distinct during placement and ratsnest review.

Do not treat this as the final 50-ohm geometry. The final E22-to-SMA GCPW dimensions must be calculated from the selected JLCPCB stack-up, currently targeted as `JLC04161H-3313`, and the final Molex SMA launch drawing.

## Routing Intent

`HighCurrentPower` nets should generally become pours or very short, wide copper rather than long 1.50 mm tracks. The width setting is a minimum/preset for early routing, not permission to neck high-current paths unnecessarily.

The non-RF clearance values remain at 0.15 mm because BQ25798, TPS61088 and LTC4365 package pad pitches cannot support a larger class clearance without false DRC errors at the component pads. Extra spacing around high-current and switching routes must be achieved through placement, pours, keepouts and manual routing discipline rather than a blanket net-class clearance.

`SwitchNode` copper should be compact, especially `BQ_SW1`, `BQ_SW2` and `BOOST_SW`. The class keeps these nets visually obvious and gives them more clearance, but layout still matters more than the class width.

`SensitiveSense` nets should avoid switching nodes, inductors and the RF corridor. `BATP_KELVIN`, `BOOST_FB`, `UV_NODE` and `OV_NODE` should route as quiet sense traces with no load current.

## Exclusions

Do not add test points, current shunts, probe loops or bench-only measurement links to satisfy routing/debug convenience.
