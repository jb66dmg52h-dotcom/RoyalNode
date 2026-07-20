# 2Watt Project Trace and Path Compatibility Audit, Rev 5

## Verdict

The radio, battery, XIAO power isolation, fuel gauge and 5 V boost paths are fundamentally compatible. The design is **not yet ready for schematic freeze** because two upstream power-path details are incomplete or mismatched:

1. The solar and USB sources need a fully defined BQ25798 dual-input mux implementation with external ACFET/RBFET devices.
2. The selected SMBJ22A TVS does not clamp below the BQ25798 30 V absolute maximum and therefore is not adequate protection for the charger input.

A third limitation must be locked into the design: the shared XIAO USB-C connector should be treated as a low-current charging input, not a 1.5 A charger input, because the USB data lines remain dedicated to the XIAO and the BQ25798 cannot perform BC1.2 detection.

## Path 1: Solar connector to charger

```text
12 V nominal panel
-> XT30PW
-> 2 A fuse
-> reverse-polarity P-FET
-> surge clamp
-> BQ25798 input mux
-> BQ25798 VBUS
```

### XT30PW to fuse

Compatible.

- A 10 W panel near 17 V Vmp supplies about 0.6 A.
- A 20 W panel supplies about 1.2 A.
- The 2 A fuse has appropriate operating margin for both.

### Fuse to BSL303SPE P-FET

Compatible for the expected panel current.

- The MOSFET's -30 V drain-source rating is above the normal voltage of a 12 V-class panel.
- The final panel recommendation must keep cold-weather Voc comfortably below 30 V.
- The P-FET orientation must be checked carefully so its body diode allows correct startup while blocking reverse polarity.

### BSL303SPE to SMBJ22A

Not accepted as currently selected.

- SMBJ22A has 22 V reverse standoff.
- Its breakdown and clamp voltage can rise above the BQ25798's 30 V absolute maximum.
- It may therefore fail to protect the charger during the very event it is intended to clamp.

Decision: remove SMBJ22A from the locked BOM. Select a protection scheme only after the maximum allowed panel Voc and surge target are defined. A precision surge-stopper or lower-clamp architecture may be required if true transient protection below 30 V is desired while still supporting common 12 V panels with cold Voc above 20 V.

### Solar source to BQ25798

Incomplete.

The BQ25798 has one VBUS power input and optional VAC1/VAC2-controlled external input paths. Two independent sources cannot simply be routed as two ordinary charger input pins. A real dual-source design needs either:

- two external ACFET/RBFET pairs following the BQ25798 dual-input application, or
- one direct VBUS source plus one ACFET/RBFET-controlled source following the one-pair application.

Decision: use the official two-source mux topology unless a later schematic review proves the one-pair topology provides the desired autonomous behavior. Exact back-to-back N-channel MOSFETs remain to be selected.

## Path 2: XIAO USB-C to BQ25798

```text
USB-C connector on XIAO
-> XIAO VBUS node
-> protected branch from exposed VBUS pad
-> BQ25798 input mux
-> charger VBUS
```

Electrically possible, but current-limited.

- USB D+ and D- remain connected to the nRF52840 for firmware and serial data.
- BQ25798 D+ and D- must remain unconnected, so the charger cannot perform BC1.2 source detection.
- The XIAO onboard BQ25101 charger may also draw current from USB when the BAT node is below its charge target.

Decision:

- Treat the shared USB-C connector as a default USB device power source.
- Set the BQ25798 USB input-current limit conservatively to 350 mA during USB operation.
- Do not advertise or assume 1.5 A or 3 A charging from this connector.
- Solar remains the primary high-power charging path.

This keeps total USB current closer to the ordinary 500 mA device envelope after allowing for the XIAO itself and its onboard charger.

## Path 3: Charger to protected 1S battery

```text
BQ25798 BAT pins
<-> battery copper and vias
<-> board-mounted XT30PW
<-> protected 1S 10 Ah LiPo
```

Compatible with conditions.

