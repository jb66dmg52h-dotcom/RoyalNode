# 2Watt Project Full-Board Compatibility Audit, Rev 3

## Executive verdict

The core radio, charger, fuel-gauge and 5 V boost components are mutually compatible, but the current XIAO power arrangement has one critical conflict that must be corrected before KiCad schematic capture.

### Critical conflict

Do **not** power the XIAO from the TPS61088 5 V rail through the XIAO 5V/VBUS pad while also using the XIAO USB-C connector.

The XIAO 5V pin is the same VBUS node as the USB connector. Feeding the generated 5 V rail into that node can energize the USB connector and create source-fighting/backfeed conditions when USB is inserted.

### Corrected XIAO power architecture

Power the XIAO from the protected 1S battery/system node through its BAT input, using a blocking/ideal-diode element so the XIAO's onboard 50/100 mA charger cannot feed back into the main battery.

Recommended path:

```text
Protected 1S battery/system node
        |
 low-current ideal diode or Schottky
        |
 2-pin JST-PH lead
        |
 XIAO BAT + GND
```

This preserves native USB firmware updates, avoids energizing the USB VBUS connector from the board's 5 V boost rail, and keeps the XIAO onboard charger isolated from the main battery.

## Component-by-component audit

### EBYTE E22-900M33S

Status: compatible.

- Supply range: 2.5-5.5 V.
- Use 5.0 V for full-power operation.
- Logic interface is compatible with 3.3 V XIAO GPIO.
- Required signals: NSS, SCK, MOSI, MISO, BUSY, DIO1, NRST, TXEN and RXEN.
- DIO3 is internally used for the TCXO and must be configured correctly in firmware.
- Direct 50-ohm RF path to board-edge SMA is appropriate.

Direct connection to the TPS61088 5 V output is acceptable if the converter soft-start, current limit and local bulk capacitance are correctly implemented. A separate load switch is not mandatory for Rev A.

### TPS61088

Status: compatible.

- Input range supports a 1S LiPo.
- 5 V output is within the specified range.
- Calculated 2 A continuous and 3 A transient target is within the device's capability with proper inductor, current-limit and thermal design.
- Built-in cycle-by-cycle current limiting and thermal shutdown remain available.

Required implementation details:

- 2.2 uH shielded inductor, 10 A minimum saturation target.
- Large ceramic input/output banks with DC-bias derating checked.
- 330-470 uF low-ESR bulk near the E22.
- EN tied for automatic startup through a defined pull-up/control network.
- MODE option retained as a resistor/jumper footprint so RF testing can compare PFM and forced-PWM operation.

### BQ25798

Status: compatible, configuration-sensitive.

- Supports 1S Li-ion/LiPo.
- Accepts 5 V USB and 12 V-class solar input.
- Supports buck-boost charging, MPPT and power-path operation.
- 2 A charge current is suitable for the 10 Ah design target, subject to the final battery's allowed charge current.

Mandatory details:

- PROG/cell-count configuration must select 1S.
- /CE must be held low for autonomous charging.
- TS cannot simply be ignored accidentally. Since no thermistor is used, either set TS to the normal region with a fixed divider or disable TS in firmware; hardware-safe bias is preferred for Rev A startup.
- REGN, PMID and SYS minimum effective capacitances must meet the datasheet after DC-bias derating.
- Battery-present and battery-absent behavior must be tested.
- Charger defaults must be safe before XIAO firmware initializes I2C.

### MAX17048

Status: compatible.

- Correct device for a single Li-ion cell.
- Battery voltage range matches a 1S pack.
- I2C interface is compatible with 3.3 V pull-ups.
- Shares the D4/D5 I2C bus with BQ25798 without an address conflict.
- Can be polled; no alert GPIO is required.

Place close to the battery node and away from high-current switch loops.

### XIAO nRF52840

Status: compatible after power-path correction.

GPIO allocation remains valid:

- D0 NRST
- D1 DIO1
- D2 BUSY
- D3 NSS
- D4 SDA
- D5 SCL
- D6 TXEN
- D7 RXEN
- D8 SCK
- D9 MISO
- D10 MOSI

All 11 exposed GPIOs are consumed. Therefore:

- Charger telemetry is read by I2C polling.
- Charge LED is hardware-driven.
- No carrier reset button, SWD connector, solar-present telemetry or USB-present telemetry.
- No power button.

Corrected two-wire XIAO lead:

1. XIAO BAT positive, through a blocking diode/ideal-diode path from the protected battery/system node.
2. Ground.

Do not feed the XIAO 5V/VBUS pad from the TPS61088 rail.

### USB-C path

Status: compatible after XIAO power-path correction.

- USB D+/D- remain entirely on the XIAO for firmware updates.
- USB VBUS can be tapped from the XIAO 5V/VBUS node and routed to BQ25798 input B.
- Generated board power must never be injected into the XIAO VBUS node.
- Add input current limiting/protection between XIAO VBUS and BQ25798.

### Solar input

Status: compatible.

- Board-mounted keyed XT30.
- Fuse/PTC and TVS remain recommended.
- Reverse-polarity protection on solar input remains recommended because panel cables may be field-wired.
- Recommended panel class remains 12 V nominal, 10-20 W.
- Published board maximum must be based on the final TVS, FET and BQ25798 limits.

### Battery input

Status: compatible.

- Board-mounted keyed XT30.
- No reverse-polarity circuit by project decision.
- Battery must be a protected 1S pack.
- Target: 10 Ah, at least 5 A continuous discharge, at least 2 A allowed charge current.
- No temperature monitoring.

### Charge LED

Status: compatible.

- One external charge LED only.
- Drive from BQ25798 status output/open-drain logic with a low-current resistor network.
- No full, fault or external system LED.

### Direct E22-to-5 V connection

Status: acceptable with conditions.

Removing the load switch and eFuse is acceptable for Rev A if:

- TPS61088 soft-start is set conservatively.
- E22 local bulk capacitance is fitted.
- TXEN and RXEN have pull-downs so the RF path is closed during MCU reset.
- TPS61088 current limit is set above normal startup/transmit peak but below damaging fault levels.
- Bench testing confirms no XIAO reset or 5 V collapse during radio startup and repeated transmit bursts.

## Conflicts removed from scope

- power button
- eFuse
- radio load switch
- battery temperature monitoring
- SWD connector
- pogo pins
- 8-wire XIAO harness
- solar-present telemetry
- USB-present telemetry
- full/fault LEDs
- radio-disable jumper
- battery reverse-polarity circuit

## Remaining compatibility blockers before KiCad

1. Replace the XIAO 5 V supply concept with the BAT-input plus blocking-diode arrangement.
2. Choose the exact blocking diode or ideal-diode part for the XIAO BAT lead.
3. Choose the fixed TS-bias divider for BQ25798 no-thermistor operation.
4. Confirm BQ25798 default 1S startup settings and PROG resistor.
5. Choose final solar TVS, fuse/PTC and reverse-polarity FETs.
6. Confirm exact inductor and capacitor manufacturer part numbers, including effective-capacitance checks.
7. Confirm automatic TPS61088 enable wiring and soft-start value.
8. Perform one final schematic-level ERC audit after capture.

## Final verdict

The board is feasible and the major components are compatible. The only critical architectural issue found is the XIAO 5V/VBUS backfeed risk. Powering the XIAO through its BAT input via a one-way low-current path resolves that conflict cleanly while preserving USB-C firmware updates and keeping the onboard XIAO charger isolated from the main 10 Ah battery.
