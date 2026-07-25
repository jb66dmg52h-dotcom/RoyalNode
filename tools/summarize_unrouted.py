#!/usr/bin/env python3
"""Summarize KiCad unrouted items by net for the current Rev A layout pass."""

from __future__ import annotations

import collections
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRC = ROOT / "hardware/fabrication/RoyalNode_drc.rpt"
OUT = ROOT / "docs/UNROUTED_SUMMARY_REV_A.md"


def main() -> None:
    text = DRC.read_text(encoding="utf-8")
    pairs: list[tuple[str, str]] = []
    lines_in = text.splitlines()
    for index, line in enumerate(lines_in):
        if not line.startswith("[unconnected_items]"):
            continue
        item_lines = [
            candidate
            for candidate in lines_in[index + 1 : index + 6]
            if candidate.strip().startswith("@(")
        ]
        if len(item_lines) < 2:
            continue
        first = re.search(r"\[([^\]]+)\]", item_lines[0])
        second = re.search(r"\[([^\]]+)\]", item_lines[1])
        if first and second:
            pairs.append((first.group(1), second.group(1)))
    net_counts: collections.Counter[str] = collections.Counter()
    mismatched_pairs: list[tuple[str, str]] = []
    for first, second in pairs:
        if first != second:
            mismatched_pairs.append((first, second))
        net_counts[first] += 1

    lines = [
        "# Unrouted Summary Rev A",
        "",
        "Generated from `hardware/fabrication/RoyalNode_drc.rpt`.",
        "",
        "This file is a layout planning aid, not a manufacturing release note. Counts are KiCad ratsnest-pair counts, so a net with several components can appear multiple times.",
        "",
        f"Total unrouted pairs: {sum(net_counts.values())}",
        "",
        "| Net | Ratsnest pairs | Layout note |",
        "|---|---:|---|",
    ]

    notes = {
        "RF_915": "Hold for final SMA footprint and 50-ohm GCPW review.",
        "BOOST_EN": "Hold for TPS61088/R405 local fanout placement pass.",
        "BQ_REGN": "Hold for BQ25798 local fanout and inductor-area placement pass.",
        "GND": "Route through ground pours/stitching after component placement is stable.",
        "5V_RADIO": "Route as high-current power pour after boost/radio placement review.",
        "BQ_SYS": "Route as system power pour after charger/boost placement review.",
        "BAT_RAW": "Route as high-current battery path after XT30 and power-path review.",
        "SOLAR_RAW": "Route with input protection path after XT30/fuse placement review.",
        "SOLAR_FUSED": "Route with solar protection power path after Q1/U4 placement review.",
        "SOLAR_PROTECTED": "Route with protected solar path after Q1/Q2/U1 placement review.",
        "BQ_SW1": "Switch node; keep compact and route only after BQ25798 power-loop placement.",
        "BQ_SW2": "Switch node; keep compact and route only after BQ25798 power-loop placement.",
        "BOOST_SW": "Switch node; keep compact and route only after TPS61088 power-loop placement.",
        "BQ_PMID": "Route as local charger power copper after capacitor placement review.",
        "BQ_VBUS": "Route as input-selector power copper after Q2/Q3/U1 placement review.",
    }

    for net, count in sorted(net_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{net}` | {count} | {notes.get(net, '')} |")

    if mismatched_pairs:
        lines.extend(
            [
                "",
                "## Mismatched Net Pairs",
                "",
                "These should be investigated because each KiCad unrouted pair is expected to refer to one net.",
                "",
            ]
        )
        for first, second in mismatched_pairs:
            lines.append(f"- `{first}` / `{second}`")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
