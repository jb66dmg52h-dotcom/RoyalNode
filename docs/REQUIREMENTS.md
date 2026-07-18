# RoyalNode Rev A Requirements

## 1. Mission

RoyalNode Rev A is an engineering-validation platform for a rugged, solar-powered 915 MHz LoRa repeater using a Seeed XIAO nRF52840 and an EBYTE E22-900M33S radio module.

## 2. Functional requirements

- Operate as a continuously available LoRa repeater.
- Support the E22-900M33S SPI interface and external RF-control behavior.
- Expose sufficient test points for bench validation of every critical power and radio signal.
- Support firmware-controlled radio power, reset and receive/transmit control.
- Provide battery, solar-input and radio-rail telemetry.
- Permit safe reduced-power operation when battery charge or temperature is outside preferred limits.

## 3. Power requirements

- Primary energy source: solar panel.
- Nominal solar source: 6 V class, 20 W monocrystalline panel.
- Panel maximum-power current target: approximately 3.3 A or less.
- Panel open-circuit voltage must remain within the selected charger's absolute maximum input rating.
- Energy storage: 2S protected Li-ion battery, 15 Ah target.
- Battery pack must include cell balancing, over-current, over-charge and over-discharge protection.
- The battery connection must be fused at the pack interface.
- Charging must use a true MPPT-capable buck-boost charger suitable for a 6 V input and 2S lithium pack.
- Charging must be inhibited below the cell manufacturer's allowed temperature.
- Radio rail: regulated 5.0 V, 3 A continuous design target, with short transient margin above 3 A.
- MCU and sensing electronics should use a separate low-noise supply path.
- The design must tolerate repeated full-power transmit bursts without brownout or MCU reset.
- A panel above 20 W at 6 V requires a charger with more than 3.3 A continuous input capability or a split/multi-channel input architecture.

## 4. Environmental requirements

- Intended for outdoor use in Canada.
- Electronics enclosure target: IP65 minimum, IP67 preferred.
- Use a pressure-equalizing breathable vent to reduce condensation.
- Battery temperature must be measured directly at the pack.
- PCB temperature should be measured near the radio power amplifier and main regulator.
- Materials, connectors and cabling must be suitable for UV exposure or protected inside the enclosure.

## 5. Electrical protection

- Reverse-polarity protection on solar and battery inputs.
- Input fusing on solar and battery paths.
- TVS protection on the solar input.
- Hardware over-voltage protection on the 5 V radio rail.
- Hardware or firmware transmit timeout.
- Brownout supervision and watchdog recovery.
- Current measurement on the radio rail and solar input.

## 6. Mechanical requirements

- Socketed XIAO nRF52840 on Rev A.
- Serviceable EBYTE radio module.
- Locking battery and solar connectors rated for at least 5 A.
- Solar wiring sized for approximately 3.3 A continuous current with low voltage drop.
- U.FL-to-bulkhead-SMA antenna connection for Rev A.
- At least four mounting holes.
- Board layout must separate switching power circuitry from the radio module and MCU antenna.

## 7. PCB requirements

- Four-layer PCB.
- Continuous ground plane.
- Two-ounce outer copper preferred.
- ENIG finish preferred.
- Wide copper pours for battery, solar-input and radio-current paths.
- Extensive labeled test points.
- Configuration jumpers for uncertain EBYTE control routing.
- DRC and ERC must pass before fabrication release.

## 8. Firmware requirements

- Safe startup sequencing for the radio supply.
- EBYTE-specific TCXO and RF-switch configuration.
- Low-battery power reduction and shutdown thresholds.
- Charge-temperature lockout support.
- Daily airtime and fault counters.
- Recoverable watchdog behavior.
- Bench-test firmware independent of MeshCore.

## 9. Regulatory requirement

Hardware capability does not imply legal operating permission. Deployed firmware settings, antenna gain, cable loss, bandwidth and duty cycle must be reviewed against current Canadian 902–928 MHz requirements before field operation.

## 10. Rev A acceptance criteria

Rev A is successful when:

1. The charger safely charges and balances the selected 2S pack from a 6 V / 20 W panel.
2. The charger operates in boost mode without unstable panel collapse under varying sunlight.
3. The 5 V radio rail holds regulation during repeated full-power load steps.
4. The XIAO remains stable during radio transmission.
5. The radio initializes, receives and transmits through test firmware.
6. Battery, solar and radio-current telemetry are reliable.
7. Thermal measurements remain within component limits.
8. The board survives multi-day outdoor pilot testing without unexplained resets.
