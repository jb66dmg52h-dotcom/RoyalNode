#!/usr/bin/env python3
"""Lightweight consistency checks for the RoyalNode hardware repo."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def check_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.reader(handle) if any(cell.strip() for cell in row)]
    if not rows:
        fail(f"{path} is empty")
    widths = {len(row) for row in rows}
    if len(widths) != 1:
        fail(f"{path} has inconsistent column counts: {sorted(widths)}")
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if any((cell or "").strip() for cell in row.values())]


def check_required_refs(rows: list[dict[str, str]], required: set[str], path: str) -> None:
    refs = {row["Reference"] for row in rows}
    missing = sorted(required - refs)
    if missing:
        fail(f"{path} missing references: {', '.join(missing)}")


def check_no_stale_design_terms() -> None:
    stale_terms = {
        "MAX17048": "Rev A removed the dedicated fuel gauge",
        "SWD service": "Rev A removed the SWD connector",
        "Molex 5037630291": "Rev A NTC connector is JST-GH SM02B-GHS-TB",
        "JST-PH": "Rev A standardized low-current JST connectors on JST-GH",
        "CJT A2012": "Rev A standardized the battery NTC connector on JST-GH",
        "JST-PH 4-pin": "Rev A has no 4-pin debug/programming JST harness",
        "GPS": "Rev A removed GPS",
        "display": "Rev A removed display hardware",
        "fan connector": "Rev A removed fan/accessory connector",
    }
    current_files = [
        "docs/DESIGN_FREEZE_REV_A.md",
        "docs/FOOTPRINT_AUDIT_REV_A.md",
        "docs/KICAD_SYMBOL_AUDIT_REV_A.md",
        "docs/FOOTPRINT_SOURCE_LINKS_REV_A.md",
        "docs/MOLEX_SMA_FOOTPRINT_BLOCKER_REV_A.md",
        "docs/E22_ASSEMBLER_FOOTPRINT_CROSSCHECK_REV_A.md",
        "docs/PCB_PLACEMENT_STATUS_REV_A.md",
        "docs/REFERENCE_DESIGNATORS_REV_A.md",
        "hardware/kicad/RoyalNode/SCHEMATIC_CAPTURE_SEED_REV_A.csv",
        "bom/REV_A_LOCKED_CORE_BOM.csv",
        "bom/REV_A_LOCKED_PASSIVES.csv",
    ]
    for rel in current_files:
        lines = read(rel).splitlines()
        in_removed_section = False
        for term, reason in stale_terms.items():
            for lineno, line in enumerate(lines, start=1):
                if line.startswith("## "):
                    in_removed_section = "removed" in line.lower()
                if term.lower() not in line.lower():
                    continue
                if in_removed_section:
                    continue
                if re.search(r"\b(removed|no |not |without|excludes?|prohibit)", line, re.I):
                    continue
                fail(f"stale term {term!r} found in {rel}:{lineno}: {reason}")


def check_symbols() -> None:
    sym = read("hardware/kicad/RoyalNode/lib_symbols/RoyalNode.kicad_sym")
    required_symbols = [
        "RN_XIAO_nRF52840_SOCKET",
        "RN_E22_900M33S",
        "RN_BQ25798RQMR",
        "RN_TPS61088RHLR",
        "RN_LM66100DCKR",
        "RN_LTC4365ITS8_1",
        "RN_ISA170170N04LMDS",
        "RN_XT30PW_M",
        "RN_SMA_EDGE",
        "RN_JST_GH_2",
        "RN_JST_GH_4",
        "RN_TWO_PIN_POWER_PART",
        "RN_PWR_FLAG",
    ]
    for name in required_symbols:
        if f'(symbol "{name}"' not in sym:
            fail(f"missing KiCad symbol {name}")
    if '(pin power_in line' not in sym:
        fail("symbol library appears malformed: no power pins found")


def check_footprint_source_links() -> None:
    text = read("docs/FOOTPRINT_SOURCE_LINKS_REV_A.md")
    required = [
        "https://www.cdebyte.com/pdf-down.aspx?id=4216",
        "C22399506",
        "E22_ASSEMBLER_FOOTPRINT_CROSSCHECK_REV_A.md",
        "https://www.molex.com/en-us/products/part-detail/732511150",
        "Sales Drawing SD-73251-115-001",
        "DRAFT_NOT_RELEASED",
    ]
    for needle in required:
        if needle not in text:
            fail(f"footprint source links missing {needle!r}")
    blocker = read("docs/MOLEX_SMA_FOOTPRINT_BLOCKER_REV_A.md")
    for needle in ["Sales Drawing SD-73251-115-001", "no electrical pads", "not sufficient to create the PCB launch"]:
        if needle not in blocker:
            fail(f"Molex SMA blocker missing {needle!r}")


def check_draft_envelope_footprints() -> None:
    fp_dir = ROOT / "hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty"
    draft_files = sorted(fp_dir.glob("*DRAFT_ENVELOPE.kicad_mod"))
    if len(draft_files) < 4:
        fail("expected at least four DRAFT_ENVELOPE planning footprints")
    for path in draft_files:
        text = path.read_text(encoding="utf-8")
        if "DRAFT_NOT_RELEASED" not in text:
            fail(f"{path.relative_to(ROOT)} missing DRAFT_NOT_RELEASED marker")
        if re.search(r"^\s*\(pad\b", text, re.M):
            fail(f"{path.relative_to(ROOT)} is an envelope footprint but contains pads")


def check_e22_manual_draft_footprint() -> None:
    path = ROOT / "hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD2_E22_900M33S_EBYTE_MANUAL_DRAFT.kicad_mod"
    if not path.exists():
        fail("missing E22 manual-draft footprint")
    text = path.read_text(encoding="utf-8")
    if "NOT_RELEASED" not in text:
        fail("E22 manual-draft footprint must remain marked NOT_RELEASED")
    pad_count = len(re.findall(r"^\s*\(pad\s+\"", text, re.M))
    if pad_count != 22:
        fail(f"E22 manual-draft footprint should have 22 pads, found {pad_count}")
    if '(pad "21" smd rect' not in text:
        fail("E22 manual-draft footprint missing ANT pad 21")
    audit = read("docs/E22_FOOTPRINT_TRANSCRIPTION_REV_A.md")
    for needle in ["Pin 21", "ANT", "C22399506", "E22_ASSEMBLER_FOOTPRINT_CROSSCHECK_REV_A.md"]:
        if needle not in audit:
            fail(f"E22 footprint transcription audit missing {needle!r}")


def check_e22_assembler_crosscheck() -> None:
    fp_path = ROOT / "hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD2_E22_900M33S_JLC_C22399506_IMPORT_RC.kicad_mod"
    if not fp_path.exists():
        fail("missing E22 JLC/LCSC C22399506 import release-candidate footprint")
    text = fp_path.read_text(encoding="utf-8")
    for needle in ["NOT_RELEASED", "C22399506", "MOD2_E22_900M33S_JLC_C22399506_IMPORT_RC"]:
        if needle not in text:
            fail(f"E22 JLC import footprint missing {needle!r}")
    pad_count = len(re.findall(r"^\s*\(pad\s+\"?\d+\"?\s+smd\s+rect", text, re.M))
    if pad_count != 22:
        fail(f"E22 JLC import footprint should have 22 pads, found {pad_count}")
    if not re.search(r"^\s*\(pad\s+\"?21\"?\s+smd\s+rect", text, re.M):
        fail("E22 JLC import footprint missing ANT pad 21")

    crosscheck = read("docs/E22_ASSEMBLER_FOOTPRINT_CROSSCHECK_REV_A.md")
    required = [
        "C22399506",
        "JLCPCB",
        "LCSC",
        "EasyEDA",
        "1.50 x 2.20 mm",
        "first article",
        "factory-installed",
        "first Rev A PCB",
    ]
    for needle in required:
        if needle not in crosscheck:
            fail(f"E22 assembler cross-check missing {needle!r}")


def check_e22_native_rc_footprint() -> None:
    fp_path = ROOT / "hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty/MOD2_E22_900M33S_JLC_C22399506_RC.kicad_mod"
    if not fp_path.exists():
        fail("missing KiCad-10-native E22 C22399506 release-candidate footprint")
    text = fp_path.read_text(encoding="utf-8")
    for needle in [
        "MOD2_E22_900M33S_JLC_C22399506_RC",
        "NOT_RELEASED_RELEASE_CANDIDATE",
        "C22399506",
        "ANT pin 21",
    ]:
        if needle not in text:
            fail(f"E22 native release-candidate footprint missing {needle!r}")
    pad_count = len(re.findall(r"^\s*\(pad\s+\"?\d+\"?\s+smd\s+rect", text, re.M))
    if pad_count != 22:
        fail(f"E22 native release-candidate footprint should have 22 pads, found {pad_count}")
    if not re.search(r"^\s*\(pad\s+\"?21\"?\s+smd\s+rect", text, re.M):
        fail("E22 native release-candidate footprint missing ANT pad 21")


def check_connector_rc_footprints() -> None:
    fp_dir = ROOT / "hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty"
    checks = [
        (
            fp_dir / "J_POWER_XT30PW_M_C431092_RC.kicad_mod",
            ["J_POWER_XT30PW_M_C431092_RC", "C431092", "NOT_RELEASED_RELEASE_CANDIDATE"],
            4,
        ),
        (
            fp_dir / "J_LOW_JST_GH_SM02B_GHS_TB_RC.kicad_mod",
            ["J_LOW_JST_GH_SM02B_GHS_TB_RC", "SM02B-GHS-TB", "NOT_RELEASED_RELEASE_CANDIDATE"],
            4,
        ),
        (
            fp_dir / "J_LOW_JST_GH_SM04B_GHS_TB_RC.kicad_mod",
            ["J_LOW_JST_GH_SM04B_GHS_TB_RC", "SM04B-GHS-TB", "NOT_RELEASED_RELEASE_CANDIDATE"],
            6,
        ),
        (
            fp_dir / "MOD1_XIAO_SOCKET_1X7_C53202181_RC.kicad_mod",
            ["MOD1_XIAO_SOCKET_1X7_C53202181_RC", "C53202181", "NOT_RELEASED_RELEASE_CANDIDATE"],
            7,
        ),
        (
            fp_dir / "MOD1_XIAO_NRF52840_SOCKET_C53202181_RC.kicad_mod",
            ["MOD1_XIAO_NRF52840_SOCKET_C53202181_RC", "C53202181 x2", "17.78 mm row spacing"],
            14,
        ),
        (
            fp_dir / "J5_SMA_MOLEX_732511150_C841205_IMPORT_RC.kicad_mod",
            ["J5_SMA_MOLEX_732511150_C841205_IMPORT_RC", "C841205", "Edge.Cuts"],
            5,
        ),
    ]
    for path, needles, expected_pad_count in checks:
        if not path.exists():
            fail(f"missing release-candidate connector footprint {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                fail(f"{path.relative_to(ROOT)} missing {needle!r}")
        pad_count = len(re.findall(r"^\s*\(pad\s+\"", text, re.M))
        if pad_count != expected_pad_count:
            fail(f"{path.relative_to(ROOT)} expected {expected_pad_count} pads, found {pad_count}")


def check_power_rc_footprints() -> None:
    fp_dir = ROOT / "hardware/kicad/RoyalNode/lib_footprints/RoyalNode.pretty"
    checks = [
        ("U1_BQ25798_RQM0029A_RC.kicad_mod", ["BQ25798", "RQM0029A", "NOT_RELEASED_RELEASE_CANDIDATE"], 29),
        ("U3_TPS61088_RHL0020A_THERMALVIAS_RC.kicad_mod", ["TPS61088", "RHL", "NOT_RELEASED_RELEASE_CANDIDATE"], 41),
        ("U2_LM66100_DCK0006A_SC70_6_RC.kicad_mod", ["LM66100", "NOT_RELEASED_RELEASE_CANDIDATE"], 6),
        ("U4_LTC4365_TSOT23_8_RC.kicad_mod", ["LTC4365", "NOT_RELEASED_RELEASE_CANDIDATE"], 8),
        ("Q_POWER_INFINEON_PG_DSO_8_27_RC.kicad_mod", ["Infineon", "PG-DSO-8-27", "NOT_RELEASED_RELEASE_CANDIDATE"], 23),
        ("L1_COILCRAFT_XAL7070_222MEC_RC.kicad_mod", ["XAL7070-222MEC", "NOT_RELEASED_RELEASE_CANDIDATE"], 2),
        ("L2_COILCRAFT_XAL7030_222MEC_RC.kicad_mod", ["XAL7030-222MEC", "NOT_RELEASED_RELEASE_CANDIDATE"], 2),
        ("F1_LITTELFUSE_483_1206_RC.kicad_mod", ["Littelfuse 483", "NOT_RELEASED_RELEASE_CANDIDATE"], 2),
        ("C503_PANASONIC_10SVPC330M_8X6P9_RC.kicad_mod", ["Panasonic 10SVPC330M", "pad 1 positive", "NOT_RELEASED_RELEASE_CANDIDATE"], 2),
    ]
    for filename, needles, expected_pad_count in checks:
        path = fp_dir / filename
        if not path.exists():
            fail(f"missing release-candidate power footprint {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                fail(f"{path.relative_to(ROOT)} missing {needle!r}")
        pad_count = len(re.findall(r"^\s*\(pad\s+\"", text, re.M))
        if pad_count != expected_pad_count:
            fail(f"{path.relative_to(ROOT)} expected {expected_pad_count} pads, found {pad_count}")


def check_generated_pcb_placement() -> None:
    generator = read("tools/generate_pcb_placement.py")
    required_generator_terms = [
        "MOD2_E22_900M33S_JLC_C22399506_RC.kicad_mod",
        "MOD1_XIAO_NRF52840_SOCKET_C53202181_RC.kicad_mod",
        "J5_SMA_0732511150_DRAFT_ENVELOPE.kicad_mod",
        "J_POWER_XT30PW_M_C431092_RC.kicad_mod",
        "J_LOW_JST_GH_SM02B_GHS_TB_RC.kicad_mod",
        "J_LOW_JST_GH_SM04B_GHS_TB_RC.kicad_mod",
        "U1_BQ25798_RQM0029A_RC.kicad_mod",
        "U3_TPS61088_RHL0020A_THERMALVIAS_RC.kicad_mod",
        "Q_POWER_INFINEON_PG_DSO_8_27_RC.kicad_mod",
        "F1_LITTELFUSE_483_1206_RC.kicad_mod",
        "factory-installed PCBA item",
    ]
    for needle in required_generator_terms:
        if needle not in generator:
            fail(f"PCB placement generator missing {needle!r}")

    pcb = read("hardware/kicad/RoyalNode/RoyalNode.kicad_pcb")
    required_placements = {
        "MOD2": "RoyalNode:MOD2_E22_900M33S_JLC_C22399506_RC",
        "MOD1": "RoyalNode:MOD1_XIAO_NRF52840_SOCKET_C53202181_RC",
        "J5": "RoyalNode:J5_SMA_0732511150_DRAFT_ENVELOPE",
        "J1": "RoyalNode:J_POWER_XT30PW_M_C431092_RC",
        "J2": "RoyalNode:J_POWER_XT30PW_M_C431092_RC",
        "J3": "RoyalNode:J_LOW_JST_GH_SM02B_GHS_TB_RC",
        "J4": "RoyalNode:J_LOW_JST_GH_SM02B_GHS_TB_RC",
        "J6": "RoyalNode:J_LOW_JST_GH_SM04B_GHS_TB_RC",
        "U1": "RoyalNode:U1_BQ25798_RQM0029A_RC",
        "L1": "RoyalNode:L1_COILCRAFT_XAL7070_222MEC_RC",
        "U3": "RoyalNode:U3_TPS61088_RHL0020A_THERMALVIAS_RC",
        "L2": "RoyalNode:L2_COILCRAFT_XAL7030_222MEC_RC",
        "U2": "RoyalNode:U2_LM66100_DCK0006A_SC70_6_RC",
        "U4": "RoyalNode:U4_LTC4365_TSOT23_8_RC",
        "F1": "RoyalNode:F1_LITTELFUSE_483_1206_RC",
        "Q1": "RoyalNode:Q_POWER_INFINEON_PG_DSO_8_27_RC",
        "Q2": "RoyalNode:Q_POWER_INFINEON_PG_DSO_8_27_RC",
        "Q3": "RoyalNode:Q_POWER_INFINEON_PG_DSO_8_27_RC",
    }
    for ref, footprint in required_placements.items():
        if f'(footprint "{footprint}"' not in pcb:
            fail(f"PCB missing generated footprint {footprint}")
        if f'(property "Reference" "{ref}"' not in pcb:
            fail(f"PCB missing generated placement reference {ref}")

    for needle in [
        'gr_text "50 ohm RF corridor',
        'gr_text "E22-900M33S\\nmodule zone"',
        'gr_text "XIAO',
        'gr_text "XT30',
    ]:
        if needle not in pcb:
            fail(f"PCB scaffold missing board planning graphic {needle!r}")

    for net_name in ["GND", "5V_RADIO", "RF_915", "SOLAR_RAW"]:
        if not re.search(rf'\(net\s+"{re.escape(net_name)}"\)', pcb):
            fail(f"PCB scaffold missing generated net annotation {net_name!r}")

    for pinfunction in ["ANT", "PLUS", "SW"]:
        needle = f'(pinfunction "{pinfunction}")'
        if needle not in pcb:
            fail(f"PCB scaffold missing generated pin annotation {needle!r}")

    status = read("docs/PCB_PLACEMENT_STATUS_REV_A.md")
    for needle in [
        "P1a",
        "85 mm x 75 mm",
        "MOD2_E22_900M33S_JLC_C22399506_RC",
        "J_POWER_XT30PW_M_C431092_RC",
        "MOD1_XIAO_NRF52840_SOCKET_C53202181_RC",
        "factory PCBA footprint",
        "lib_footprint_mismatch on MOD2",
        "Do not add test points",
    ]:
        if needle not in status:
            fail(f"PCB placement status missing {needle!r}")


def check_net_classes() -> None:
    project = json.loads(read("hardware/kicad/RoyalNode/RoyalNode.kicad_pro"))
    net_settings = project.get("net_settings", {})
    classes = {item.get("name"): item for item in net_settings.get("classes", [])}
    expected_classes = {
        "Default": {"track_width": 0.2, "clearance": 0.15},
        "HighCurrentPower": {"track_width": 1.5, "clearance": 0.15},
        "RF_50OHM": {"track_width": 0.5, "clearance": 0.25},
        "SwitchNode": {"track_width": 0.8, "clearance": 0.15},
        "SensitiveSense": {"track_width": 0.2, "clearance": 0.15},
    }
    for name, expected_values in expected_classes.items():
        if name not in classes:
            fail(f"missing KiCad net class {name}")
        for key, expected in expected_values.items():
            actual = classes[name].get(key)
            if actual != expected:
                fail(f"net class {name} expected {key}={expected}, found {actual}")

    patterns = {
        (item.get("netclass"), item.get("pattern"))
        for item in net_settings.get("netclass_patterns", [])
    }
    expected_patterns = {
        ("HighCurrentPower", "BAT*"),
        ("HighCurrentPower", "SOLAR*"),
        ("HighCurrentPower", "BQ_VBUS"),
        ("HighCurrentPower", "BQ_SYS"),
        ("HighCurrentPower", "BQ_PMID"),
        ("HighCurrentPower", "5V_RADIO"),
        ("RF_50OHM", "RF_915"),
        ("SwitchNode", "BQ_SW*"),
        ("SwitchNode", "BOOST_SW"),
        ("SensitiveSense", "BATP_KELVIN"),
        ("SensitiveSense", "BQ_TS"),
        ("SensitiveSense", "BOOST_FB"),
        ("SensitiveSense", "BOOST_COMP*"),
        ("SensitiveSense", "UV_NODE"),
        ("SensitiveSense", "OV_NODE"),
    }
    missing = sorted(expected_patterns - patterns)
    if missing:
        fail(f"missing KiCad netclass patterns: {missing}")

    status = read("docs/PCB_PLACEMENT_STATUS_REV_A.md")
    for needle in ["HighCurrentPower", "SwitchNode", "SensitiveSense", "RF_50OHM", "1.5 mm"]:
        if needle not in status:
            fail(f"PCB placement status missing net-class note {needle!r}")

    net_class_doc = read("docs/PCB_NET_CLASSES_REV_A.md")
    for needle in ["HighCurrentPower", "SwitchNode", "SensitiveSense", "RF_50OHM", "JLC04161H-3313"]:
        if needle not in net_class_doc:
            fail(f"PCB net-class doc missing {needle!r}")


def check_initial_routes() -> None:
    route_generator = read("tools/generate_initial_routes.py")
    for needle in [
        "E22_TXEN_DIO2",
        "E22_NRST",
        "E22_DIO1",
        "E22_BUSY",
        "E22_NSS",
        "E22_RXEN",
        "3V3",
        "GND",
        "I2C_SDA",
        "I2C_SCL",
        "j6-3v3-backbone",
        "j6-gnd-backbone",
        "j6-sda-backbone",
        "j6-scl-backbone",
        "e22-nrst-backbone",
        "e22-dio1-backbone",
        "e22-busy-backbone",
        "e22-nss-backbone",
        "e22-rxen-direct",
        "e22-rxen-backbone",
        'net "{net}"',
        "L2_GND_REFERENCE",
    ]:
        if needle not in route_generator:
            fail(f"initial route generator missing {needle!r}")

    makefile = read("Makefile")
    if "generate-routes" not in makefile:
        fail("Makefile missing generate-routes target")
    if "--refill-zones" not in makefile or "--save-board" not in makefile:
        fail("Makefile DRC target must refill and save zones")

    pcb = read("hardware/kicad/RoyalNode/RoyalNode.kicad_pcb")
    for net_name in [
        "GND",
        "3V3",
        "E22_TXEN_DIO2",
        "I2C_SDA",
        "I2C_SCL",
        "E22_NRST",
        "E22_DIO1",
        "E22_BUSY",
        "E22_NSS",
        "E22_RXEN",
    ]:
        if not re.search(rf'\(net\s+"{re.escape(net_name)}"\)', pcb):
            fail(f"PCB missing generated initial route for net {net_name!r}")
    for needle in ['(layer "B.Cu")', '(layer "In2.Cu")', '(via', '(start 30.35 59.08)', '(end 30.35 61.62)', '(layer "In1.Cu")', '(name "L2_GND_REFERENCE")']:
        if needle not in pcb:
            fail(f"PCB missing expected initial route geometry {needle!r}")

    status = read("docs/PCB_PLACEMENT_STATUS_REV_A.md")
    for needle in [
        "Initial Routed Nets",
        "E22_TXEN_DIO2",
        "E22_NRST",
        "E22_DIO1",
        "E22_BUSY",
        "E22_NSS",
        "E22_RXEN",
        "SPI_SCK",
        "SPI_MISO",
        "SPI_MOSI",
        "deferred",
        "I2C_SDA",
        "I2C_SCL",
        "L2_GND_REFERENCE",
    ]:
        if needle not in status:
            fail(f"PCB placement status missing initial-route note {needle!r}")


def check_generated_schematic_footprints() -> None:
    schematic = read("hardware/kicad/RoyalNode/RoyalNode.kicad_sch")
    required_footprints = {
        "MOD1": "RoyalNode:MOD1_XIAO_NRF52840_SOCKET_C53202181_RC",
        "MOD2": "RoyalNode:MOD2_E22_900M33S_JLC_C22399506_RC",
        "U1": "RoyalNode:U1_BQ25798_RQM0029A_RC",
        "U2": "RoyalNode:U2_LM66100_DCK0006A_SC70_6_RC",
        "U3": "RoyalNode:U3_TPS61088_RHL0020A_THERMALVIAS_RC",
        "U4": "RoyalNode:U4_LTC4365_TSOT23_8_RC",
        "Q1": "RoyalNode:Q_POWER_INFINEON_PG_DSO_8_27_RC",
        "Q2": "RoyalNode:Q_POWER_INFINEON_PG_DSO_8_27_RC",
        "Q3": "RoyalNode:Q_POWER_INFINEON_PG_DSO_8_27_RC",
        "J1": "RoyalNode:J_POWER_XT30PW_M_C431092_RC",
        "J2": "RoyalNode:J_POWER_XT30PW_M_C431092_RC",
        "J3": "RoyalNode:J_LOW_JST_GH_SM02B_GHS_TB_RC",
        "J4": "RoyalNode:J_LOW_JST_GH_SM02B_GHS_TB_RC",
        "J6": "RoyalNode:J_LOW_JST_GH_SM04B_GHS_TB_RC",
        "F1": "RoyalNode:F1_LITTELFUSE_483_1206_RC",
        "L1": "RoyalNode:L1_COILCRAFT_XAL7070_222MEC_RC",
        "L2": "RoyalNode:L2_COILCRAFT_XAL7030_222MEC_RC",
    }
    for ref, footprint in required_footprints.items():
        pattern = (
            rf'\(property "Reference" "{re.escape(ref)}".*?'
            rf'\(property "Footprint" "{re.escape(footprint)}"'
        )
        if not re.search(pattern, schematic, re.S):
            fail(f"schematic symbol {ref} missing footprint assignment {footprint}")


def check_passive_footprint_seed(passive_rows: list[dict[str, str]]) -> None:
    required = {
        "R100": "Resistor_SMD:R_0603_1608Metric",
        "R405": "Resistor_SMD:R_0603_1608Metric",
        "D1": "LED_SMD:LED_0603_1608Metric",
        "C200": "Capacitor_SMD:C_1206_3216Metric",
        "C400": "Capacitor_SMD:C_1210_3225Metric",
        "C405": "Capacitor_SMD:C_0805_2012Metric",
        "C406": "Capacitor_SMD:C_0603_1608Metric",
        "C503": "RoyalNode:C503_PANASONIC_10SVPC330M_8X6P9_RC",
        "TH1": "",
    }
    by_ref = {row["Reference"]: row for row in passive_rows}
    if "Footprint" not in passive_rows[0]:
        fail("passive capture seed missing Footprint column")
    for ref, footprint in required.items():
        actual = by_ref.get(ref, {}).get("Footprint")
        if actual != footprint:
            fail(f"passive seed {ref} expected footprint {footprint!r}, found {actual!r}")


def check_capture_seed(seed_rows: list[dict[str, str]]) -> None:
    required_nets = {
        "GND",
        "3V3",
        "BAT_RAW",
        "BQ_SYS",
        "5V_RADIO",
        "RF_915",
        "E22_TXEN_DIO2",
        "I2C_SDA",
        "I2C_SCL",
        "SPI_SCK",
        "SPI_MISO",
        "SPI_MOSI",
        "SOLAR_RAW",
        "SOLAR_FUSED",
        "SOLAR_PROTECTED",
        "USB_VBUS_RAW",
    }
    nets = {row["Net"] for row in seed_rows}
    missing = sorted(required_nets - nets)
    if missing:
        fail(f"capture seed missing nets: {', '.join(missing)}")

    for row in seed_rows:
        if row["Net"] == "NC" and not re.search(r"no-connect|floating", row["Notes"], re.I):
            fail(f"NC row lacks explicit no-connect/floating note: {row}")


def check_generated_schematic() -> None:
    generator = read("tools/generate_kicad_capture.py")
    for needle in ["SCHEMATIC_CAPTURE_SEED_REV_A.csv", "PASSIVE_CAPTURE_SEED_REV_A.csv", "RN_TWO_PIN_POWER_PART", "RN_PWR_FLAG", "CAPTURED_ORDER"]:
        if needle not in generator:
            fail(f"KiCad capture generator missing {needle!r}")

    schematic = read("hardware/kicad/RoyalNode/RoyalNode.kicad_sch")
    required_refs = [
        "MOD1",
        "MOD2",
        "U1",
        "U2",
        "U3",
        "U4",
        "Q1",
        "Q2",
        "Q3",
        "J1",
        "J2",
        "J3",
        "J4",
        "J5",
        "J6",
        "F1",
        "L1",
        "L2",
        "R100",
        "R101",
        "R102",
        "R103",
        "D1",
        "R207",
        "TH1",
        "PF1",
        "PF6",
    ]
    for ref in required_refs:
        if f'(property "Reference" "{ref}"' not in schematic:
            fail(f"generated schematic missing reference {ref}")
    for net in ["E22_TXEN_DIO2", "RF_915", "5V_RADIO", "SOLAR_RAW", "BAT_RAW", "BQ_SW1", "BQ_SW2", "BOOST_SW", "UV_NODE", "OV_NODE", "LTC_SHDN", "CHG_LED_K"]:
        if f'(global_label "{net}"' not in schematic:
            fail(f"generated schematic missing net label {net}")
    if 'Generated from SCHEMATIC_CAPTURE_SEED_REV_A.csv' not in schematic:
        fail("schematic title block no longer records the capture seed")
    if not re.search(r'\(on_board no\).*?\(property "Reference" "TH1"', schematic, re.S):
        fail("TH1 must remain an off-board battery-mounted thermistor with on_board no")

    status = read("docs/KICAD_CAPTURE_STATUS_REV_A.md")
    for needle in ["K1d", "Footprint Assignment Status", "0 messages", "52 support passive", "6 ERC-only power flags", "Do not add test points"]:
        if needle not in status:
            fail(f"KiCad capture status missing {needle!r}")


def main() -> None:
    core_rows = check_csv("bom/REV_A_LOCKED_CORE_BOM.csv")
    locked_passive_rows = check_csv("bom/REV_A_LOCKED_PASSIVES.csv")
    seed_rows = check_csv("hardware/kicad/RoyalNode/SCHEMATIC_CAPTURE_SEED_REV_A.csv")
    capture_passive_rows = check_csv("hardware/kicad/RoyalNode/PASSIVE_CAPTURE_SEED_REV_A.csv")

    check_required_refs(
        core_rows,
        {"MOD1", "MOD2", "U1", "U2", "U3", "U4", "Q1", "Q2", "Q3", "J1", "J2", "J3", "J4", "J5", "J6", "L1", "L2", "F1", "TH1", "D1"},
        "bom/REV_A_LOCKED_CORE_BOM.csv",
    )
    if len(locked_passive_rows) < 25:
        fail("locked passive BOM has unexpectedly few rows")
    check_no_stale_design_terms()
    check_symbols()
    check_footprint_source_links()
    check_draft_envelope_footprints()
    check_e22_manual_draft_footprint()
    check_e22_assembler_crosscheck()
    check_e22_native_rc_footprint()
    check_connector_rc_footprints()
    check_power_rc_footprints()
    check_capture_seed(seed_rows)
    check_passive_footprint_seed(capture_passive_rows)
    check_generated_schematic()
    check_generated_schematic_footprints()
    check_generated_pcb_placement()
    check_net_classes()
    check_initial_routes()

    print("RoyalNode validation passed")
    print(f"  core BOM rows: {len(core_rows)}")
    print(f"  passive BOM rows: {len(locked_passive_rows)}")
    print(f"  schematic capture seed rows: {len(seed_rows)}")
    print(f"  passive capture seed rows: {len(capture_passive_rows)}")


if __name__ == "__main__":
    main()