- BQ25798 supports 1S Li-ion/LiPo charging.
- PROG = 4.7 kOhm correctly selects 1S at 750 kHz.
- A 2 A charge target equals 0.2 C for a 10 Ah pack.
- The selected battery must explicitly allow at least 2 A charge current and at least 5 A continuous discharge.
- Battery traces, connector pads and vias must be sized for at least 5 A continuous and approximately 6 A transient.
- BATP remote sense must connect to the battery-positive node using a Kelvin-style low-current sense route rather than sharing the high-current copper drop.

Accepted limitation: no battery-temperature sensing. TS is biased into the normal range with a fixed divider, so deployment documentation must prohibit charging outside the pack manufacturer's allowed temperature range.

## Path 4: Battery/system node to XIAO

```text
protected battery/system node
-> LM66100DCKR
-> board-mounted 2-pin JST-PH
-> two-wire harness
-> XIAO BAT and GND underside pads
```

Compatible.

- The LM66100 input range of 1.5-5.5 V covers the full 1S battery range.
- Its 1.5 A rating is far above XIAO demand.
- Reverse-current blocking prevents the XIAO onboard charger from feeding the main battery rail.
- The XIAO BAT input is intended for a single lithium-cell voltage range.

Implementation requirements:

- LM66100 CE must be tied to the correct active state.
- ST output may remain unused according to datasheet guidance.
- Place input/output bypass capacitance close to the IC.
- Keep the JST polarity unmistakable.
- The carrier must never drive the XIAO 5V/VBUS pin.

USB-present behavior:

When USB is connected, the XIAO charger may raise the local BAT node. LM66100 then reverse-blocks toward the main battery. This is the intended behavior.

## Path 5: BQ25798 SYS to TPS61088

```text
BQ25798 SYS
-> wide copper and bulk capacitance
-> TPS61088 VIN
```

Compatible.

- TPS61088 accepts 2.7-12 V.
- BQ25798 SYS for a 1S battery is inside this range.
- The converter remains operational through the intended 1S discharge range.

Trace requirements:

- Treat this as a high-current path.
- Use a broad pour on outer copper with multiple stitching vias if layer transitions are unavoidable.
- Keep the BQ25798 SYS capacitors close to the charger and TPS61088 input capacitors close to the boost converter.
- Avoid sending pulsed boost current through the MAX17048 sense area or XIAO ground return.

## Path 6: TPS61088 power stage

```text
SYS
-> input capacitor bank
-> XAL7030-222MEC
-> TPS61088 switch stage
-> output capacitor bank
-> 5 V rail
```

Compatible with the selected targets.

- TPS61088 supports single-cell lithium inputs and 5 V output.
- The 2.2 uH XAL7030-222MEC has comfortable saturation and RMS-current margin.
- 178 kOhm / 56 kOhm is suitable for approximately 5 V output.
- 140 kOhm RILIM gives an approximately 8.5 A typical peak limit, with minimum limit expected roughly 1.3 A lower.
- The previously calculated worst-case transient peak is below this minimum margin.

Correction:

The frequency-setting resistor is connected between FSW and SW, not between FSW and ground. This must be represented correctly in KiCad.

Trace requirements:

- Minimize the VIN-capacitor-inductor-switch-ground hot loop.
- Keep SW copper compact and isolated from RF, I2C and fuel-gauge routing.
- Use the exposed thermal pad and dense ground/thermal vias exactly as the package layout requires.
- Retain optional RC snubber pads at SW for EMI tuning.

## Path 7: TPS61088 5 V rail to E22

```text
TPS61088 output
-> wide 5 V pour
-> local ceramics and 330-470 uF bulk
-> both E22 VCC pins
```

Compatible with conditions.

- E22 accepts 3.3-5.5 V and needs approximately 5 V for rated output.
- The direct connection is valid without a load switch or eFuse.
- The boost converter's soft start reduces startup shock.
- Local bulk capacitance supports transmit-current steps.

Accepted limitation:

TPS61088 does not provide true output disconnect or complete short-circuit isolation. A hard 5 V short can remain a serious fault. Rev A accepts this risk and relies on the protected battery, converter current limiting, layout fusing behavior and prototype testing.

Trace requirements:

- Route 5 V and return as a low-impedance pair.
- Connect both E22 VCC pins.
- Place 100 nF, 1 uF, 22 uF ceramics and the bulk capacitor immediately beside the E22 supply pins.
- Keep E22 return current away from the XIAO and MAX17048 ground routes.

