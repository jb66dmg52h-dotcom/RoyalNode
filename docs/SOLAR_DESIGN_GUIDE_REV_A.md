# 2Watt Project Solar Design Guide, Rev A

## Supported panel class

- Nominal panel class: 12 V
- Supported deployment size: 10-20 W
- Minimum recommended size: 10 W
- Preferred permanent-deployment size: 20 W
- Installer must verify Vmp, Voc, Imp and cold-weather Voc
- Board input target: 24 V maximum recommended operating Voc, subject to final schematic validation

## 10 W panel calculation

Representative 12 V-class 10 W panel assumptions:

- Vmp: approximately 17 V
- Imp: approximately 0.59 A
- Maximum panel power: 10 W
- Charger efficiency assumption: 90%
- Usable power after charger loss: approximately 9 W

### Heavy continuous radio load

Approximate load budget:

- E22 at full-power transmit: up to roughly 6 W at the 5 V rail
- XIAO and support electronics: approximately 0.3-0.6 W
- Converter losses and margin: approximately 1 W
- Full-load system estimate: approximately 7.5-8 W

Under ideal full sun, a 10 W panel leaves roughly 1 W for charging during continuous full-power transmission. At a battery voltage near 3.8 V, this is approximately 0.25 A after conversion losses.

### Normal repeater duty cycle

A repeater normally spends much more time receiving or idle than transmitting continuously. At an illustrative 2 W average system load, a 10 W panel can leave approximately 7 W for battery charging in strong sun, equivalent to roughly 1.6-1.8 A into a 1S battery after conversion losses.

### Daily energy

At five peak-sun-hours:

- 10 W x 5 h = 50 Wh raw solar energy
- approximately 45 Wh after 90% charge-path efficiency

A nominal 3.7 V, 10 Ah battery stores about 37 Wh. Therefore, one good solar day can theoretically replace about one full battery's nominal energy while also supporting the system load, but real results depend on orientation, weather, temperature, shading and radio traffic.

## 20 W recommendation

A 20 W panel is preferred for permanent outdoor deployments because it:

- provides more winter and cloudy-day margin
- recovers the 10 Ah battery faster after poor weather
- is more likely to maintain the configured 2 A charge current
- better supports high radio traffic

A 20 W panel near 17 V Vmp produces roughly 1.18 A at maximum power. This remains within the locked 2 A solar-input fuse choice while providing substantially more energy than the 10 W option.

## Locked solar protection

- Fuse: Littelfuse 0483002.DR, 2 A, 75 V, 1206 fast-acting SMD
- TVS: Littelfuse SMBJ22A, unidirectional, 22 V standoff, 600 W
- Reverse-polarity MOSFET: Infineon BSL303SPE, P-channel, -30 V, TSOP-6

## Deployment verdict

- 10 W: supported and workable for normal repeater duty cycle
- 20 W: recommended for permanent outdoor use
- Above 20 W: not prohibited by wattage alone, but input current and Voc must remain inside the board limits
