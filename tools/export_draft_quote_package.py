#!/usr/bin/env python3
"""Export a non-release KiCad quote package for RoyalNode Rev A.

This produces the file types a PCB/PCBA manufacturer will eventually need,
but it intentionally marks the package as blocked because Rev A still has
unrouted nets and unreleased RF/SMA geometry.
"""

from __future__ import annotations

import os
import csv
import re
import shutil
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "hardware/kicad/RoyalNode"
SCH = PROJECT_DIR / "RoyalNode.kicad_sch"
PCB = PROJECT_DIR / "RoyalNode.kicad_pcb"
OUT = ROOT / "hardware/fabrication/quote_draft_rev_a"
GERBERS = OUT / "gerbers"
DRILL = OUT / "drill"
ASSEMBLY = OUT / "assembly"
REPORTS = OUT / "reports"
KICAD_CLI = Path(os.environ.get("KICAD_CLI", "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"))
CORE_BOM = ROOT / "bom/REV_A_LOCKED_CORE_BOM.csv"
PASSIVE_BOM = ROOT / "bom/REV_A_LOCKED_PASSIVES.csv"
PASSIVE_SEED = PROJECT_DIR / "PASSIVE_CAPTURE_SEED_REV_A.csv"


def run(args: list[str]) -> None:
    print("+", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def zip_dir(source: Path, destination: Path) -> None:
    if destination.exists():
        destination.unlink()
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source.parent))


def write_blocker_note() -> None:
    note = OUT / "READ_ME_NOT_FOR_FABRICATION.txt"
    note.write_text(
        "\n".join(
            [
                "RoyalNode Rev A draft quote package",
                "",
                f"Generated: {datetime.now(timezone.utc).isoformat()}",
                "",
                "This package is for workflow validation and rough manufacturer quoting only.",
                "Do not order boards from this package.",
                "",
                "Known blockers:",
                "- RF_915 is intentionally unrouted.",
                "- J5 is still a draft SMA envelope, not the released Molex edge-launch footprint.",
                "- Final 50 ohm GCPW width/gap still needs JLCPCB stack-up calculation.",
                "- High-current power rails and switching loops are not complete.",
                "- Current KiCad DRC state includes 74 expected unconnected items.",
                "- Current known footprint/library warnings are MOD2, U3 and L2.",
                "",
                "Use `make layout-status` for the current validation gate.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def lcsc_from_notes(notes: str) -> str:
    match = re.search(r"\b(?:JLCPCB\s*)?(C\d+)\b", notes)
    return match.group(1) if match else ""


def write_draft_jlc_bom() -> None:
    """Write a richer quote BOM from the locked sourcing tables.

    The KiCad BOM remains useful as a schematic export. This file is shaped for
    early PCBA sourcing review and keeps unresolved/off-board parts visible.
    """
    core_rows = read_csv(CORE_BOM)
    passive_rows = {row["Reference"]: row for row in read_csv(PASSIVE_BOM)}
    passive_seed = read_csv(PASSIVE_SEED)

    rows: list[dict[str, str]] = []
    for row in core_rows:
        ref = row["Reference"]
        scope = "off-board" if ref == "TH1" else "pcba"
        rows.append(
            {
                "Designator": ref,
                "Qty": row["Quantity"],
                "Comment": row["Description"],
                "Value": row["Manufacturer Part Number"],
                "Footprint": row["Package Or Form"],
                "Manufacturer": row["Manufacturer"],
                "Manufacturer Part Number": row["Manufacturer Part Number"],
                "LCSC Part Number": lcsc_from_notes(row["Assembly Notes"]),
                "Assembly Scope": scope,
                "Status": row["Status"],
                "Notes": row["Assembly Notes"],
            }
        )

    grouped_passives: dict[str, list[dict[str, str]]] = {}
    for row in passive_seed:
        grouped_passives.setdefault(row["Source Group"], []).append(row)

    for group, seed_rows in sorted(grouped_passives.items()):
        locked = passive_rows.get(group)
        if not locked:
            continue
        designators = ",".join(row["Reference"] for row in seed_rows)
        footprint = seed_rows[0]["Footprint"]
        rows.append(
            {
                "Designator": designators,
                "Qty": str(len(seed_rows)),
                "Comment": locked["Description"],
                "Value": locked["Value"],
                "Footprint": footprint,
                "Manufacturer": locked["Manufacturer"],
                "Manufacturer Part Number": locked["Manufacturer Part Number"],
                "LCSC Part Number": lcsc_from_notes(locked["Assembly Notes"]),
                "Assembly Scope": "pcba",
                "Status": locked["Status"],
                "Notes": locked["Assembly Notes"],
            }
        )

    output = ASSEMBLY / "RoyalNode_RevA_JLCPCB_DRAFT_BOM.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "Designator",
            "Qty",
            "Comment",
            "Value",
            "Footprint",
            "Manufacturer",
            "Manufacturer Part Number",
            "LCSC Part Number",
            "Assembly Scope",
            "Status",
            "Notes",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    for directory in [GERBERS, DRILL, ASSEMBLY, REPORTS]:
        directory.mkdir(parents=True, exist_ok=True)

    run(
        [
            str(KICAD_CLI),
            "pcb",
            "export",
            "gerbers",
            "--output",
            str(GERBERS),
            "--layers",
            "F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
            "--check-zones",
            str(PCB),
        ]
    )
    run(
        [
            str(KICAD_CLI),
            "pcb",
            "export",
            "drill",
            "--output",
            str(DRILL),
            "--excellon-units",
            "mm",
            "--generate-map",
            "--map-format",
            "pdf",
            "--generate-report",
            "--report-path",
            str(REPORTS / "RoyalNode_RevA_drill_report.txt"),
            str(PCB),
        ]
    )
    run(
        [
            str(KICAD_CLI),
            "pcb",
            "export",
            "pos",
            "--output",
            str(ASSEMBLY / "RoyalNode_RevA_CPL.csv"),
            "--side",
            "both",
            "--format",
            "csv",
            "--units",
            "mm",
            "--exclude-dnp",
            str(PCB),
        ]
    )
    run(
        [
            str(KICAD_CLI),
            "sch",
            "export",
            "bom",
            "--output",
            str(ASSEMBLY / "RoyalNode_RevA_BOM.csv"),
            "--exclude-dnp",
            str(SCH),
        ]
    )
    run(
        [
            str(KICAD_CLI),
            "sch",
            "export",
            "netlist",
            "--output",
            str(REPORTS / "RoyalNode_RevA.net"),
            str(SCH),
        ]
    )

    write_draft_jlc_bom()
    write_blocker_note()
    zip_dir(GERBERS, OUT / "RoyalNode_RevA_Gerbers_DRAFT_NOT_FOR_FAB.zip")
    zip_dir(DRILL, OUT / "RoyalNode_RevA_Drill_DRAFT_NOT_FOR_FAB.zip")
    zip_dir(ASSEMBLY, OUT / "RoyalNode_RevA_Assembly_DRAFT_NOT_FOR_FAB.zip")
    print(f"Wrote draft quote package to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
