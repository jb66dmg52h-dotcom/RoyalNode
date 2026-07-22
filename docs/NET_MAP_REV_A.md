# RoyalNode Rev A KiCad Net Map

## Status

This is the authoritative net-by-net capture map for the Rev A schematic. Use `docs/PIN_AUDIT_REV_A.md` for manufacturer pin numbering and this file for connectivity. Earlier concept wiring is superseded where it conflicts.

Net names below are recommended KiCad global/local labels.

---

## 1. Ground and logic rails

### `GND`
Connect:

- Battery XT30 negative
- Solar XT30 negative
- XIAO power JST pin 2
- XIAO exposed GND header pin(s)
- BQ25798 pin 27 GND
- all BQ25798 local bypass capacitor returns
- LTC4365 pin 4 GND
- TPS61088 pin 20 AGND
- TPS61088 exposed pad 21 PGND
- TPS61088 package pins 11/12 to ground plane per TI thermal recommendation
- LM66100 pin 2 GND
- LM66100 pin 5 ST
- E22 pins 1-5, 11, 12, 20, 22
- NTC connector ground pin
- SMA shell/ground tabs
- all local decoupling/bulk returns

Use one continuous Layer-2 ground plane. Do not split RF ground from power ground.

### `3V3`
Source: XIAO 3V3 output header pin.

Loads:

- BQ25798 SDA pull-up, 10 kOhm
- BQ25798 SCL pull-up, 10 kOhm
- BQ25798 INT pull-up, 10 kOhm
- charge LED anode path

Do not use `3V3` for the E22 power pins.

---

## 2. Battery and XIAO power

### `BAT_RAW`
Connect:

- Battery XT30 positive
- BQ25798 pins 22/23 BAT
- BQ25798 BAT capacitors, 2 x 10 uF to GND
- BQ25798 BATP Kelvin branch origin
- LM66100 pin 1 VIN

The battery pack must be internally protected.

### `BATP_KELVIN`
Connect:

- `BAT_RAW` -> 100 Ohm series resistor -> BQ25798 pin 18 BATP

No load current is routed through this trace.

### `XIAO_BAT_ISO`
Connect:

- LM66100 pin 6 VOUT
- LM66100 pin 3 CE
- LM66100 output 1 uF capacitor to GND
- XIAO power JST pin 1
- short harness -> XIAO underside battery-positive pad (`BAT0` / VBAT)

LM66100 pin 5 ST is tied to GND, not left open.

### `XIAO_BAT_NEG`
Physical harness connection from XIAO power JST pin 2 to the XIAO dedicated underside battery-negative pad (`GND0`). On the carrier this is the `GND` net.

The XIAO underside battery pads are harness-only connections and are not represented as pads in the carrier's socket footprint. Seeed's official current nRF52840 schematic labels the battery pad nets `BAT0` and `GND0`, and Seeed publishes separate Bottom Pad Data for their physical positions.

---

## 3. Solar protection

### `SOLAR_RAW`
Connect:

- Solar XT30 positive
- input side of Littelfuse 0483002.DR 2 A fuse

### `SOLAR_FUSED`
Connect:

- output side of 2 A fuse
- LTC4365 pin 1 VIN
- LTC4365 SHDN pull-up branch: 100 kOhm to pin 5 SHDN
- top of LTC4365 UV/OV divider
- input-side drain of LTC4365 protection MOSFET pair

### LTC4365 UV/OV divider
Use the series chain:

```text
SOLAR_FUSED
   |
 R3 1.87 MOhm
   |
  UV_NODE --------> LTC4365 pin 2 UV
   |
 R2 104 kOhm
   |
  OV_NODE --------> LTC4365 pin 3 OV
   |
 R1 40.2 kOhm
   |
  GND
```

This ordering follows the LTC4365 divider equations: UV senses `(R1+R2)` over the full chain while OV senses `R1` over the full chain.

### `SOLAR_PROT_GATE`
Connect:

- LTC4365 pin 8 GATE
- Gate1 + Gate2 of the solar-protection ISA170170N04LMDS dual MOSFET

### `SOLAR_PROTECTED`
Connect:

- output-side drain of LTC4365 protection MOSFET pair
- LTC4365 pin 7 VOUT sense
- BQ25798 pin 9 VAC1
- input-side drain of the BQ25798 port-1 selector MOSFET pair

Solar is BQ port 1 and is the preferred source.

LTC4365 pin 6 FAULT is NC in Rev A.

---

## 4. USB input path

