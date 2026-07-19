# RoyalNode Rev A Component Compatibility Review

## Verdict

The proposed architecture is broadly compatible, but it is **not ready for schematic freeze**. Two items are currently critical: the 6 V panel/BQ24650 voltage margin, and isolation of the XIAO nRF52840's onboard charger from the main battery-charging path.

## Compatibility matrix

| Interface | Status | Review |
|---|---|---|
| 1S LiPo to TPS61088 | Compatible | TPS61088 supports single-cell input and can generate 5 V. Validate thermal performance, inductor saturation current, low-battery operation and repeated TX bursts. |
| TPS61088 5 V rail to E22-900M33S | Compatible | E22 high-power version requires about 5 V for rated output and can draw about 1.1–1.2 A during transmission. Design for at least 3 A rail capability and strong transient capacitance. |
| XIAO nRF52840 logic to E22 SPI | Compatible | Both use 3.3 V logic. Required signals are NSS, SCK, MOSI, MISO, BUSY, DIO1, NRST, TXEN and RXEN; confirm GPIO allocation before layout. |
| XIAO USB-C to firmware updates | Compatible | Native USB supports firmware updates. Preserve D+/D- routing and reset/boot access. |
| XIAO onboard charger to main charger | Conflict unless isolated | XIAO includes a 50/100 mA LiPo charger. Do not directly parallel it with the multi-amp BQ24650 battery path without a verified isolation/OR-ing design. |
| 6 V panel to BQ24650 | Marginal / unresolved | BQ24650 accepts 5–28 V, but it is a buck charger. A nominal 6 V panel may not retain enough voltage above a 4.2 V battery under heat, shade, cable loss and MPPT regulation. Exact Vmp/Voc are mandatory. |
| BQ24650 to 1S LiPo | Compatible in principle | Float voltage, current sense, NTC network, MOSFETs and inductor must be calculated for the exact pack and panel. |
| MAX17048 to 1S LiPo and XIAO I2C | Compatible | Suitable for a single Li-ion cell and 3.3 V I2C. Place close to the battery node and avoid noisy boost-current paths. |
| XT30 solar input | Compatible | Electrically oversized but compact and rugged. Use a board-mounted through-hole part with mechanical enclosure support and reverse-polarity protection. |
| XT30 battery input | Compatible | Current rating is ample. Use a different gender and/or physical orientation from the solar connector to prevent cross-connection. |
| E22 ANT pin to board-edge SMA | Compatible | Use a very short controlled-impedance 50-ohm trace, continuous ground reference, via stitching and no switching-node routing nearby. |
| Push-button power control | Compatible but unspecified | Requires a chosen latch/load-switch circuit. It must survive radio current, allow USB wake/power and provide a hard-off recovery method. |
| Charging/status LEDs | Compatible | BQ24650 provides status outputs. Keep LED current low and consider firmware-controlled dimming or disablement at night. |
| Battery telemetry | Compatible | MAX17048 is preferred; direct ADC may be retained as a diagnostic cross-check. |

## GPIO budget to confirm

Minimum likely E22 connections:

- SPI: SCK, MOSI, MISO, NSS
- control/status: BUSY, DIO1, NRST, TXEN, RXEN
- optional: DIO2 if firmware uses it rather than dedicated TXEN control

Additional board functions need GPIO for:

- power-button sense/hold
- status LED
- charger-status input(s)
- optional ADC battery cross-check
- I2C for MAX17048

The XIAO has enough functions on paper, but the exact pin map must avoid USB, SWD, battery-charge-current control and onboard battery-monitor pins.

## Required decisions before schematic capture

1. Select the exact solar panel and record Vmp, Imp and Voc at standard and hot conditions.
2. Select the exact protected flat LiPo, including capacity, maximum charge current, continuous discharge current, protection cutoff and NTC characteristics.
3. Decide whether USB-C feeds the BQ24650 path, a separate USB charger, or a power-path combiner.
4. Define how the XIAO onboard charger is isolated.
5. Select exact XT30 PCB parts and use unmistakable battery/solar keying.
6. Select the board-edge SMA footprint and PCB stack-up so the 50-ohm trace width can be calculated.
7. Select the power-button latch/load-switch solution.
8. Complete a formal GPIO/pin-assignment table.
9. Check MeshCore firmware support for external PA control, RX/TX switch control and TCXO configuration.
10. Run power, thermal, RF-layout and regulatory reviews before ordering Rev A.
