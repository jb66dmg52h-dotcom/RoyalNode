#!/usr/bin/env python3
"""Lightweight consistency checks for the RoyalNode hardware repo."""

from __future__ import annotations

import csv
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
        "Molex 5037630291": "Rev A NTC connector is CJT A2012WV-S-2P",
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
        "RN_JST_PH_2",
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


def main() -> None:
    core_rows = check_csv("bom/REV_A_LOCKED_CORE_BOM.csv")
    passive_rows = check_csv("bom/REV_A_LOCKED_PASSIVES.csv")
    seed_rows = check_csv("hardware/kicad/RoyalNode/SCHEMATIC_CAPTURE_SEED_REV_A.csv")

    check_required_refs(
        core_rows,
        {"MOD1", "MOD2", "U1", "U2", "U3", "U4", "Q1", "Q2", "Q3", "J1", "J2", "J3", "J4", "J5", "L1", "L2", "F1", "TH1", "D1"},
        "bom/REV_A_LOCKED_CORE_BOM.csv",
    )
    if len(passive_rows) < 25:
        fail("locked passive BOM has unexpectedly few rows")
    check_no_stale_design_terms()
    check_symbols()
    check_footprint_source_links()
    check_draft_envelope_footprints()
    check_e22_manual_draft_footprint()
    check_e22_assembler_crosscheck()
    check_capture_seed(seed_rows)

    print("RoyalNode validation passed")
    print(f"  core BOM rows: {len(core_rows)}")
    print(f"  passive BOM rows: {len(passive_rows)}")
    print(f"  schematic capture seed rows: {len(seed_rows)}")


if __name__ == "__main__":
    main()