### `USB_VBUS_RAW`
Source: XIAO exposed `5V/VBUS` header pin, which is fed from the XIAO USB-C VBUS when USB is attached.

Connect:

- BQ25798 pin 8 VAC2
- input-side drain of BQ25798 port-2 selector MOSFET pair

The carrier may draw from this pin for charging but must never drive voltage back into it.

### `BQ_ACDRV1`
Connect:

- BQ25798 pin 11 ACDRV1
- Gate1 + Gate2 of solar BQ selector dual MOSFET

### `BQ_ACDRV2`
Connect:

- BQ25798 pin 10 ACDRV2
- Gate1 + Gate2 of USB BQ selector dual MOSFET

### `BQ_VBUS`
Connect:

- output-side drains of both BQ input selector MOSFET pairs
- BQ25798 pins 2/3 VBUS
- 2 x 10 uF + 100 nF to GND

The solar and USB paths only join here, after their individual back-to-back selector pair.

---

## 5. BQ25798 charger power stage

### `BQ_PMID`
Connect:

- BQ25798 pin 29 PMID
- 3 x 10 uF + 100 nF to GND

### `BQ_SW1`
Connect:

- BQ25798 pin 28 SW1
- one end of Coilcraft XAL7070-222MEC
- low side of BTST1 capacitor

### `BQ_SW2`
Connect:

- BQ25798 pin 26 SW2
- other end of Coilcraft XAL7070-222MEC
- low side of BTST2 capacitor

### `BQ_BTST1`
Connect:

- BQ25798 pin 4 BTST1
- 47 nF capacitor to `BQ_SW1`

### `BQ_BTST2`
Connect:

- BQ25798 pin 19 BTST2
- 47 nF capacitor to `BQ_SW2`

### `BQ_SYS`
Connect:

- BQ25798 pin 25 SYS
- 5 x 10 uF + 100 nF to GND
- TPS61088 pin 9 VIN
- boost inductor input

This is the system/power-path rail feeding the radio boost stage.

### `BQ_REGN`
Connect:

- BQ25798 pin 5 REGN
- 4.7 uF to GND
- BQ25798 pin 17 ILIM_HIZ
- top of 5.23 kOhm TS resistor

### `BQ_SDRV`
Connect:

- BQ25798 pin 24 SDRV
- 1 nF C0G to GND

No external ship FET is used.

### `BQ_PROG`
Connect:

- BQ25798 pin 20 PROG
- 4.70 kOhm to GND

### `BQ_CE`
Connect:

- BQ25798 pin 13 CE
- GND

### `BQ_QON`
BQ25798 pin 12 QON: NC. Keep free of copper except its land; rely on internal pull-up.

### `BQ_DPLUS` / `BQ_DMINUS`
BQ25798 pins 6/7: NC.

---

## 6. Battery temperature sense

### `NTC_SENSE`
Connect:

- NTC connector pin 1
- battery-mounted Semitec 103AT-2 terminal 1
- bottom of 30.1 kOhm resistor

NTC connector pin 2 / other thermistor terminal -> GND.

### `BQ_TS`
Connect:

```text
BQ_REGN -> 5.23 kOhm -> BQ_TS -> 30.1 kOhm -> NTC_SENSE -> 103AT-2 -> GND
```

- BQ25798 pin 16 TS is `BQ_TS`.

---

## 7. I2C and charger status

### `I2C_SDA`
Connect:

- XIAO D4
- BQ25798 pin 15 SDA
- 10 kOhm pull-up to 3V3

### `I2C_SCL`
Connect:

- XIAO D5
- BQ25798 pin 14 SCL
- 10 kOhm pull-up to 3V3

### `BQ_INT`
Connect:

- BQ25798 pin 21 INT
- 10 kOhm pull-up to 3V3

No MCU connection in Rev A.

### `BQ_STAT`
Connect:

```text
3V3 -> Everlight red LED -> 2.2 kOhm -> BQ25798 pin 1 STAT
```

No BSS84 and no separate STAT pull-up.

---

## 8. TPS61088 5 V boost

### `BOOST_VIN`
Same electrical node as `BQ_SYS`.

Connect:

- TPS61088 pin 9 VIN
- input side of Coilcraft XAL7030-222MEC
- 2 x 22 uF + 100 nF to GND

### `BOOST_SW`
Connect:

- TPS61088 pins 4/5/6/7 SW
- output side of XAL7030-222MEC
- low side of 100 nF BOOT capacitor
- low side of 330 kOhm RFREQ resistor

### `BOOST_BOOT`
Connect:

