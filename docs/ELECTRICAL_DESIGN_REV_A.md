# 2Watt Project Electrical Design, Rev A Draft

## Design status

This document defines the proposed Rev A electrical architecture and candidate parts. It is suitable for beginning KiCad schematic capture. Battery-specific charge current and several converter passives remain TBD until the exact battery is selected. Battery-temperature monitoring is intentionally omitted. This is not yet an order-ready or safety-certified schematic.

## System block diagram

```text
12 V nominal solar panel
        |
   XT30_SOLAR
        |
 fuse + reverse protection + TVS
        |
 BQ25798 dual-input path A

XIAO USB-C VBUS
        |
 USB protection + current limiting
        |
 BQ25798 dual-input path B

BQ25798 NVDC power path
        |---------------------------> protected 1S LiPo through XT30_BAT
        |
      SYS rail
        |
        +--> always-on control domain: MAX16054, BQ25798, MAX17048
        |
        +--> TPS61088 5.0 V boost
                  |
                  +--> diode-isolated XIAO 5V supply
                  |
                  +--> TPS22990 radio load switch --> E22-900M33S
```

## 1. Solar input stage

### Connector

- J1: board-mounted XT30.
- Use a different gender and board edge from the battery XT30.
- Label `SOLAR INPUT` and polarity clearly.

### Protection chain

Proposed order:

1. replaceable fuse or resettable fuse sized for the allowed panel class
2. reverse-polarity protection using a P-channel MOSFET or back-to-back N-channel arrangement
3. TVS diode selected for the final maximum panel Voc and BQ25798 input limit
4. local ceramic plus bulk input capacitance
5. BQ25798 input-selector FET path

### Panel envelope

Recommended deployment class:

- 12 V nominal monocrystalline panel
- approximately 10-20 W
- Vmp typically in the mid-to-high teens
- cold-weather Voc must remain below the published board input maximum with margin

Proposed board label and manual limit should be set only after the TVS and input FET ratings are finalized.

## 2. USB-C input and firmware path

The XIAO's native USB-C connector remains the firmware/programming connector.

### Charger isolation

- XIAO BAT pad: no connection.
- The project battery is never connected to the XIAO onboard charger output.
- USB D+ and D- remain untouched and route only through the XIAO.
- USB VBUS is taken from the XIAO 5V/VBUS pad and routed to BQ25798 input B through a fuse/current limiter and input-selector path.

### Input-current policy

Rev A default:

- safe startup current limit: 500 mA
- allow firmware to raise the limit only after BQ25798 source detection confirms a suitable USB source

## 3. Main charger and power path

### IC

- U3: BQ25798RQMR.

### Why selected

- supports 1-cell Li-ion/LiPo
- 3.6-24 V operating input
- buck-boost operation for 5 V USB or 12 V-class solar
- NVDC power path
- autonomous solar VOC-based MPPT
- optional dual-input selector
- integrated current sensing, BATFET and ADC

### Proposed configuration

- cell count: 1S
- charge voltage: 4.20 V nominal, subject to battery datasheet
- charge current: TBD from battery rating; initial engineering target 1.0-2.0 A
- minimum system voltage: approximately 3.5 V class, finalized from battery and XIAO behavior
- solar MPPT: autonomous VOC scaling enabled
- USB input current: 500 mA at startup, increased after source detection when allowed
- TS pin: configured using the datasheet-approved fixed bias method because no battery thermistor is fitted
- INT pin: XIAO NFC2/P0.10 through the underside wire harness
- SDA/SCL: XIAO D4/D5, 3.3 V pull-ups

### Required external power parts

- charger inductor sized from the TI design equations and final charge current
- local input, system and battery capacitors following the latest TI EVM layout
- optional dual-input blocking FETs controlled by the BQ25798 selector outputs
- fixed TS-bias components chosen from the datasheet guidance for operation without an NTC
- STAT/INT pull-ups and low-current LEDs

### Safety behavior

- no automatic battery-temperature lockout in Rev A
- firmware logs and reports charger faults
- hardware input OVP/OCP and thermal protections remain enabled
- charging continues when the product load is switched off
- deployment documentation must prohibit charging outside the battery manufacturer's allowed temperature range

## 4. Battery connection and telemetry

### Battery connector

- J2: board-mounted XT30, different gender/orientation from solar.
- Battery must be a protected 1S flat LiPo.
- Pack must support at least 5 A continuous discharge.
- XT30 carries battery positive and negative only.
- No NTC or temperature-sense connector is included.

### Fuel gauge

- U5: MAX17048G+T10.
- VCell connected at the protected battery/system-side battery node.
- SDA/SCL share the 3.3 V I2C bus.
- ALRT optional; if GPIO is unavailable, poll SOC and voltage periodically.
- Place close to the battery node and away from the TPS61088 switch loop.

## 5. Push-button and system latch

### Controller

- U8: MAX16054AZT+T candidate.

### Function

- momentary press toggles a clean latched output
- low quiescent current
- powered from the BQ25798 SYS/control domain
- latched output enables the TPS61088
- complementary output or CLEAR can support firmware-assisted shutdown

### Behavior

- OFF: charger and fuel gauge remain alive; XIAO and radio are off unless USB is plugged in
- ON: TPS61088 starts and powers the XIAO supply plus radio branch
- USB inserted while OFF: XIAO can still boot through native USB for recovery/programming
- long-press hard-off requires an added hold-timer/clear circuit or a different dedicated long-press controller

## 6. 5 V boost rail

### Converter

- U4: TPS61088RHLR.

### Input

- BQ25798 SYS rail, approximately battery-class voltage during battery operation.

### Output

- 5.0 V nominal
- 2 A continuous design target
- 3 A transient class

### Initial design direction

