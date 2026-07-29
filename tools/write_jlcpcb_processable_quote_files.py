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

EXCLUDED_FROM_PCBA_QUOTE = {
    "MOD1": "Seeed XIAO nRF52840 is sourced and installed by the user.",
    # JLCPCB had no safe in-stock drop-in dual N-channel PG-DSO-8 substitute for
    # the input-selector MOSFETs during quote processing. Keep them out of the
    # auto-assembly quote instead of substituting an N+P part into an N+N circuit.
    "Q1": "JLCPCB had no safe in-stock drop-in dual N-channel PG-DSO-8 substitute.",
    "Q2": "JLCPCB had no safe in-stock drop-in dual N-channel PG-DSO-8 substitute.",
    "Q3": "JLCPCB had no safe in-stock drop-in dual N-channel PG-DSO-8 substitute.",
    "J5": "Molex edge-launch SMA was recognized but not placed in the successful JLC quote flow.",
    # These are recognized by JLCPCB but remained inventory-short in the SMT quote
    # flow after multiple JLC-source substitutions. Excluding them allows a quote
    # for the board and confirmed assembly rows without pretending the design is
    # release-ready.
    "R102": "Quote-blocked precision divider resistor; JLC-source candidates were short.",
    "R200": "Quote-blocked TS-network resistor; JLC-source candidates were short.",
    "R201": "Quote-blocked TS-network resistor; JLC-source candidates were short.",
    "R400": "Quote-blocked TPS61088 feedback resistor; JLC-source candidates were short.",
    "R401": "Quote-blocked TPS61088 feedback resistor; JLC-source candidates were short.",
    "U4": "Quote-blocked LTC4365 input-protection controller; JLC-source candidates were short.",
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
        "lcsc": "C1724666",
        "note": "Vishay TNPW060340K2BEEN; same value/package precision UV/OV divider substitute.",
    },
    "R200": {
        "comment": "5.23 kOhm 0.1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C1716516",
        "note": "Yageo RT0603WRD075K23L; same value/package precision TS-network substitute.",
    },
    "R201": {
        "comment": "30.1 kOhm 0.1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C4041890",
        "note": "Yageo RT0603WRC0730K1L; same value/package precision TS-network substitute.",
    },
    "R400": {
        "comment": "176 kOhm 0.1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C2497648",
        "note": "KOA RN73R1JTTD1763D50; same value/package TPS61088 feedback quote substitute.",
    },
    "R401": {
        "comment": "56.0 kOhm 0.1%",
        "footprint": "Resistor_SMD:R_0603_1608Metric",
        "lcsc": "C4159977",
        "note": "Vishay TNPW060356K0BETA; same value/package TPS61088 feedback substitute.",
    },
    "U4": {
        "comment": "LTC4365HTS8-1#PBF",
        "footprint": "TSOT-23-8",
        "lcsc": "C117259",
        "note": "ADI LTC4365HTS8-1#PBF; same -1 TSOT-23-8 protection-controller family, higher temperature grade.",
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
            if not refs or all(ref in EXCLUDED_FROM_PCBA_QUOTE for ref in refs):
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
    included_refs = {row["Ref"] for row in cpl_rows if row["Ref"] not in EXCLUDED_FROM_PCBA_QUOTE}
    emitted_refs = write_bom(args.assembly_dir, included_refs)
    write_cpl(args.assembly_dir, emitted_refs)

    print("Wrote JLCPCB processable quote files:")
    print(args.assembly_dir / "RoyalNode_RevA_JLCPCB_BOM_PROCESSABLE_QUOTE.csv")
    print(args.assembly_dir / "RoyalNode_RevA_JLCPCB_CPL_PROCESSABLE_QUOTE.csv")
    print("Forced substitutes:")
    for designator, part in FORCED_PARTS.items():
        print(f"- {designator}: {part['lcsc']} ({part['note']})")
    print("Excluded from PCBA quote:")
    for designator in sorted(EXCLUDED_FROM_PCBA_QUOTE):
        print(f"- {designator}: {EXCLUDED_FROM_PCBA_QUOTE[designator]}")


if __name__ == "__main__":
    main()