- TPS61088 pin 8 BOOT
- 100 nF to `BOOST_SW`

### `BOOST_FSW`
Connect:

- TPS61088 pin 3 FSW
- 330 kOhm to `BOOST_SW`

### `BOOST_EN`
Connect:

- XIAO D7
- TPS61088 pin 2 EN
- 100 kOhm pulldown to GND

### `BOOST_SS`
Connect:

- TPS61088 pin 10 SS
- 47 nF to AGND/GND

### `BOOST_VCC`
Connect:

- TPS61088 pin 1 VCC
- 2.2 uF to AGND/GND

### `BOOST_ILIM`
Connect:

- TPS61088 pin 19 ILIM
- 100 kOhm to AGND/GND

### `BOOST_COMP`
Connect TPS61088 pin 18 COMP to the locked 20.0 kOhm / 4.7 nF compensation network to AGND. Follow the TI series R-C compensation topology used by the reference design.

### `BOOST_FB`
Connect:

```text
5V_RADIO -> 176 kOhm -> BOOST_FB -> 56.0 kOhm -> AGND
```

- `BOOST_FB` -> TPS61088 pin 17 FB

### `5V_RADIO`
Connect:

- TPS61088 pins 14/15/16 VOUT
- 2 x 47 uF output capacitors to GND
- E22 pins 9/10 VCC
- E22 local 2 x 22 uF, 1 uF, multiple 100 nF, and Panasonic 330 uF polymer to GND

TPS61088 pin 13 MODE: NC/floating.
TPS61088 pins 11/12: connect to GND plane for thermal dissipation.
TPS61088 exposed pad 21 PGND: GND with thermal vias.

---

## 9. E22 digital interface

### `E22_NRST`
XIAO D0 -> E22 pin 15 NRST.

### `E22_DIO1`
XIAO D1 -> E22 pin 13 DIO1.

### `E22_BUSY`
XIAO D2 -> E22 pin 14 BUSY.

### `E22_NSS`
XIAO D3 -> E22 pin 19 NSS.

### `E22_RXEN`
XIAO D6 -> E22 pin 6 RXEN.

### `E22_TXEN_DIO2`
Direct local connection:

- E22 pin 8 DIO2 -> E22 pin 7 TXEN

No XIAO GPIO is connected to TXEN.

### `SPI_SCK`
XIAO D8 -> E22 pin 18 SCK.

### `SPI_MISO`
XIAO D9 <- E22 pin 16 MISO.

### `SPI_MOSI`
XIAO D10 -> E22 pin 17 MOSI.

No external RXEN/TXEN pull-down is currently specified because the current EBYTE documentation does not mandate one. Revisit only if firmware/startup behavior requires it during schematic ERC review.

---

## 10. RF

### `RF_915`
Connect:

- E22 pin 21 ANT
- short 50-ohm grounded coplanar waveguide
- Molex 0732511150 SMA center contact

No series component or test pad.

E22 pins 20/22 and SMA ground tabs -> GND with dense stitching to Layer 2.

---

## 11. XIAO header electrical connections

Carrier socket connections used:

| XIAO header signal | Net |
|---|---|
| D0 | `E22_NRST` |
| D1 | `E22_DIO1` |
| D2 | `E22_BUSY` |
| D3 | `E22_NSS` |
| D4 | `I2C_SDA` |
| D5 | `I2C_SCL` |
| D6 | `E22_RXEN` |
| D7 | `BOOST_EN` |
| D8 | `SPI_SCK` |
| D9 | `SPI_MISO` |
| D10 | `SPI_MOSI` |
| 3V3 | `3V3` |
| GND | `GND` |
| 5V/VBUS | `USB_VBUS_RAW` (input source to charger only; never driven by carrier) |

The XIAO underside `BAT0` and `GND0` pads are connected only by the separate two-wire JST harness.

---

## 12. Schematic capture rules

- Do not silently merge similarly named nets unless this map explicitly says they are the same electrical node.
- Keep `USB_VBUS_RAW`, `SOLAR_PROTECTED`, and `BQ_VBUS` distinct.
- Keep `BAT_RAW` and `BQ_SYS` distinct even though the BQ25798 power path can couple them internally.
- Keep `BQ_SW1`, `BQ_SW2`, and `BOOST_SW` local and compact; they are noisy switch nodes.
- Do not route any switch node or high-current loop through the RF zone.
- Use manufacturer pin numbers exactly as listed in `PIN_AUDIT_REV_A.md`.
- Any discrepancy found during KiCad symbol import stops capture until resolved against the manufacturer datasheet.
