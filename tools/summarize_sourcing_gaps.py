#!/usr/bin/env python3
"""Summarize current Rev A BOM sourcing gaps."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "bom/REV_A_LOCKED_CORE_BOM.csv"
PASSIVES = ROOT / "bom/REV_A_LOCKED_PASSIVES.csv"
OUT = ROOT / "docs/SOURCING_GAPS_REV_A.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_gap(value: str) -> bool:
    return value.strip().upper() in {"", "TBD"}


def table(rows: list[list[str]]) -> list[str]:
    if not rows:
        return ["None."]
    lines = ["| Area | Ref/group | Value/part | Missing | Notes |", "|---|---|---|---|---|"]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("|", "/") for cell in row) + " |")
    return lines


def main() -> None:
    gap_rows: list[list[str]] = []

    for row in read_csv(CORE):
        missing: list[str] = []
        if is_gap(row["Manufacturer"]):
            missing.append("manufacturer")
        if is_gap(row["Manufacturer Part Number"]):
            missing.append("MPN")
        if row["Status"] in {"selected_class", "locked_candidate"}:
            missing.append(f"status {row['Status']}")
        if missing:
            gap_rows.append(
                [
                    "core",
                    row["Reference"],
                    row["Description"],
                    ", ".join(missing),
                    row["Assembly Notes"],
                ]
            )

    for row in read_csv(PASSIVES):
        missing: list[str] = []
        if is_gap(row["Manufacturer"]):
            missing.append("manufacturer")
        if is_gap(row["Manufacturer Part Number"]):
            missing.append("MPN")
        if row["Status"] in {"locked_candidate_value", "locked_value"}:
            missing.append(f"status {row['Status']}")
        if row["Quantity"].strip().upper() == "TBD":
            missing.append("quantity")
        if missing:
            gap_rows.append(
                [
                    "passive",
                    row["Reference"],
                    row["Value"],
                    ", ".join(missing),
                    row["Assembly Notes"],
                ]
            )

    lines = [
        "# RoyalNode Rev A Sourcing Gaps",
        "",
        "Generated from `bom/REV_A_LOCKED_CORE_BOM.csv` and `bom/REV_A_LOCKED_PASSIVES.csv`.",
        "",
        "This report tracks ordering friction only. It does not change the electrical design.",
        "",
        *table(gap_rows),
        "",
        "Resolve these gaps before requesting a real PCBA quote. Values marked as locked still need exact stocked manufacturer parts when the manufacturer and MPN are `TBD`.",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(gap_rows)} gap rows")


if __name__ == "__main__":
    main()
