# 2Watt Project Final Compatibility Audit, Rev 4

## Verdict

Rev A is compatible at the architecture level and may proceed to KiCad schematic capture. No unresolved feature decision blocks the schematic.

## Compatibility matrix

| Interface | Result | Final treatment |
|---|---|---|
| Protected 1S LiPo to BQ25798 | Compatible | 1S profile, 2 A maximum charge target |
| 12 V-class solar to BQ25798 | Compatible | 2 A fuse, reverse-polarity P-FET, 22 V TVS |
| XIAO USB-C VBUS to BQ25798 | Compatible with protected branch | Carrier does not drive VBUS; USB current starts conservatively |
| Battery/system node to XIAO | Compatible | LM66100 to JST-PH to XIAO BAT/GND |
| XIAO onboard charger to main battery | Isolated | LM66100 blocks reverse current toward main rail |
| BQ25798 and MAX17048 on I2C | Compatible | Shared 3.3 V pull-ups, separate addresses, polling |
| 1S rail to TPS61088 | Compatible | 2.2 uH high-current inductor and calculated current limit |
| TPS61088 5 V to E22 | Compatible | Direct connection, controlled soft-start and local bulk capacitance |
| XIAO GPIO to E22 | Compatible | 3.3 V logic and all required control lines allocated |
| E22 ANT to SMA | Compatible | Short controlled 50-ohm route with tuning footprint |
| XT30 battery and solar | Compatible | Different gender/orientation and clear silkscreen |
| No battery thermistor | Functionally compatible with limitation | Fixed TS bias; deployment temperature warning required |
| No radio load switch/eFuse | Compatible for Rev A | Rely on converter protection and prototype transient testing |

## Final component interactions

### BQ25798

- Handles 5 V USB and 12 V-class solar through separate input paths.
- Provides 1S charging and system power path.
- Uses 4.7 kOhm PROG, /CE low and fixed TS bias.
- Charger data is polled over I2C.

### TPS61088 and E22

- TPS61088 is sized for 2 A continuous and 3 A transient at 5 V.
- E22 is connected directly to the 5 V output.
- 330-470 uF bulk and ceramic decoupling are placed locally at the radio.
- TXEN and RXEN pull-downs prevent accidental transmit during MCU reset.

### XIAO

- Edge pins carry only radio and I2C signals.
- The two-wire JST carries only BAT-range positive and ground.
- The carrier does not apply 5 V to the XIAO VBUS node.
- USB-C remains available for firmware updates and USB power.

### Solar input

- 10 W panel works for normal repeater duty cycle.
- 20 W panel is recommended for permanent deployment.
- The 2 A fuse supports both panel sizes with current margin.

## Known limitations accepted for Rev A

- No automatic cold-charge battery protection.
- No carrier power switch.
- No independent radio shutdown.
- No SWD connector.
- No reverse-polarity protection on the keyed battery XT30.
- No enclosure-specific mechanical validation yet.

## Mandatory prototype tests

1. Verify USB insertion with battery and solar connected produces no backfeed.
2. Confirm autonomous 1S charging before firmware configuration.
3. Measure 5 V droop and XIAO stability during repeated 33 dBm transmissions.
4. Measure TPS61088 and charger temperatures at low battery voltage and 2 A charging.
5. Compare PFM and forced-PWM modes for RF noise.
6. Verify MAX17048 voltage and SOC reporting.
7. Verify solar MPPT with representative 10 W and 20 W panels.
8. Confirm XT30 polarity and connector-keying strategy before fabrication.

## Release gate

Proceed to KiCad schematic capture. Do not proceed from schematic to PCB layout until ERC passes and the captured schematic receives another pin-by-pin review against the BQ25798, TPS61088, XIAO and E22 source documents.