## Path 8: XIAO logic to E22

```text
XIAO 3.3 V GPIO
-> short digital traces
-> E22 SPI and control pins
```

Compatible.

- Both use 3.3 V logic.
- Pin budget fits exactly.
- TXEN and RXEN require pull-down resistors so the RF path stays closed while XIAO resets or is absent.
- NSS should receive a defined inactive pull-up if the radio datasheet/driver requires it during reset.
- BUSY and DIO1 remain direct 3.3 V inputs to the XIAO.

Routing order:

1. SCK and MOSI/MISO as short grouped traces.
2. NSS, BUSY, DIO1 and NRST.
3. TXEN/RXEN away from RF output and switch-node copper.

No level shifters are required.

## Path 9: E22 ANT to SMA

```text
E22 ANT pad
-> optional pi footprint / 0-ohm link
-> 50-ohm controlled-impedance launch
-> board-edge SMA
```

Compatible in principle, stack-up dependent.

- E22 antenna interface is 50 ohms.
- Board-edge SMA is appropriate.
- Final trace width cannot be locked until the board house supplies the actual four-layer dielectric stack.

Layout requirements:

- Place the E22 ANT pad and SMA on the same board edge when possible.
- Keep the path extremely short.
- Use an uninterrupted ground plane directly below.
- Add ground vias along the launch and around SMA ground tabs.
- No vias in the RF signal path unless unavoidable.
- Keep the TPS61088 SW node and inductors at the opposite side of the board.

## Path 10: Battery node to MAX17048

```text
protected battery positive
-> quiet Kelvin sense trace
-> MAX17048 CELL/VDD
-> local bypass
-> ground
```

Compatible.

- MAX17048 is designed for one lithium cell and supports the required voltage range.
- It draws very little current and requires no current-sense resistor.
- It may be placed on the system side of the pack.

Trace requirements:

- Do not connect its sense pin at the noisy TPS61088 input capacitor node.
- Branch from the battery-positive node before the high-current boost path.
- Use a quiet local ground connection.
- Keep it physically away from both switching inductors.

## Path 11: I2C bus

```text
XIAO D4/D5
-> 3.3 V pull-ups
-> BQ25798 SDA/SCL
-> MAX17048 SDA/SCL
```

Compatible.

- BQ25798 and MAX17048 use different addresses.
- Both support a 3.3 V I2C bus.
- Pull-ups must connect to the XIAO 3.3 V rail, not REGN or battery voltage.

Power-state requirement:

When XIAO is unpowered, its 3.3 V pull-up rail is off. This prevents the always-powered charger or gauge from feeding the XIAO through SDA/SCL. Avoid any separate always-on pull-up rail.

## Path 12: BQ25798 STAT to charge LED

```text
approved pull-up rail
-> LED resistor
-> LED
-> BQ25798 STAT open-drain output
```

Compatible.

- STAT is open drain.
- LOW indicates charging.
- The LED current target of 0.5-1 mA is appropriate.
- Choose a pull-up rail that exists while charging and stays inside STAT pin limits.
- REGN is a natural candidate when the charger is active.

No XIAO GPIO is required.

## Final compatibility result

### Accepted paths

- Battery to BQ25798
- Battery/system to LM66100 to XIAO BAT
- BQ25798 SYS to TPS61088
- TPS61088 to E22
- XIAO GPIO to E22
- Battery to MAX17048
- Shared I2C bus
- E22 ANT to SMA, pending stack-up
- STAT to charge LED

### Blockers before a final schematic can be called complete

1. Define the BQ25798 dual-input mux and select the external back-to-back MOSFETs.
2. Replace the SMBJ22A protection choice with a scheme that genuinely protects a 30 V-absolute-maximum charger while supporting the selected panel Voc envelope.
3. Lock shared USB-C main-charge current to approximately 350 mA unless the USB architecture is changed.
4. Capture and verify the exact LM66100 CE/ST connections.
5. Add explicit BATP Kelvin sense routing requirements.

## Release status

Proceed with KiCad **architecture and schematic drafting**, but do not declare the power-input sheet complete or begin final PCB routing until the dual-input mux and solar surge-protection blockers are resolved.
