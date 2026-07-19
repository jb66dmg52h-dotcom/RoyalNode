# RoyalNode Rev A Component Compatibility Review

## Verdict

The proposed architecture is broadly compatible, but it is **not ready for schematic freeze**. The main remaining electrical issue is isolation of the XIAO nRF52840's onboard charger from the main battery-charging path. The solar panel itself will be treated as a deployment recommendation rather than a fixed BOM item.

## Compatibility matrix

| Interface | Status | Review |
|---|---|---|
| 1S LiPo to TPS61088 | Compatible | TPS61088 supports single-cell input and can generate 5 V. Validate thermal performance, inductor saturation current, low-battery operation and repeated TX bursts. |
| TPS61088 5 V rail to E22-900M33S | Compatible | E22 high-power version requires about 5 V for rated output and can draw about 1.1–1.2 A during transmission. Design for at least 3 A rail capability and strong transient capacitance. |
| XIAO nRF52840 logic to E22 SPI | Compatible | Both use 3.3 V logic. Required signals are NSS, SCK, MOSI, MISO, BUSY, DIO1, NRST, TXEN and RXEN; confirm GPIO allocation before layout. |
| XIAO USB-C to firmware updates | Compatible | Native USB supports firmware updates. Preserve D+/D- routing and reset/boot access. |
| XIAO onboard charger to main charger | Conflict unless isolated | XIAO includes a 50/100 mA LiPo charger. Do not directly parallel it with the multi-amp BQ24650 battery path without a verified isolation/OR-ing design. |
| Recommended 12 V nominal panel class to BQ24650 | Compatible within limits | Do not require one panel SKU. Deployment instructions must specify a safe Vmp/Voc/Imp envelope and cold-weather Voc margin. |
| BQ24650 to 1S LiPo | Compatible in principle | Float voltage, current sense, NTC network, MOSFETs and inductor must be calculated for the pack and design charge current. |
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

## Deployment panel recommendation

The hardware should be documented for a compatible panel class rather than a single model. A practical recommendation is:

- 12 V nominal monocrystalline panel
- approximately 10–20 W
- Vmp in the normal mid-to-high-teen range for 12 V-class panels
- Voc and cold-weather Voc below the charger input limit with engineering margin
- panel current within the input connector, fuse and charger design limits

Installers must verify Vmp, Voc, Imp and cold-weather Voc before deployment.

## Required decisions before schematic capture

1. Select the exact protected flat LiPo, including capacity, maximum charge current, continuous discharge current, protection cutoff and NTC characteristics.
2. Decide whether USB-C feeds the BQ24650 path, a separate USB charger, or a power-path combiner.
3. Define how the XIAO onboard charger is isolated.
4. Select exact XT30 PCB parts and use unmistakable battery/solar keying.
5. Select the board-edge SMA footprint and PCB stack-up so the 50-ohm trace width can be calculated.
6. Select the power-button latch/load-switch solution.
7. Complete a formal GPIO/pin-assignment table.
8. Check MeshCore firmware support for external PA control, RX/TX switch control and TCXO configuration.
9. Run power, thermal, RF-layout and regulatory reviews before ordering Rev A.
