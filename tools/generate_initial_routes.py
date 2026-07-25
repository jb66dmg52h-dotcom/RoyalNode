#!/usr/bin/env python3
"""Generate the first low-risk RoyalNode PCB routes.

This intentionally routes only stable, low-current nets and adds the intended
top and Layer-2 ground pours. It does not route RF, high-current power rails or
switching loops.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "hardware/kicad/RoyalNode/RoyalNode.kicad_pcb"
NAMESPACE = uuid.UUID("0c64c82f-b03a-455f-93ce-ceb8a0674a31")

SEGMENTS = [
    {
        "name": "e22-dio2-to-txen",
        "net": "E22_TXEN_DIO2",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(30.35, 59.08), (30.35, 61.62)],
    },
    {
        "name": "e22-vcc-local",
        "net": "5V_RADIO",
        "layer": "F.Cu",
        "width": 0.80,
        "points": [(30.35, 64.16), (30.35, 66.70)],
    },
    {
        "name": "u3-5v-radio-local",
        "net": "5V_RADIO",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(57.35, 54.25), (57.35, 55.25)],
    },
    {
        "name": "radio-bulk-cap-bank",
        "net": "5V_RADIO",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(56.53, 93.40), (62.53, 93.40), (69.05, 93.40), (75.23, 93.40)],
    },
    {
        "name": "radio-bulk-c500-stub",
        "net": "5V_RADIO",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(56.53, 91.00), (56.53, 93.40)],
    },
    {
        "name": "radio-bulk-c501-stub",
        "net": "5V_RADIO",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(62.53, 91.00), (62.53, 93.40)],
    },
    {
        "name": "radio-bulk-c502-stub",
        "net": "5V_RADIO",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(69.05, 91.00), (69.05, 93.40)],
    },
    {
        "name": "radio-bulk-c504-c505-stub",
        "net": "5V_RADIO",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(75.23, 86.00), (75.23, 91.00), (75.23, 93.40)],
    },
    {
        "name": "u3-boost-sw-upper-local",
        "net": "BOOST_SW",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(60.65, 54.25), (60.65, 54.75)],
    },
    {
        "name": "u3-boost-sw-lower-local",
        "net": "BOOST_SW",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(60.65, 55.25), (60.65, 55.75)],
    },
    {
        "name": "boost-sw-u3-to-l2-upper",
        "net": "BOOST_SW",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(60.65, 54.75), (62.40, 54.75), (62.40, 55.00), (64.14, 55.00)],
    },
    {
        "name": "boost-sw-u3-to-l2-lower",
        "net": "BOOST_SW",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(60.65, 55.25), (62.40, 55.25), (62.40, 55.00)],
    },
    {
        "name": "boost-boot-u3-to-c406",
        "net": "BOOST_BOOT",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(60.65, 53.75), (61.45, 53.75), (61.45, 49.60), (62.13, 49.60)],
    },
    {
        "name": "boost-boot-c406-sw",
        "net": "BOOST_SW",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(63.68, 49.60), (64.60, 49.60), (64.60, 55.00), (64.14, 55.00)],
    },
    {
        "name": "boost-fsw-u3-to-r402",
        "net": "BOOST_FSW",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(60.65, 56.25), (61.45, 56.25), (61.45, 60.40), (62.08, 60.40)],
    },
    {
        "name": "boost-fsw-r402-sw",
        "net": "BOOST_SW",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(63.73, 60.40), (64.60, 60.40), (64.60, 55.00), (64.14, 55.00)],
    },
    {
        "name": "i2c-pullup-3v3-link",
        "net": "3V3",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(80.39, 33.54), (84.98, 33.00), (84.98, 35.60)],
    },
    {
        "name": "i2c-pullup-sda-fanout",
        "net": "I2C_SDA",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(86.62, 33.00), (86.62, 32.00)],
    },
    {
        "name": "i2c-pullup-sda-backbone",
        "net": "I2C_SDA",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(86.62, 32.00), (86.62, 41.40)],
    },
    {
        "name": "i2c-sda-bus-join",
        "net": "I2C_SDA",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(67.20, 41.40), (86.62, 41.40)],
    },
    {
        "name": "i2c-sda-xiao-entry",
        "net": "I2C_SDA",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(67.20, 41.40), (62.61, 33.54)],
    },
    {
        "name": "i2c-pullup-scl-fanout",
        "net": "I2C_SCL",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(86.62, 35.60), (87.60, 35.60), (87.60, 34.60)],
    },
    {
        "name": "i2c-pullup-scl-backbone",
        "net": "I2C_SCL",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(87.60, 34.60), (87.60, 42.80)],
    },
    {
        "name": "i2c-scl-bus-join",
        "net": "I2C_SCL",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(64.80, 42.80), (87.60, 42.80)],
    },
    {
        "name": "i2c-scl-xiao-entry",
        "net": "I2C_SCL",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(64.80, 42.80), (64.80, 36.08), (62.61, 36.08)],
    },
    {
        "name": "j6-sda-service-fanout",
        "net": "I2C_SDA",
        "layer": "F.Cu",
        "width": 0.15,
        "points": [(95.63, 22.95), (95.63, 24.45)],
    },
    {
        "name": "j6-sda-service-backbone",
        "net": "I2C_SDA",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(95.63, 24.45), (86.62, 32.00)],
    },
    {
        "name": "j6-scl-service-fanout",
        "net": "I2C_SCL",
        "layer": "F.Cu",
        "width": 0.15,
        "points": [(96.88, 22.95), (96.88, 24.45)],
    },
    {
        "name": "j6-scl-service-backbone",
        "net": "I2C_SCL",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(96.88, 24.45), (87.60, 34.60)],
    },
    {
        "name": "j6-3v3-service-route",
        "net": "3V3",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(93.13, 22.95), (93.13, 24.45), (90.40, 24.45), (90.40, 36.70), (84.98, 36.70), (84.98, 35.60)],
    },
    {
        "name": "bq-sda-fanout",
        "net": "I2C_SDA",
        "layer": "F.Cu",
        "width": 0.15,
        "points": [(66.00, 76.90), (66.00, 77.80), (67.20, 77.80), (67.20, 78.80)],
    },
    {
        "name": "bq-sda-backbone",
        "net": "I2C_SDA",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(67.20, 78.80), (67.20, 41.40)],
    },
    {
        "name": "bq-scl-fanout",
        "net": "I2C_SCL",
        "layer": "F.Cu",
        "width": 0.15,
        "points": [(65.60, 76.90), (65.60, 79.20), (64.80, 79.20), (64.80, 80.60)],
    },
    {
        "name": "bq-scl-backbone",
        "net": "I2C_SCL",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(64.80, 80.60), (64.80, 42.80)],
    },
    {
        "name": "bq-prog-local-route",
        "net": "BQ_PROG",
        "layer": "F.Cu",
        "width": 0.15,
        "points": [(66.90, 75.00), (68.80, 75.00), (68.80, 76.00), (69.68, 76.00)],
    },
    {
        "name": "bq-int-local-route",
        "net": "BQ_INT",
        "layer": "F.Cu",
        "width": 0.15,
        "points": [(66.90, 74.60), (71.33, 74.60), (71.33, 73.20)],
    },
    {
        "name": "bq-pmid-cap-bank-bus",
        "net": "BQ_PMID",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(33.73, 75.00), (39.33, 75.00), (44.93, 75.00)],
    },
    {
        "name": "bq-vbus-cap-bank-bus",
        "net": "BQ_VBUS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(22.53, 75.00), (28.13, 75.00)],
    },
    {
        "name": "bq-vbus-c200-stub",
        "net": "BQ_VBUS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(22.53, 77.00), (22.53, 75.00)],
    },
    {
        "name": "bq-vbus-c201-stub",
        "net": "BQ_VBUS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(28.13, 77.00), (28.13, 75.00)],
    },
    {
        "name": "bq-vbus-c212-bus-via-fanout",
        "net": "BQ_VBUS",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(22.53, 75.00), (21.40, 75.00)],
    },
    {
        "name": "bq-vbus-c212-bottom-jog",
        "net": "BQ_VBUS",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(21.40, 75.00), (21.40, 85.80), (22.40, 85.80)],
    },
    {
        "name": "bq-vbus-c212-pad-fanout",
        "net": "BQ_VBUS",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(22.40, 85.80), (23.23, 85.00)],
    },
    {
        "name": "bq-pmid-c202-stub",
        "net": "BQ_PMID",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(33.73, 77.00), (33.73, 75.00)],
    },
    {
        "name": "bq-pmid-c203-stub",
        "net": "BQ_PMID",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(39.33, 77.00), (39.33, 75.00)],
    },
    {
        "name": "bq-pmid-c204-stub",
        "net": "BQ_PMID",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(44.93, 77.00), (44.93, 75.00)],
    },
    {
        "name": "bq-pmid-c213-bus-via-fanout",
        "net": "BQ_PMID",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(33.73, 75.00), (32.60, 75.00)],
    },
    {
        "name": "bq-pmid-c213-bottom-jog",
        "net": "BQ_PMID",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(32.60, 75.00), (27.60, 75.00), (27.60, 85.80)],
    },
    {
        "name": "bq-pmid-c213-pad-fanout",
        "net": "BQ_PMID",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(27.60, 85.80), (28.83, 85.00)],
    },
    {
        "name": "bq-sys-cap-bank-bus",
        "net": "BQ_SYS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(22.53, 83.40), (28.13, 83.40), (33.73, 83.40), (39.33, 83.40)],
    },
    {
        "name": "bq-sys-c206-stub",
        "net": "BQ_SYS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(22.53, 81.00), (22.53, 83.40)],
    },
    {
        "name": "bq-sys-c207-stub",
        "net": "BQ_SYS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(28.13, 81.00), (28.13, 83.40)],
    },
    {
        "name": "bq-sys-c208-stub",
        "net": "BQ_SYS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(33.73, 81.00), (33.73, 83.40)],
    },
    {
        "name": "bq-sys-c209-stub",
        "net": "BQ_SYS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(39.33, 81.00), (39.33, 83.40)],
    },
    {
        "name": "bq-sys-c214-stub",
        "net": "BQ_SYS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(34.43, 85.00), (34.43, 83.40)],
    },
    {
        "name": "bat-raw-cap-bank-bus",
        "net": "BAT_RAW",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(44.93, 83.40), (50.53, 83.40)],
    },
    {
        "name": "bat-raw-c210-stub",
        "net": "BAT_RAW",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(44.93, 81.00), (44.93, 83.40)],
    },
    {
        "name": "bat-raw-c211-stub",
        "net": "BAT_RAW",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(50.53, 81.00), (50.53, 83.40)],
    },
    {
        "name": "bat-raw-r202-to-cap-bus-branch",
        "net": "BAT_RAW",
        "layer": "F.Cu",
        "width": 0.25,
        "points": [(39.98, 89.00), (39.98, 88.00), (43.80, 88.00), (43.80, 83.40), (44.93, 83.40)],
    },
    {
        "name": "boost-input-c400-c401-local-bus",
        "net": "BQ_SYS",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(23.03, 24.50), (23.03, 22.50), (28.63, 22.50), (28.63, 24.50)],
    },
    {
        "name": "boost-output-c402-c403-local-bus",
        "net": "5V_RADIO",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(34.23, 24.50), (34.23, 22.50), (39.83, 22.50), (39.83, 24.50)],
    },
    {
        "name": "boost-output-r400-sense-to-cap-bus",
        "net": "5V_RADIO",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(39.83, 24.50), (39.83, 26.60), (40.48, 26.60), (40.48, 29.00)],
    },
    {
        "name": "charge-led-k-local",
        "net": "CHG_LED_K",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(35.99, 93.00), (39.98, 93.00)],
    },
    {
        "name": "bq-stat-r207-fanout",
        "net": "BQ_STAT",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(41.62, 93.00), (42.60, 93.00)],
    },
    {
        "name": "bq-stat-backbone",
        "net": "BQ_STAT",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(42.60, 93.00), (62.40, 93.00), (62.40, 73.40)],
    },
    {
        "name": "bq-stat-u1-entry",
        "net": "BQ_STAT",
        "layer": "F.Cu",
        "width": 0.15,
        "points": [(62.40, 73.40), (63.10, 73.40)],
    },
    {
        "name": "bq-ts-divider-local",
        "net": "BQ_TS",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(30.43, 89.00), (34.38, 89.00)],
    },
    {
        "name": "bq-regn-r200-c215-local-link",
        "net": "BQ_REGN",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(28.78, 89.00), (28.78, 87.10), (39.85, 87.10), (39.85, 85.00)],
    },
    {
        "name": "uv-divider-local",
        "net": "UV_NODE",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(22.83, 38.00), (25.98, 38.00)],
    },
    {
        "name": "ov-divider-local",
        "net": "OV_NODE",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(27.63, 38.00), (29.00, 38.00), (29.00, 44.40), (21.18, 44.40), (21.18, 42.80)],
    },
    {
        "name": "u2-gnd-local",
        "net": "GND",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(83.16, 49.00), (84.84, 49.00)],
    },
    {
        "name": "u2-xiao-bat-iso-local",
        "net": "XIAO_BAT_ISO",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(83.16, 49.65), (82.40, 49.65), (82.40, 50.30), (85.60, 50.30), (85.60, 48.35), (84.84, 48.35)],
    },
    {
        "name": "j3-xiao-bat-iso-service-route",
        "net": "XIAO_BAT_ISO",
        "layer": "B.Cu",
        "width": 0.30,
        "points": [(85.60, 50.30), (102.40, 50.30), (102.40, 87.80), (94.38, 87.80)],
    },
    {
        "name": "j3-xiao-bat-iso-pad-entry",
        "net": "XIAO_BAT_ISO",
        "layer": "F.Cu",
        "width": 0.30,
        "points": [(94.38, 87.80), (94.38, 89.15)],
    },
    {
        "name": "j4-ntc-sense-service-route",
        "net": "NTC_SENSE",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(36.03, 89.00), (36.03, 93.60), (83.88, 93.60), (83.88, 86.65)],
    },
    {
        "name": "solar-raw-xt30-to-fuse",
        "net": "SOLAR_RAW",
        "layer": "F.Cu",
        "width": 0.80,
        "points": [(90.50, 57.00), (85.60, 57.00), (85.60, 54.00)],
    },
    {
        "name": "q1-solar-prot-gate-local",
        "net": "SOLAR_PROT_GATE",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(75.38, 55.37), (74.20, 55.37), (74.20, 57.91), (75.38, 57.91)],
    },
    {
        "name": "solar-prot-gate-u4-fanout-b",
        "net": "SOLAR_PROT_GATE",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(75.14, 49.03), (76.60, 49.03)],
    },
    {
        "name": "solar-prot-gate-backbone-b",
        "net": "SOLAR_PROT_GATE",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(76.60, 49.03), (74.00, 49.03), (74.00, 55.37)],
    },
    {
        "name": "solar-prot-gate-q1-entry-b",
        "net": "SOLAR_PROT_GATE",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(74.00, 55.37), (74.20, 55.37)],
    },
    {
        "name": "q1-solar-prot-common-left-fanout",
        "net": "SOLAR_PROT_COMMON",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(75.38, 54.10), (72.50, 54.10)],
    },
    {
        "name": "q1-solar-prot-common-backbone",
        "net": "SOLAR_PROT_COMMON",
        "layer": "B.Cu",
        "width": 0.40,
        "points": [(72.50, 54.10), (72.50, 58.50), (82.00, 58.50), (82.00, 56.64)],
    },
    {
        "name": "q1-solar-prot-common-right-entry",
        "net": "SOLAR_PROT_COMMON",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(82.00, 56.64), (80.63, 56.64)],
    },
    {
        "name": "q2-acdrv1-gate-local",
        "net": "BQ_ACDRV1",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(75.38, 63.37), (74.20, 63.37), (74.20, 65.91), (75.38, 65.91)],
    },
    {
        "name": "q3-acdrv2-gate-local",
        "net": "BQ_ACDRV2",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(75.38, 71.37), (74.20, 71.37), (74.20, 73.91), (75.38, 73.91)],
    },
    {
        "name": "q1-solar-fused-drain-local",
        "net": "SOLAR_FUSED",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(80.63, 54.10), (80.63, 55.37)],
    },
    {
        "name": "solar-fused-fuse-fanout",
        "net": "SOLAR_FUSED",
        "layer": "F.Cu",
        "width": 0.80,
        "points": [(88.40, 54.00), (89.60, 54.00)],
    },
    {
        "name": "solar-fused-backbone",
        "net": "SOLAR_FUSED",
        "layer": "B.Cu",
        "width": 0.80,
        "points": [(89.60, 54.00), (89.60, 52.20), (80.63, 52.20)],
    },
    {
        "name": "solar-fused-q1-entry",
        "net": "SOLAR_FUSED",
        "layer": "F.Cu",
        "width": 0.80,
        "points": [(80.63, 52.20), (80.63, 54.10)],
    },
    {
        "name": "solar-fused-divider-r100-fanout",
        "net": "SOLAR_FUSED",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(21.18, 38.00), (21.18, 39.00)],
    },
    {
        "name": "solar-fused-divider-bottom-jog",
        "net": "SOLAR_FUSED",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(21.18, 39.00), (21.18, 44.00), (25.98, 44.00), (25.98, 43.70)],
    },
    {
        "name": "solar-fused-divider-r103-fanout",
        "net": "SOLAR_FUSED",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(25.98, 43.70), (25.98, 42.80)],
    },
    {
        "name": "q2-solar-protected-drain-local",
        "net": "SOLAR_PROTECTED",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(80.63, 62.10), (80.63, 63.37)],
    },
    {
        "name": "q2-solar-selector-common-left-fanout-b",
        "net": "BQ_SOLAR_SELECTOR_COMMON",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(75.38, 62.10), (72.50, 62.10)],
    },
    {
        "name": "q2-solar-selector-common-backbone-b",
        "net": "BQ_SOLAR_SELECTOR_COMMON",
        "layer": "B.Cu",
        "width": 0.40,
        "points": [(72.50, 62.10), (72.50, 66.50), (82.00, 66.50), (82.00, 64.64)],
    },
    {
        "name": "q2-solar-selector-common-right-entry-b",
        "net": "BQ_SOLAR_SELECTOR_COMMON",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(82.00, 64.64), (80.63, 64.64)],
    },
    {
        "name": "solar-protected-q1-to-q2",
        "net": "SOLAR_PROTECTED",
        "layer": "F.Cu",
        "width": 0.80,
        "points": [(80.63, 57.91), (80.63, 62.10)],
    },
    {
        "name": "q3-usb-vbus-raw-drain-local",
        "net": "USB_VBUS_RAW",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(80.63, 70.10), (80.63, 71.37)],
    },
    {
        "name": "q3-usb-selector-common-left-fanout-b",
        "net": "BQ_USB_SELECTOR_COMMON",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(75.38, 70.10), (72.50, 70.10)],
    },
    {
        "name": "q3-usb-selector-common-backbone-b",
        "net": "BQ_USB_SELECTOR_COMMON",
        "layer": "B.Cu",
        "width": 0.40,
        "points": [(72.50, 70.10), (72.50, 74.50), (82.00, 74.50), (82.00, 72.64)],
    },
    {
        "name": "q3-usb-selector-common-right-entry-b",
        "net": "BQ_USB_SELECTOR_COMMON",
        "layer": "F.Cu",
        "width": 0.40,
        "points": [(82.00, 72.64), (80.63, 72.64)],
    },
    {
        "name": "bq-vbus-q2-right-fanout",
        "net": "BQ_VBUS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(80.63, 65.91), (83.50, 65.91)],
    },
    {
        "name": "bq-vbus-q2-q3-backbone",
        "net": "BQ_VBUS",
        "layer": "B.Cu",
        "width": 0.60,
        "points": [(83.50, 65.91), (83.50, 73.91)],
    },
    {
        "name": "bq-vbus-q3-right-entry",
        "net": "BQ_VBUS",
        "layer": "F.Cu",
        "width": 0.60,
        "points": [(83.50, 73.91), (80.63, 73.91)],
    },
    {
        "name": "u1-bq-vbus-local",
        "net": "BQ_VBUS",
        "layer": "F.Cu",
        "width": 0.15,
        "points": [(63.10, 73.80), (63.10, 74.20)],
    },
    {
        "name": "u1-bat-raw-local",
        "net": "BAT_RAW",
        "layer": "F.Cu",
        "width": 0.15,
        "points": [(66.90, 73.80), (66.90, 74.20)],
    },
    {
        "name": "boost-fb-r400-r401-local-link",
        "net": "BOOST_FB",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(42.13, 29.00), (46.08, 29.00)],
    },
    {
        "name": "boost-comp-rc-r404-fanout",
        "net": "BOOST_COMP_RC",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(27.63, 47.00), (28.80, 47.00)],
    },
    {
        "name": "boost-comp-rc-bottom-route",
        "net": "BOOST_COMP_RC",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(28.80, 47.00), (28.80, 34.00), (34.10, 34.00), (34.10, 29.00)],
    },
    {
        "name": "boost-comp-rc-c408-fanout",
        "net": "BOOST_COMP_RC",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(34.10, 29.00), (34.93, 29.00)],
    },
    {
        "name": "e22-nrst-fanout",
        "net": "E22_NRST",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(53.65, 61.62), (54.60, 61.62)],
    },
    {
        "name": "e22-nrst-backbone",
        "net": "E22_NRST",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(54.60, 61.62), (54.60, 22.80), (62.61, 22.80), (62.61, 23.38)],
    },
    {
        "name": "e22-dio1-fanout",
        "net": "E22_DIO1",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(53.65, 66.70), (55.20, 66.70)],
    },
    {
        "name": "e22-dio1-backbone",
        "net": "E22_DIO1",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(55.20, 66.70), (55.20, 25.50), (62.61, 25.50), (62.61, 25.92)],
    },
    {
        "name": "e22-busy-fanout",
        "net": "E22_BUSY",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(53.65, 64.16), (55.80, 64.16)],
    },
    {
        "name": "e22-busy-backbone",
        "net": "E22_BUSY",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(55.80, 64.16), (55.80, 28.00), (62.61, 28.00), (62.61, 28.46)],
    },
    {
        "name": "e22-nss-fanout",
        "net": "E22_NSS",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(53.65, 51.46), (57.00, 51.46)],
    },
    {
        "name": "e22-nss-backbone",
        "net": "E22_NSS",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(57.00, 51.46), (57.00, 30.60), (62.61, 30.60), (62.61, 31.00)],
    },
    {
        "name": "e22-rxen-direct",
        "net": "E22_RXEN",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(30.35, 56.54), (28.60, 56.54)],
    },
    {
        "name": "e22-rxen-backbone",
        "net": "E22_RXEN",
        "layer": "In2.Cu",
        "width": 0.20,
        "points": [(28.60, 56.54), (28.60, 68.50), (62.61, 68.50), (62.61, 38.62)],
    },
    {
        "name": "e22-sck-fanout",
        "net": "SPI_SCK",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(53.65, 54.00), (50.40, 54.00)],
    },
    {
        "name": "e22-sck-backbone",
        "net": "SPI_SCK",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(50.40, 54.00), (50.40, 24.60), (88.00, 24.60), (88.00, 25.92)],
    },
    {
        "name": "e22-sck-xiao-entry",
        "net": "SPI_SCK",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(88.00, 25.92), (80.39, 25.92)],
    },
    {
        "name": "e22-miso-fanout",
        "net": "SPI_MISO",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(53.65, 59.08), (51.20, 59.08)],
    },
    {
        "name": "e22-miso-backbone",
        "net": "SPI_MISO",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(51.20, 59.08), (51.20, 27.00), (87.00, 27.00), (87.00, 28.46)],
    },
    {
        "name": "e22-miso-xiao-entry",
        "net": "SPI_MISO",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(87.00, 28.46), (80.39, 28.46)],
    },
    {
        "name": "e22-mosi-fanout",
        "net": "SPI_MOSI",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(53.65, 56.54), (52.40, 56.54)],
    },
    {
        "name": "e22-mosi-backbone",
        "net": "SPI_MOSI",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(52.40, 56.54), (52.40, 32.20), (86.00, 32.20), (86.00, 31.00)],
    },
    {
        "name": "e22-mosi-xiao-entry",
        "net": "SPI_MOSI",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(86.00, 31.00), (80.39, 31.00)],
    },
]

VIAS = [
    {"name": "i2c-pullup-sda-via", "net": "I2C_SDA", "at": (86.62, 32.00)},
    {"name": "i2c-pullup-scl-via", "net": "I2C_SCL", "at": (87.60, 34.60)},
    {"name": "bq-sda-via", "net": "I2C_SDA", "at": (67.20, 78.80)},
    {"name": "bq-scl-via", "net": "I2C_SCL", "at": (64.80, 80.60)},
    {"name": "j6-sda-service-via", "net": "I2C_SDA", "at": (95.63, 24.45)},
    {"name": "j6-scl-service-via", "net": "I2C_SCL", "at": (96.88, 24.45)},
    {"name": "j3-xiao-bat-iso-u2-via", "net": "XIAO_BAT_ISO", "at": (85.60, 50.30)},
    {"name": "j3-xiao-bat-iso-pad-via", "net": "XIAO_BAT_ISO", "at": (94.38, 87.80)},
    {"name": "j4-ntc-sense-r201-via", "net": "NTC_SENSE", "at": (36.03, 89.00)},
    {"name": "j4-ntc-sense-pad-via", "net": "NTC_SENSE", "at": (83.88, 86.65)},
    {"name": "solar-prot-gate-u4-via-b", "net": "SOLAR_PROT_GATE", "at": (76.60, 49.03)},
    {"name": "solar-prot-gate-q1-via-b", "net": "SOLAR_PROT_GATE", "at": (74.00, 55.37)},
    {"name": "q1-solar-prot-common-left-via", "net": "SOLAR_PROT_COMMON", "at": (72.50, 54.10)},
    {"name": "q1-solar-prot-common-right-via", "net": "SOLAR_PROT_COMMON", "at": (82.00, 56.64)},
    {"name": "q2-solar-selector-common-left-via-b", "net": "BQ_SOLAR_SELECTOR_COMMON", "at": (72.50, 62.10)},
    {"name": "q2-solar-selector-common-right-via-b", "net": "BQ_SOLAR_SELECTOR_COMMON", "at": (82.00, 64.64)},
    {"name": "q3-usb-selector-common-left-via-b", "net": "BQ_USB_SELECTOR_COMMON", "at": (72.50, 70.10)},
    {"name": "q3-usb-selector-common-right-via-b", "net": "BQ_USB_SELECTOR_COMMON", "at": (82.00, 72.64)},
    {"name": "bq-pmid-c213-bus-via", "net": "BQ_PMID", "at": (32.60, 75.00)},
    {"name": "bq-pmid-c213-pad-via", "net": "BQ_PMID", "at": (27.60, 85.80)},
    {"name": "bq-vbus-c212-bus-via", "net": "BQ_VBUS", "at": (21.40, 75.00)},
    {"name": "bq-vbus-c212-pad-via", "net": "BQ_VBUS", "at": (22.40, 85.80)},
    {"name": "bq-vbus-q2-via", "net": "BQ_VBUS", "at": (83.50, 65.91)},
    {"name": "bq-vbus-q3-via", "net": "BQ_VBUS", "at": (83.50, 73.91)},
    {"name": "solar-fused-fuse-via", "net": "SOLAR_FUSED", "at": (89.60, 54.00)},
    {"name": "solar-fused-q1-via", "net": "SOLAR_FUSED", "at": (80.63, 52.20)},
    {"name": "solar-fused-divider-r100-via", "net": "SOLAR_FUSED", "at": (21.18, 39.00)},
    {"name": "solar-fused-divider-r103-via", "net": "SOLAR_FUSED", "at": (25.98, 43.70)},
    {"name": "bq-stat-r207-via", "net": "BQ_STAT", "at": (42.60, 93.00)},
    {"name": "bq-stat-u1-via", "net": "BQ_STAT", "at": (62.40, 73.40)},
    {"name": "boost-comp-rc-r404-via", "net": "BOOST_COMP_RC", "at": (28.80, 47.00)},
    {"name": "boost-comp-rc-c408-via", "net": "BOOST_COMP_RC", "at": (34.10, 29.00)},
    {"name": "e22-nrst-via", "net": "E22_NRST", "at": (54.60, 61.62)},
    {"name": "e22-dio1-via", "net": "E22_DIO1", "at": (55.20, 66.70)},
    {"name": "e22-busy-via", "net": "E22_BUSY", "at": (55.80, 64.16)},
    {"name": "e22-nss-via", "net": "E22_NSS", "at": (57.00, 51.46)},
    {"name": "e22-rxen-via", "net": "E22_RXEN", "at": (28.60, 56.54)},
    {"name": "e22-sck-e22-via", "net": "SPI_SCK", "at": (50.40, 54.00)},
    {"name": "e22-sck-xiao-via", "net": "SPI_SCK", "at": (88.00, 25.92)},
    {"name": "e22-miso-e22-via", "net": "SPI_MISO", "at": (51.20, 59.08)},
    {"name": "e22-miso-xiao-via", "net": "SPI_MISO", "at": (87.00, 28.46)},
    {"name": "e22-mosi-e22-via", "net": "SPI_MOSI", "at": (52.40, 56.54)},
    {"name": "e22-mosi-xiao-via", "net": "SPI_MOSI", "at": (86.00, 31.00)},
]

def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "::".join(parts)))


GROUND_ZONES = [
    ("F.Cu", "TOP_GND_FILL", stable_uuid("zone", "top-ground-fill")),
    ("In1.Cu", "L2_GND_REFERENCE", stable_uuid("zone", "l2-ground-reference")),
]
RETIRED_GENERATED_UUIDS = {
    stable_uuid("zone", "bottom-ground-fill"),
    stable_uuid("segment", "e22-rxen-direct", "1"),
    stable_uuid("segment", "e22-rxen-direct", "2"),
    stable_uuid("segment", "j6-3v3-fanout", "0"),
    stable_uuid("segment", "j6-3v3-fanout", "1"),
    stable_uuid("segment", "j6-3v3-backbone", "0"),
    stable_uuid("segment", "j6-3v3-backbone", "1"),
    stable_uuid("segment", "j6-3v3-backbone", "2"),
    stable_uuid("segment", "j6-gnd-fanout", "0"),
    stable_uuid("segment", "j6-gnd-backbone", "0"),
    stable_uuid("segment", "j6-gnd-backbone", "1"),
    stable_uuid("segment", "j6-gnd-backbone", "2"),
    stable_uuid("segment", "j6-sda-fanout", "0"),
    stable_uuid("segment", "j6-sda-fanout", "1"),
    stable_uuid("segment", "j6-sda-backbone", "0"),
    stable_uuid("segment", "j6-sda-backbone", "1"),
    stable_uuid("segment", "j6-sda-backbone", "2"),
    stable_uuid("segment", "j6-sda-backbone", "3"),
    stable_uuid("segment", "j6-scl-fanout", "0"),
    stable_uuid("segment", "j6-scl-fanout", "1"),
    stable_uuid("segment", "j6-scl-backbone", "0"),
    stable_uuid("segment", "j6-scl-backbone", "1"),
    stable_uuid("segment", "j6-scl-backbone", "2"),
    stable_uuid("segment", "j6-scl-backbone", "3"),
    stable_uuid("segment", "i2c-scl-xiao-entry", "2"),
    stable_uuid("segment", "bq-prog-local-route", "0"),
    stable_uuid("segment", "bq-prog-local-route", "1"),
    stable_uuid("segment", "bq-prog-local-route", "2"),
    stable_uuid("segment", "bq-prog-local-route", "3"),
    stable_uuid("segment", "bq-int-local-route", "0"),
    stable_uuid("segment", "bq-int-local-route", "1"),
    stable_uuid("segment", "bq-int-local-route", "2"),
    stable_uuid("segment", "bq-int-local-route", "3"),
    stable_uuid("segment", "boost-fb-divider-local", "0"),
    stable_uuid("segment", "boost-fb-divider-local", "1"),
    stable_uuid("segment", "boost-fb-divider-local", "2"),
    stable_uuid("segment", "boost-fb-divider-local", "3"),
    stable_uuid("segment", "j3-xiao-bat-iso-service-route", "3"),
    stable_uuid("segment", "batp-kelvin-service-route", "0"),
    stable_uuid("segment", "batp-kelvin-service-route", "1"),
    stable_uuid("segment", "batp-kelvin-service-route", "2"),
    stable_uuid("segment", "batp-kelvin-service-route", "3"),
    stable_uuid("segment", "uv-divider-local", "1"),
    stable_uuid("segment", "uv-divider-local", "2"),
    stable_uuid("segment", "uv-divider-local", "3"),
    stable_uuid("segment", "uv-divider-local", "4"),
    stable_uuid("segment", "uv-divider-local", "5"),
    stable_uuid("segment", "ov-divider-local", "4"),
    stable_uuid("segment", "ov-divider-local", "5"),
    stable_uuid("segment", "ltc-shdn-local", "0"),
    stable_uuid("segment", "r204-3v3-fanout", "0"),
    stable_uuid("segment", "r204-3v3-backbone", "0"),
    stable_uuid("segment", "r204-3v3-backbone", "1"),
    stable_uuid("segment", "r204-3v3-backbone", "2"),
    stable_uuid("segment", "q1-solar-prot-common-local", "0"),
    stable_uuid("segment", "q1-solar-prot-common-local", "1"),
    stable_uuid("segment", "q1-solar-prot-common-local", "2"),
    stable_uuid("segment", "solar-prot-gate-u4-fanout", "0"),
    stable_uuid("segment", "solar-prot-gate-backbone", "0"),
    stable_uuid("segment", "solar-prot-gate-q1-entry", "0"),
    stable_uuid("segment", "solar-prot-gate-u4-to-q1", "0"),
    stable_uuid("segment", "solar-prot-gate-u4-to-q1", "1"),
    stable_uuid("segment", "solar-prot-gate-u4-to-q1", "2"),
    stable_uuid("segment", "solar-prot-gate-u4-to-q1", "3"),
    stable_uuid("segment", "solar-fused-fuse-to-q1", "0"),
    stable_uuid("segment", "solar-fused-fuse-to-q1", "1"),
    stable_uuid("segment", "solar-fused-fuse-to-q1", "2"),
    stable_uuid("segment", "solar-fused-backbone", "2"),
    stable_uuid("segment", "solar-protected-u4-fanout", "0"),
    stable_uuid("segment", "solar-protected-u4-sense-backbone", "0"),
    stable_uuid("segment", "solar-protected-u4-sense-backbone", "1"),
    stable_uuid("segment", "solar-protected-q1-sense-entry", "0"),
    stable_uuid("segment", "solar-protected-q1-sense-entry", "1"),
    stable_uuid("segment", "boost-ss-u3-to-c407", "0"),
    stable_uuid("segment", "boost-ss-u3-to-c407", "1"),
    stable_uuid("segment", "boost-ss-u3-to-c407", "2"),
    stable_uuid("segment", "boost-bq-sys-u3-to-l2", "0"),
    stable_uuid("segment", "boost-bq-sys-u3-to-l2", "1"),
    stable_uuid("segment", "boost-bq-sys-u3-to-l2", "2"),
    stable_uuid("segment", "boost-bq-sys-u3-to-l2", "3"),
    stable_uuid("segment", "usb-vbus-q3-fanout", "0"),
    stable_uuid("segment", "usb-vbus-xiao-backbone", "0"),
    stable_uuid("segment", "usb-vbus-xiao-backbone", "1"),
    stable_uuid("segment", "usb-vbus-xiao-backbone", "2"),
    stable_uuid("segment", "bq-pmid-cap-bank-bus", "2"),
    stable_uuid("segment", "bq-pmid-c213-stub", "0"),
    stable_uuid("via", "usb-vbus-q3-via"),
    stable_uuid("via", "solar-protected-u4-via"),
    stable_uuid("via", "solar-protected-q1-via"),
    stable_uuid("segment", "q2-solar-selector-common-local", "0"),
    stable_uuid("segment", "q2-solar-selector-common-local", "1"),
    stable_uuid("segment", "q2-solar-selector-common-local", "2"),
    stable_uuid("segment", "q3-usb-selector-common-local", "0"),
    stable_uuid("segment", "q3-usb-selector-common-local", "1"),
    stable_uuid("segment", "q3-usb-selector-common-local", "2"),
    stable_uuid("segment", "bq-vbus-q2-left-drain-loop", "0"),
    stable_uuid("segment", "bq-vbus-q2-left-drain-loop", "1"),
    stable_uuid("segment", "bq-vbus-q2-left-drain-loop", "2"),
    stable_uuid("segment", "bq-vbus-q2-left-drain-loop", "3"),
    stable_uuid("segment", "bq-vbus-q3-left-drain-loop", "0"),
    stable_uuid("segment", "bq-vbus-q3-left-drain-loop", "1"),
    stable_uuid("segment", "bq-vbus-q3-left-drain-loop", "2"),
    stable_uuid("segment", "bq-vbus-q3-left-drain-loop", "3"),
    stable_uuid("segment", "q2-acdrv1-backbone", "0"),
    stable_uuid("segment", "q2-acdrv1-backbone", "1"),
    stable_uuid("segment", "q2-acdrv1-backbone", "2"),
    stable_uuid("segment", "q2-acdrv1-u1-fanout", "0"),
    stable_uuid("segment", "q2-acdrv1-u1-fanout", "1"),
    stable_uuid("segment", "q2-acdrv1-u1-fanout", "2"),
    stable_uuid("segment", "q3-acdrv2-backbone", "0"),
    stable_uuid("segment", "q3-acdrv2-backbone", "1"),
    stable_uuid("segment", "q3-acdrv2-backbone", "2"),
    stable_uuid("segment", "q3-acdrv2-u1-fanout", "0"),
    stable_uuid("segment", "q3-acdrv2-u1-fanout", "1"),
    stable_uuid("segment", "q3-acdrv2-u1-fanout", "2"),
    stable_uuid("segment", "solar-raw-xt30-to-fuse", "2"),
    stable_uuid("via", "q2-acdrv1-u1-via"),
    stable_uuid("via", "q2-acdrv1-gate-via"),
    stable_uuid("via", "q3-acdrv2-u1-via"),
    stable_uuid("via", "q3-acdrv2-gate-via"),
    stable_uuid("via", "solar-prot-gate-u4-via"),
    stable_uuid("via", "solar-prot-gate-q1-via"),
    stable_uuid("via", "r204-3v3-via"),
    stable_uuid("via", "r204-3v3-spine-via"),
    stable_uuid("via", "batp-kelvin-r202-via"),
    stable_uuid("via", "batp-kelvin-u1-via"),
    stable_uuid("segment", "boost-en-u3-via-fanout", "0"),
    stable_uuid("segment", "boost-en-u3-via-fanout", "1"),
    stable_uuid("segment", "boost-en-u3-via-fanout", "2"),
    stable_uuid("segment", "boost-en-xiao-backbone", "0"),
    stable_uuid("segment", "boost-en-xiao-backbone", "1"),
    stable_uuid("segment", "boost-en-xiao-backbone", "2"),
    stable_uuid("segment", "boost-en-xiao-backbone", "3"),
    stable_uuid("segment", "boost-en-r405-link", "0"),
    stable_uuid("segment", "boost-en-r405-link", "1"),
    stable_uuid("segment", "boost-en-r405-link", "2"),
    stable_uuid("segment", "boost-en-r405-ground", "0"),
    stable_uuid("segment", "boost-en-local-pulldown", "0"),
    stable_uuid("segment", "boost-en-pulldown-ground", "0"),
    stable_uuid("segment", "u3-boost-en-pulldown-local", "0"),
    stable_uuid("segment", "bq-ts-u1-to-r200-local", "0"),
    stable_uuid("segment", "u1-regn-ilim-local", "0"),
    stable_uuid("segment", "u1-regn-ilim-local", "1"),
    stable_uuid("segment", "u1-regn-ilim-local", "2"),
    stable_uuid("segment", "u1-regn-ilim-local", "3"),
    stable_uuid("segment", "u1-regn-ilim-local", "4"),
    stable_uuid("segment", "u1-regn-ilim-left-fanout", "0"),
    stable_uuid("segment", "u1-regn-ilim-bottom", "0"),
    stable_uuid("segment", "u1-regn-ilim-bottom", "1"),
    stable_uuid("segment", "u1-regn-ilim-bottom", "2"),
    stable_uuid("segment", "u1-regn-ilim-right-fanout", "0"),
    stable_uuid("segment", "u1-regn-ilim-clear-local", "0"),
    stable_uuid("segment", "u1-regn-ilim-clear-local", "1"),
    stable_uuid("segment", "u1-regn-ilim-clear-local", "2"),
    stable_uuid("segment", "u1-regn-ilim-clear-local", "3"),
    stable_uuid("segment", "u1-regn-ilim-clear-local", "4"),
    stable_uuid("segment", "protection-gnd-local", "0"),
    stable_uuid("segment", "protection-gnd-local", "1"),
    stable_uuid("segment", "protection-gnd-local", "2"),
    stable_uuid("segment", "protection-gnd-r102-fanout", "0"),
    stable_uuid("segment", "protection-gnd-bottom", "0"),
    stable_uuid("segment", "protection-gnd-r405-fanout", "0"),
    stable_uuid("via", "j6-3v3-via"),
    stable_uuid("via", "j6-gnd-via"),
    stable_uuid("via", "j6-sda-via"),
    stable_uuid("via", "j6-scl-via"),
    stable_uuid("via", "boost-en-xiao-via"),
    stable_uuid("via", "boost-en-r405-gnd-via"),
    stable_uuid("via", "boost-en-pulldown-gnd-via"),
    stable_uuid("via", "u1-regn-ilim-left-via"),
    stable_uuid("via", "u1-regn-ilim-right-via"),
    stable_uuid("via", "protection-gnd-via"),
    stable_uuid("via", "protection-gnd-r102-via"),
    stable_uuid("via", "protection-gnd-r405-via"),
    stable_uuid("via", "e22-sck-via"),
    stable_uuid("via", "e22-miso-via"),
    stable_uuid("via", "e22-mosi-via"),
}


def generated_uuids() -> set[str]:
    ids: set[str] = set()
    for route in SEGMENTS:
        points = route["points"]
        for index in range(len(points) - 1):
            ids.add(stable_uuid("segment", str(route["name"]), str(index)))
    for via in VIAS:
        ids.add(stable_uuid("via", str(via["name"])))
    ids.update(uuid for _, _, uuid in GROUND_ZONES)
    ids.update(RETIRED_GENERATED_UUIDS)
    return ids


def remove_generated_routes(text: str) -> str:
    ids = generated_uuids()
    result: list[str] = []
    idx = 0
    pattern = re.compile(r"\n[ \t]*\((segment|via|zone)\b")
    while True:
        match = pattern.search(text, idx)
        if not match:
            result.append(text[idx:])
            break
        start = match.start()
        result.append(text[idx:start])
        depth = 0
        end = start + 1
        while end < len(text):
            char = text[end]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    end += 1
                    break
            end += 1
        block = text[start:end]
        uuid_match = re.search(r'\(uuid "([^"]+)"\)', block)
        if not uuid_match or uuid_match.group(1) not in ids:
            result.append(block)
        idx = end
    return "".join(result)


def segment_block(name: str, index: int, net: str, layer: str, width: float, start: tuple[float, float], end: tuple[float, float]) -> str:
    return (
        f'  (segment\n'
        f'    (start {start[0]:.2f} {start[1]:.2f})\n'
        f'    (end {end[0]:.2f} {end[1]:.2f})\n'
        f'    (width {width:.2f})\n'
        f'    (layer "{layer}")\n'
        f'    (net "{net}")\n'
        f'    (uuid "{stable_uuid("segment", name, str(index))}")\n'
        f'  )'
    )


def via_block(name: str, net: str, at: tuple[float, float]) -> str:
    return (
        f'  (via\n'
        f'    (at {at[0]:.2f} {at[1]:.2f})\n'
        f'    (size 0.60)\n'
        f'    (drill 0.30)\n'
        f'    (layers "F.Cu" "B.Cu")\n'
        f'    (net "{net}")\n'
        f'    (uuid "{stable_uuid("via", name)}")\n'
        f'  )'
    )


def ground_zone_block(layer: str, name: str, zone_uuid: str) -> str:
    return (
        f'  (zone\n'
        f'    (net 1)\n'
        f'    (net_name "GND")\n'
        f'    (layer "{layer}")\n'
        f'    (uuid "{zone_uuid}")\n'
        f'    (name "{name}")\n'
        f'    (hatch edge 0.50)\n'
        f'    (connect_pads\n'
        f'      (clearance 0.15)\n'
        f'    )\n'
        f'    (min_thickness 0.20)\n'
        f'    (filled_areas_thickness no)\n'
        f'    (fill\n'
        f'      (thermal_gap 0.50)\n'
        f'      (thermal_bridge_width 0.50)\n'
        f'    )\n'
        f'    (polygon\n'
        f'      (pts\n'
        f'        (xy 20.50 20.50) (xy 104.50 20.50) (xy 104.50 94.50) (xy 20.50 94.50)\n'
        f'      )\n'
        f'    )\n'
        f'  )'
    )


def generated_blocks() -> str:
    blocks: list[str] = []
    for route in SEGMENTS:
        points = route["points"]
        for index, (start, end) in enumerate(zip(points, points[1:])):
            blocks.append(
                segment_block(
                    str(route["name"]),
                    index,
                    str(route["net"]),
                    str(route["layer"]),
                    float(route["width"]),
                    start,  # type: ignore[arg-type]
                    end,  # type: ignore[arg-type]
                )
            )
    for via in VIAS:
        blocks.append(via_block(str(via["name"]), str(via["net"]), via["at"]))  # type: ignore[arg-type]
    for layer, name, zone_uuid in GROUND_ZONES:
        blocks.append(ground_zone_block(layer, name, zone_uuid))
    return "\n".join(blocks)


def main() -> None:
    text = remove_generated_routes(PCB.read_text(encoding="utf-8")).rstrip()
    if not text.endswith(")"):
        raise SystemExit("PCB file does not end with a closing S-expression")
    body = text[:-1].rstrip()
    PCB.write_text(f"{body}\n{generated_blocks()}\n)\n", encoding="utf-8")
    print("Generated initial routes, E22 control/SPI/VCC, TPS61088 local output/SW pins, charge LED/STAT, temp/UV/OV-divider, U1/U2/Q-gate/MOSFET-drain local links and top/L2 ground pours")


if __name__ == "__main__":
    main()
