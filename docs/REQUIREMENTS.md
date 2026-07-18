# RoyalNode Rev A Requirements

## 1. Mission

RoyalNode Rev A is an engineering-validation platform for a rugged, solar-powered 915 MHz LoRa repeater using a Seeed XIAO nRF52840 and an EBYTE E22-900M33S radio module.

## 2. Functional requirements

- Operate as a continuously available LoRa repeater.
- Support the E22-900M33S SPI interface and external RF-control behavior.
- Support firmware-controlled radio power, reset and receive/transmit control.
- Expose only telemetry that can be reported through the MeshCore ecosystem.
- Permit safe reduced-power operation when battery charge or temperature is outside preferred limits.
- Do not include dedicated electrical test points, current-shunt footprints, removable measurement links or bench-only instrumentation hardware.

## 3. Power requirements

- Primary energy source: 6 V class, 20 W monocrystalline panel.
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

## 4. Connector standard

### High-current power connectors

- Battery input: XT60.
- Solar input: XT60.
- XT60-equivalent locking connectors may be used only if they meet or exceed XT60 contact reliability, current capability and mechanical retention.
- PCB-mounted XT60 connectors are preferred where enclosure space permits.
- Panel-mounted XT60 connectors with short 16–18 AWG silicone-wire pigtails are acceptable.
- Solar and battery connector positions must be mechanically keyed and clearly labeled to prevent cross-connection.

### Low-current signal connectors

- All JST-style connectors shall use the JST-GH family, 1.25 mm pitch.
- Do not mix JST-PH, JST-XH, JST-SH or JST-ZH families on the board.
- Use JST-GH only for MeshCore-supported environmental telemetry modules.
- No fan, generic analog sensor, general-purpose UART, or six-pin debug/programming JST connector shall be fitted.
- Programming shall use the XIAO USB-C connector.
- Recovery/debug shall use a compact Tag-Connect or exposed SWD pad footprint.
- Every JST-GH connector must have pin 1 and signal names marked on silkscreen.
- JST-GH connections must remain inside the weather-sealed enclosure unless a sealed bulkhead transition is used.

## 5. MeshCore telemetry requirements

Only the following telemetry categories are approved for Rev A:

1. **Battery voltage**
   - Required.
   - Reported through MeshCore base telemetry.
   - Measure the 2S pack with a protected resistor divider into an ADC input or another board-supported method.

2. **MCU temperature**
   - Required where supported by the XIAO nRF52840 board definition.
   - Uses the MCU's internal temperature measurement.
   - Treated as enclosure/electronics temperature, not precise outdoor ambient temperature.

3. **Environmental telemetry**
   - Optional.
   - Temperature, humidity and pressure only.
   - Preferred sensor: BME680 because current MeshCore firmware includes BME680 support.
   - Connection: one 4-pin JST-GH I2C port with 3.3 V, GND, SDA and SCL.
   - Gas-resistance or air-quality values are not required unless MeshCore explicitly exposes them.

4. **GPS/location telemetry**
   - Optional and not required for a fixed repeater.
   - Omit GPS hardware by default.
   - The fixed node position may be configured in firmware instead.

The following shall not be included as deployed telemetry sensors unless future MeshCore support is confirmed:

- solar current sensor
- radio current sensor
- battery current sensor
- external PA temperature sensor
- regulator temperature sensor
- fan tachometer
- generic analog sensors
- arbitrary accessory sensors

## 6. Environmental requirements

- Intended for outdoor use in Canada.
- Electronics enclosure target: IP65 minimum, IP67 preferred.
- Use a pressure-equalizing breathable vent to reduce condensation.
- Battery charging temperature must still be monitored by the charger or battery pack for safety, even if that value is not exposed through MeshCore.
- Materials, connectors and cabling must be suitable for UV exposure or protected inside the enclosure.

## 7. Electrical protection

- Reverse-polarity protection on solar and battery inputs.
- Input fusing on solar and battery paths.
- TVS protection on the solar input.
- Hardware over-voltage protection on the 5 V radio rail.
- Hardware or firmware transmit timeout.
- Brownout supervision and watchdog recovery.
- No current-shunt footprints, zero-ohm measurement links or dedicated probe pads shall be included.

## 8. Mechanical requirements

- Socketed XIAO nRF52840 on Rev A.
- Serviceable EBYTE radio module.
- XT60 battery and solar connectors.
- No low-current connector except the optional 4-pin JST-GH environmental-sensor port.
- Solar wiring sized for approximately 3.3 A continuous current with low voltage drop.
- U.FL-to-bulkhead-SMA antenna connection for Rev A.
- At least four mounting holes.
- Board layout must separate switching power circuitry from the radio module and MCU antenna.

## 9. PCB requirements

- Four-layer PCB.
- Continuous ground plane.
- Two-ounce outer copper preferred.
- ENIG finish preferred.
- Wide copper pours for battery, solar-input and radio-current paths.
- No dedicated test points, measurement loops or shunt footprints.
- Configuration jumpers are allowed only where electrically necessary for uncertain EBYTE control routing, not for current measurement.
- DRC and ERC must pass before fabrication release.

## 10. Firmware requirements

- Safe startup sequencing for the radio supply.
- EBYTE-specific TCXO and RF-switch configuration.
- Low-battery power reduction and shutdown thresholds.
- Charge-temperature lockout support.
- MeshCore battery telemetry.
- MeshCore MCU-temperature telemetry where supported.
- Optional MeshCore environmental telemetry using the supported sensor interface.
- Daily airtime and fault counters.
- Recoverable watchdog behavior.
- Bench-test firmware independent of MeshCore.

## 11. Regulatory requirement

Hardware capability does not imply legal operating permission. Deployed firmware settings, antenna gain, cable loss, bandwidth and duty cycle must be reviewed against current Canadian 902–928 MHz requirements before field operation.

## 12. Rev A acceptance criteria

Rev A is successful when:

1. The charger safely charges and balances the selected 2S pack from a 6 V / 20 W panel.
2. The charger operates in boost mode without unstable panel collapse under varying sunlight.
3. The 5 V radio rail holds regulation during repeated full-power load steps.
4. The XIAO remains stable during radio transmission.
5. The radio initializes, receives and transmits through test firmware.
6. Battery voltage appears correctly through MeshCore telemetry.
7. MCU temperature appears through MeshCore where supported.
8. Optional BME680 temperature, humidity and pressure appear through MeshCore when fitted.
9. XT60 and any fitted JST-GH connector pass continuity, retention and polarity checks.
10. The board survives multi-day outdoor pilot testing without unexplained resets.
