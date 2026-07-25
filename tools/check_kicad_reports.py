#!/usr/bin/env python3
"""Check KiCad ERC/DRC reports against the current RoyalNode Rev A milestone."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERC = ROOT / "hardware/fabrication/RoyalNode_erc.rpt"
DRC = ROOT / "hardware/fabrication/RoyalNode_drc.rpt"

EXPECTED_DRC_TAGS = ["lib_footprint_mismatch"]
EXPECTED_UNCONNECTED = 145


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
        fail(f"expected {len(EXPECTED_DRC_TAGS)} DRC violation, found {violation_count}")
    if "Footprint MOD2" not in text or "MOD2_E22_900M33S_JLC_C22399506_RC" not in text:
        fail("known MOD2 footprint warning is missing or changed")

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
    print(f"  DRC: expected {len(EXPECTED_DRC_TAGS)} known warning")
    print(f"  Unconnected pads: {EXPECTED_UNCONNECTED}")


if __name__ == "__main__":
    main()
