#!/usr/bin/env python3
"""Check KiCad ERC/DRC reports against the current RoyalNode Rev A milestone."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERC = ROOT / "hardware/fabrication/RoyalNode_erc.rpt"
DRC = ROOT / "hardware/fabrication/RoyalNode_drc.rpt"

EXPECTED_FOOTPRINT_WARNINGS = {
    "MOD2": "MOD2_E22_900M33S_JLC_C22399506_RC",
    "U3": "U3_TPS61088_RHL0020A_THERMALVIAS_RC",
    "L2": "L2_COILCRAFT_XAL7030_222MEC_RC",
}
EXPECTED_DRC_TAGS = ["lib_footprint_mismatch"] * len(EXPECTED_FOOTPRINT_WARNINGS)
EXPECTED_UNCONNECTED = 51


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing report: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def check_erc(text: str) -> None:
    if not re.search(r"ERC messages:\s+0\s+Errors\s+0\s+Warnings\s+0", text):
        fail("ERC report is not clean")


def check_drc(text: str) -> None:
    found = re.search(r"\*\* Found (\d+) DRC violations \*\*", text)
    if not found:
        fail("DRC report missing violation count")
    violation_count = int(found.group(1))

    main_section = text.split("** Found", 2)[1]
    tags = re.findall(r"^\[([^\]]+)\]:", main_section, flags=re.M)
    if tags != EXPECTED_DRC_TAGS:
        fail(f"unexpected DRC tags before unrouted list: {tags}")
    if violation_count != len(EXPECTED_DRC_TAGS):
        fail(f"expected {len(EXPECTED_DRC_TAGS)} DRC violations, found {violation_count}")
    for ref, footprint in EXPECTED_FOOTPRINT_WARNINGS.items():
        if f"Footprint {ref}" not in text or footprint not in text:
            fail(f"known {ref} footprint warning is missing or changed")

    unconnected = re.search(r"\*\* Found (\d+) unconnected pads \*\*", text)
    if not unconnected:
        fail("DRC report missing unconnected-pad count")
    unconnected_count = int(unconnected.group(1))
    if unconnected_count != EXPECTED_UNCONNECTED:
        fail(f"expected {EXPECTED_UNCONNECTED} unconnected pads, found {unconnected_count}")


def main() -> None:
    check_erc(read(ERC))
    check_drc(read(DRC))
    print("KiCad report check passed")
    print("  ERC: 0 errors, 0 warnings")
    refs = ", ".join(EXPECTED_FOOTPRINT_WARNINGS)
    print(f"  DRC: expected {len(EXPECTED_DRC_TAGS)} known footprint warnings ({refs})")
    print(f"  Unconnected pads: {EXPECTED_UNCONNECTED}")


if __name__ == "__main__":
    main()