- switching frequency target: approximately 1 MHz
- PFM permitted for idle efficiency unless RF testing reveals interference
- approximately 1 uH shielded low-DCR inductor with saturation rating chosen from worst-case low-battery peak current
- bulk input capacitance close to TPS61088
- output ceramics and low-ESR bulk close to both converter and E22 branch
- EN driven from the push-button latch

Final values must be generated from the latest TPS61088 datasheet or WEBENCH and checked at 3.0, 3.2, 3.7 and 4.2 V input.

## 7. XIAO power path and removable underside harness

### Battery-powered operation

- TPS61088 5 V output feeds the XIAO 5V pin through a Schottky diode or ideal-diode element.
- This prevents the internally generated 5 V rail from backfeeding USB VBUS when a USB cable is attached.
- Add local 10 uF plus 100 nF near the XIAO socket.

### USB-powered operation

- Native USB VBUS powers the XIAO directly.
- USB VBUS also reaches BQ25798 input B through the protected input path.
- Internal 5 V diode isolation prevents source fighting.

### Socketing

- XIAO is socketed on two edge-header rows.
- Bottom pads are not contacted by pogo pins.
- Short flexible wires are soldered directly to the required underside pads on the XIAO.
- The wires terminate in one keyed 8-position JST-PH 2.0 plug.
- The carrier PCB has the matching board-mounted JST-PH receptacle.
- The XIAO and wire harness are removed together as one assembly.

### Harness pinout

1. SWDIO
2. SWCLK
3. 3V3 reference
4. GND
5. NFC1 / P0.09 / power-button sense
6. NFC2 / P0.10 / charger interrupt
7. RESET_N
8. reserved spare

### Harness construction rules

- use thin, flexible stranded wire
- keep the harness short
- route it away from the RF trace and switching nodes
- add strain relief near the underside solder pads
- do not use the 3V3 conductor to power the board
- mark pin 1 clearly on both cable and PCB

## 8. Radio load switch and supply filtering

### Load switch

- U6: TPS22990DMLR candidate.
- VIN/VBIAS: 5 V boost rail.
- EN: XIAO-controlled radio-power signal or tied to system latch for first bring-up.
- CT: selected for controlled ramp to prevent the E22 bulk capacitance from collapsing the rail.
- PG: optional status input if a GPIO remains available.

### E22 decoupling

At the E22 VCC pins:

- multiple 100 nF ceramics
- 1 uF ceramic
- 10-22 uF ceramic
- 220-470 uF low-ESR bulk capacitor footprint

### Radio controls

- TXEN and RXEN default low with pull-down resistors
- NRST pulled high with local RC only if required by driver timing
- BUSY and DIO1 route away from RF and switching nodes
- DIO3 remains internal to the E22 TCXO function

## 9. RF path

- E22 ANT pad to SMA using a short 50-ohm coplanar waveguide or microstrip.
- Use a solid ground plane directly below.
- Add ground-via fencing.
- Include a 0-ohm series link and optional unpopulated pi network for tuning.
- No power or digital traces cross the RF keepout.
- Place TPS61088 and its inductor at the opposite end of the PCB from the SMA/E22 antenna edge.

## 10. LEDs

- CHARGE LED driven by BQ25798 status logic; target 0.5-1 mA.
- FAULT/FULL LED behavior defined by charger outputs or firmware.
- SYSTEM indication uses the XIAO onboard RGB LED where practical.
- Provide solder jumpers to disable external LEDs for lowest overnight consumption.

## 11. Grounding and PCB stack-up

Recommended 4-layer stack:

1. top: components, RF and critical power loops
2. inner 1: uninterrupted ground plane
3. inner 2: power distribution and low-speed signals
4. bottom: low-speed routing and secondary ground copper

Rules:

- do not route beneath the E22 RF section unless allowed by its keepout
- keep BQ25798 and TPS61088 hot loops compact
- separate switch-node copper from I2C, harness signals and RF
- join all grounds through a continuous plane; do not use split-ground islands
- use dense thermal and current-sharing vias under QFN thermal pads and high-current pours

## 12. Bring-up power states

| State | Solar | USB | Battery | XIAO | Radio | Charging |
|---|---|---|---|---|---|---|
| Stored/off | optional | no | yes | off | off | yes if solar available |
| USB recovery | no | yes | optional | on | off by default | yes if battery installed |
| Solar operation | yes | no | yes | on | firmware controlled | yes |
| Battery operation | no | no | yes | on | firmware controlled | no |
| No battery bench | USB or solar | optional | no | permitted after validation | radio limited until SYS stability verified | no |

## 13. Firmware initialization order

1. configure NFC pads as GPIO where used
2. initialize I2C
3. read BQ25798 status and program conservative 1S limits
4. initialize MAX17048
5. hold TXEN/RXEN low
6. enable radio load switch
7. initialize SX126x with correct TCXO and RF-switch behavior
8. begin telemetry and watchdog tasks

## 14. Remaining schematic values marked TBD

- exact protected battery capacity and permitted charge current
- exact fixed TS-bias network for BQ25798 without an NTC
- exact BQ25798 inductor and capacitor values
- exact dual-input FETs
- exact solar TVS and fuse rating
- exact TPS61088 inductor, frequency, current limit and soft-start values
- radio load-switch rise-time capacitor
- long-press/hard-off implementation
- exact 8-pin JST-PH part number, harness wire gauge and strain relief

## Electrical design verdict

The revised architecture matches the stated requirements: no battery-temperature monitoring, no pogo contacts, and a socketed XIAO with a removable underside wire harness. The electrical design remains feasible. The main tradeoff is that Rev A now depends on deployment guidance rather than automatic cold-charge protection, and the underside harness becomes a hand-assembled service component that must be strain-relieved carefully.
