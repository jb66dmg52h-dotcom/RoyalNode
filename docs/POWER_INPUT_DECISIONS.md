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

**Status: LOCKED**

Locked connection:

```text
Battery XT30 positive pad
  -> dedicated Kelvin sense trace
  -> 100 ohm series resistor
  -> BQ25798 BATP
```

Routing and component requirements:

- BATP sense origin is the battery XT30 positive pad itself.
- Do not sense BATP from the BQ25798 BAT power pin, from the charger-side BAT copper, or from an intermediate high-current node.
- Use a dedicated low-current sense trace from the battery connector pad to BATP.
- The BATP sense trace must not carry battery charge or system current.
- Route the BATP trace away from SW1, SW2 and other noisy switching nodes.
- Place the 100 ohm series resistor close to the BQ25798 BATP pin.
- Do not add a BATP capacitor unless explicitly required by TI guidance used during final schematic verification.
- Keep BATP sensing tied to the actual battery-positive terminal side of any future switching element.

Functional intent:

- The charger measures actual battery-terminal voltage rather than voltage elevated by IR drop in the high-current charge path.
- The Kelvin connection protects charge-voltage accuracy, especially at the 2 A charge target.

## Issue 6: External MOSFET selection and LTC4365 threshold divider

**Status: LOCKED**

### Common MOSFET device

Use one common dual N-channel 40 V MOSFET device for all three back-to-back pairs:

- Manufacturer: Infineon
- Device: ISA170170N04LMDS
- Ordering code: ISA170170N04LMDSXTMA1
- Configuration: dual N-channel
- VDS rating: 40 V
- Package: SO-8 / PG-DSO-8
- Logic-level device
- RDS(on) max at VGS = 4.5 V: 23.6 milliohm per MOSFET
- QG typ at 4.5 V: 6 nC

Use one dual-MOSFET package for each function:

1. One ISA170170N04LMDS package for the LTC4365 solar protection pair.
2. One ISA170170N04LMDS package for the BQ25798 solar ACFET/RBFET pair.
3. One ISA170170N04LMDS package for the BQ25798 USB ACFET/RBFET pair.

### LTC4365 UV/OV divider

```text
VIN
 |
 R3 = 1.87 MOhm
 |
 UV
 |
 R2 = 104 kOhm
 |
 OV
 |
 R1 = 40.2 kOhm
 |
GND
```

Nominal thresholds:

- UV falling cutoff: approximately 6.98 V
- UV rising/reconnect: approximately 7.33 V
- OV rising cutoff: approximately 25.05 V
- OV falling/reconnect: approximately 23.80 V

## Issue 7: BQ25798 TS policy for Rev A

**Status: LOCKED**

Rev A will not use a physical battery thermistor. The TS input will use a fixed simulated in-range condition rather than real battery-temperature sensing.

Design intent:

- Keep the BQ25798 TS input permanently in its normal-temperature operating region for Rev A.
- Do not fit an external battery NTC connector on Rev A.
- Treat this as a Rev A simplification only; a real temperature-sensing option may be reconsidered in a later hardware revision.
- Exact TS network implementation is to follow the BQ25798 datasheet/reference design during schematic capture.

## Issue 8: BQ25798 remaining static/configuration pins

**Status: NEXT**

Next, close out the remaining charger static/configuration details:

- Confirm PROG = 4.7 kOhm for 1S / 750 kHz.
- Lock STAT charge-LED wiring and resistor value.
- Confirm treatment of unused D+/D- pins.
- Confirm any required pullups, pulldowns, bypass capacitors, or no-connect rules on the remaining configuration/static pins.
- Perform a final BQ25798 pin-by-pin schematic-readiness check before KiCad capture.
