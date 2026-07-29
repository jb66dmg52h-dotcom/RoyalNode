#!/usr/bin/env python3
"""Write JLCPCB sample-format BOM/CPL files for quote processing.

The draft export keeps every design intent visible. JLCPCB's SMT quote flow is
pickier: it needs only assemblable designators, sample-format headers, positive
placement coordinates, and forced JLC part numbers for parts that do not
auto-select cleanly.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ASSEMBLY_DIR = ROOT / "hardware/fabrication/quote_draft_rev_a/assembly"

USER_SUPPLIED = {
    "MOD1",  # Seeed XIAO nRF52840 is sourced and installed by the user.
}

FORCED_PARTS = {
    "C212,C213,C214": {
        "comment": "100 nF 50 V X7R",
        "footprint": "Capacitor_SMD:C_0603_1608Metric",
        "lcsc": "C14663",
        "note": "Yageo CC0603KRX7R9BB104; JLC-stock 0603 substitute.",
    },
    "C404": {
        "comment": "100 nF 50 V X7R",
        "footprint": "Capacitor_SMD:C_0603_1608Metric",
        "lcsc": "C14663",
        "note": "Yageo CC0603KRX7R9BB104; same substitute as C212-C214.",
    },
    "C215": {
        "comment": "4.7 uF 25 V X7R",
        "footprint": "Capacitor_SMD:C_0805_2012Metric",
        "lcsc": "C98195",
        "note": "Samsung CL21B475KAFNNNE; 0805 REGN bypass substitute.",
    },
    "C216,C217": {
        "comment": "47 nF 50 V X7R",
        "footprint": "Capacitor_SMD:C_0603_1608Metric",
        "lcsc": "C1622",
        "note": "Samsung CL10B473KB8NNNC; 0603 bootstrap-cap substitute.",
    },
    "C218": {
        "comment": "1 nF 50 V C0G",
        "footprint": "Capacitor_SMD:C_0603_1608Metric",
        "lcsc": "C163508",
        "note": "Samsung CL10C102JB8NNNC; 0603 SDRV-cap substitute.",
    },
    "C405": {
        "comment": "2.2 uF 25 V X7R",
        "footprint": "Capacitor_SMD:C_0805_2012Metric",
        "lcsc": "C74690",
        "note": "FH 0805B225K250NT; 0805 TPS61088 VCC-cap substitute.",
    },
    "F1": {
        "comment": "SF-1206S500-2",
        "footprint": "Fuse:Fuse_1206_3216Metric",
        "lcsc": "C913282",
        "note": "Bourns 5 A 1206 fuse; quote substitute for Littelfuse 0483005.DR.",
    },
    "Q1": {
        "comment": "ISA250250N04LMDSXTMA1",
        "footprint": "PG-DSO-8",
        "lcsc": "C43317100",
        "note": "Infineon same-family dual N-channel PG-DSO-8 candidate; release-review required.",
    },
    "Q2": {
        "comment": "ISA250250N04LMDSXTMA1",
        "footprint": "PG-DSO-8",
        "lcsc": "C43317100",
        "note": "Same quote candidate as Q1.",
    },
    "Q3": {
        "comment": "ISA250250N04LMDSXTMA1",
        "footprint": "PG-DSO-8",
        "lcsc": "C43317100",
        "note": "Same quote candidate as Q1.",
    },
    "J5": {
        "comment": "0732511150",
        "footprint": "1.60 mm PCB edge mount",
        "lcsc": "C841205",
        "note": "Exact Molex 73251-1150 / 0732511150 SMA edge-launch connector.",
    },
    "J6": {
        "comment": "XY-SM04B-GHS-TB",
        "footprint": "4-pin 1.25 mm SMT JST-GH-compatible",
        "lcsc": "C51940118",
        "note": "XYECONN right-angle 4-pin GH-compatible connector; footprint release-review required.",
    },
    "R100": {
        "comment": "1.78 MOhm 1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C166890",
        "note": "RALEC RTT031784FTP; 0603 UV/OV divider substitute.",
    },
    "R102": {
        "comment": "40.2 kOhm 0.1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C4210499",
        "note": "Vishay TNPW060340K2BYEN; precision UV/OV divider substitute.",
    },
    "R200": {
        "comment": "5.23 kOhm 0.1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C4076829",
        "note": "Vishay TNPU06035K23BZEN00; precision TS-network substitute.",
    },
    "R201": {
        "comment": "30.1 kOhm 0.1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C1709086",
        "note": "Susumu RG1608N-3012-B-T5; precision TS-network substitute.",
    },
    "R400": {
        "comment": "180 kOhm 0.1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C4074070",
        "note": "KOA RN731JTTD1803B50; paired with 57.6 kOhm R401 for quote-time TPS61088 feedback.",
    },
    "R401": {
        "comment": "57.6 kOhm 0.1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C4106968",
        "note": "SEI RNCF0603BTE57K6; paired with 180 kOhm R400 for about 4.97 V nominal output.",
    },
    "U4": {
        "comment": "LTC4365HTS8-1#TRMPBF",
        "footprint": "TSOT-23-8",
        "lcsc": "C688323",
        "note": "ADI high-temperature -1 variant; same TSOT-23-8 family, release-review required.",
    },
}


def split_designators(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_bom(assembly_dir: Path, included_refs: set[str]) -> set[str]:
    source = assembly_dir / "RoyalNode_RevA_JLCPCB_DRAFT_BOM.csv"
    destination = assembly_dir / "RoyalNode_RevA_JLCPCB_BOM_PROCESSABLE_QUOTE.csv"
    rows = read_csv(source)

    emitted_refs: set[str] = set()
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["Comment", "Designator", "Footprint", "JLCPCB Part #（optional）"],
        )
        writer.writeheader()

        for row in rows:
            refs = split_designators(row["Designator"])
            if not refs or all(ref in USER_SUPPLIED for ref in refs):
                continue
            if row["Assembly Scope"] != "pcba":
                continue
            if not any(ref in included_refs for ref in refs):
                continue

            override = FORCED_PARTS.get(row["Designator"])
            comment = row["Value"]
            footprint = row["Footprint"]
            lcsc = row["LCSC Part Number"]
            if override:
                comment = override["comment"]
                footprint = override["footprint"]
                lcsc = override["lcsc"]

            writer.writerow(
                {
                    "Comment": comment,
                    "Designator": row["Designator"],
                    "Footprint": footprint,
                    "JLCPCB Part #（optional）": lcsc,
                }
            )
            emitted_refs.update(ref for ref in refs if ref in included_refs)

    return emitted_refs


def write_cpl(assembly_dir: Path, emitted_refs: set[str]) -> None:
    source = assembly_dir / "RoyalNode_RevA_CPL.csv"
    destination = assembly_dir / "RoyalNode_RevA_JLCPCB_CPL_PROCESSABLE_QUOTE.csv"
    rows = read_csv(source)

    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["Designator", "Mid X", "Mid Y", "Layer", "Rotation"],
        )
        writer.writeheader()

        for row in rows:
            ref = row["Ref"]
            if ref not in emitted_refs:
                continue
            x = float(row["PosX"])
            y = -float(row["PosY"])
            rotation = float(row["Rot"])
            layer = "Top" if row["Side"].lower() == "top" else "Bottom"
            writer.writerow(
                {
                    "Designator": ref,
                    "Mid X": f"{x:.4f}mm",
                    "Mid Y": f"{y:.4f}mm",
                    "Layer": layer,
                    "Rotation": f"{rotation:g}",
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assembly-dir",
        type=Path,
        default=DEFAULT_ASSEMBLY_DIR,
        help="Directory containing RoyalNode_RevA_CPL.csv and JLC draft BOM.",
    )
    args = parser.parse_args()

    cpl_rows = read_csv(args.assembly_dir / "RoyalNode_RevA_CPL.csv")
    included_refs = {row["Ref"] for row in cpl_rows if row["Ref"] not in USER_SUPPLIED}
    emitted_refs = write_bom(args.assembly_dir, included_refs)
    write_cpl(args.assembly_dir, emitted_refs)

    print("Wrote JLCPCB processable quote files:")
    print(args.assembly_dir / "RoyalNode_RevA_JLCPCB_BOM_PROCESSABLE_QUOTE.csv")
    print(args.assembly_dir / "RoyalNode_RevA_JLCPCB_CPL_PROCESSABLE_QUOTE.csv")
    print("Forced substitutes:")
    for designator, part in FORCED_PARTS.items():
        print(f"- {designator}: {part['lcsc']} ({part['note']})")
    print("User-supplied / excluded:")
    for designator in sorted(USER_SUPPLIED):
        print(f"- {designator}")


if __name__ == "__main__":
    main()
