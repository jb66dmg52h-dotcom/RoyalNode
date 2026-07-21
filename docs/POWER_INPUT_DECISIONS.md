# 2Watt Project Power Input Decisions

## Issue 1: BQ25798 dual-input source mux

**Status: LOCKED**

Use the full BQ25798 dual-source mux topology:

```text
Solar source -> back-to-back ACFET/RBFET pair -> common VBUS
USB source   -> back-to-back ACFET/RBFET pair -> common VBUS
```

Requirements:

- Solar source is assigned to VAC1 control/sense.
- USB source is assigned to VAC2 control/sense.
- Each source receives its own back-to-back N-channel MOSFET pair.
- The BQ25798 controls the source-selection FETs through its source-driver outputs.
- No source may backfeed the other source or its connector.
- Exact MOSFET manufacturer part numbers remain to be selected during the input-stage schematic design.

This supersedes all earlier one-pair or direct-source concepts.

## Issue 2: Solar overvoltage and reverse-polarity protection

**Status: LOCKED**

Use an active input-protection stage based on:

- Controller: Analog Devices LTC4365ITS8-1#TRMPBF
- Package: TSOT-23-8
- Temperature range: -40 C to +85 C
- External protection devices: one back-to-back N-channel MOSFET pair

Locked solar path:

```text
Solar XT30
  -> 2 A fuse
  -> LTC4365-1 protection controller
  -> back-to-back N-channel protection MOSFETs
  -> BQ25798 solar-source ACFET/RBFET mux pair
  -> common BQ25798 VBUS
```

Locked threshold targets:

- Undervoltage cutoff: approximately 7 V
- Overvoltage cutoff: approximately 25 V

Requirements:

- The LTC4365 protection pair handles reverse polarity and disconnects the panel during excessive input voltage.
- The BQ25798 mux pair remains a separate stage for source selection and source-to-source reverse blocking.
- The previously selected SMBJ22A TVS is removed from the locked BOM.
- The previously selected BSL303SPE P-channel reverse-polarity MOSFET is removed from the locked BOM.
- Final UV/OV divider values and the exact external N-channel MOSFET part number must be calculated from the LTC4365 datasheet during schematic capture.
- Recommended panel cold-weather Voc must remain below the 25 V cutoff target with suitable tolerance margin.

## Issue 3: Shared USB-C charging-current policy

**Status: LOCKED**

The XIAO USB-C connector remains shared between firmware/data operation and BQ25798 main-battery charging.

Locked policy:

- Initial BQ25798 USB input-current limit: 100 mA.
- After successful USB enumeration by the XIAO: raise the BQ25798 USB input-current limit to 350 mA.
- Never exceed 350 mA through the shared XIAO USB-C charging branch.
- BQ25798 D+ and D- remain unconnected.
- Solar remains the primary high-power charging source.

Firmware requirement:

- Initialize the BQ25798 USB path at 100 mA.
- Raise to 350 mA only after the USB stack confirms successful enumeration.
- Fall back to 100 mA after disconnect, USB reset or enumeration failure.

## Issue 4: LM66100 exact wiring

**Status: LOCKED**

Use LM66100DCKR as the always-enabled ideal-diode feed from the protected 1S battery/system node to the XIAO underside BAT input.

Locked path:

```text
Protected battery/system node
  -> LM66100 VIN
  -> LM66100 VOUT
  -> 2-pin JST-PH positive
  -> XIAO BAT pad

Common GND
  -> 2-pin JST-PH ground
  -> XIAO GND
```

Pin and support-component requirements:

- VIN: protected battery/system node.
- VOUT: JST positive output to XIAO BAT.
- GND: common system ground.
- CE: tie high to VIN for always-enabled operation.
- ST: leave unconnected.
- Input bypass capacitor: 1 uF ceramic located close to VIN/GND.
- Output bypass capacitor: 1 uF ceramic located close to VOUT/GND.
- No MCU GPIO control is required.

Functional intent:

- XIAO automatically receives battery power whenever the main protected battery is present.
- Reverse current from the XIAO side toward the main battery rail is blocked by the ideal-diode path.
- XIAO remains socketed and USB-C remains available for firmware/data operation.

## Issue 5: BQ25798 BATP Kelvin routing

**Status: NEXT**

The next decision is the exact BATP sense connection, series resistance, routing point and Kelvin-routing rules so the charger measures true battery-terminal voltage rather than voltage drop in the high-current charge path.
