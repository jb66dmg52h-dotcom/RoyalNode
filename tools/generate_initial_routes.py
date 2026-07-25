#!/usr/bin/env python3
"""Generate the first low-risk RoyalNode PCB routes.

This intentionally routes only stable, low-current nets and adds the intended
Layer-2 ground reference plane. It does not route RF, high-current power rails
or switching loops.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "hardware/kicad/RoyalNode/RoyalNode.kicad_pcb"
NAMESPACE = uuid.UUID("0c64c82f-b03a-455f-93ce-ceb8a0674a31")

NETS = {
    "GND": 1,
    "3V3": 2,
    "E22_TXEN_DIO2": 44,
    "I2C_SCL": 45,
    "I2C_SDA": 46,
}

SEGMENTS = [
    {
        "name": "e22-dio2-to-txen",
        "net": "E22_TXEN_DIO2",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(30.35, 59.08), (30.35, 61.62)],
    },
    {
        "name": "j6-3v3-fanout",
        "net": "3V3",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(90.12, 25.15), (90.12, 22.30)],
    },
    {
        "name": "j6-3v3-backbone",
        "net": "3V3",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(90.12, 22.30), (82.00, 22.30), (82.00, 33.54), (80.39, 33.54)],
    },
    {
        "name": "j6-gnd-fanout",
        "net": "GND",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(91.38, 25.15), (91.38, 23.80)],
    },
    {
        "name": "j6-gnd-backbone",
        "net": "GND",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(91.38, 23.80), (84.00, 23.80), (84.00, 38.62), (80.39, 38.62)],
    },
    {
        "name": "j6-sda-fanout",
        "net": "I2C_SDA",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(92.62, 25.15), (92.62, 21.50)],
    },
    {
        "name": "j6-sda-backbone",
        "net": "I2C_SDA",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(92.62, 21.50), (60.00, 21.50), (60.00, 33.54), (62.61, 33.54)],
    },
    {
        "name": "j6-scl-fanout",
        "net": "I2C_SCL",
        "layer": "F.Cu",
        "width": 0.20,
        "points": [(93.88, 25.15), (93.88, 20.75)],
    },
    {
        "name": "j6-scl-backbone",
        "net": "I2C_SCL",
        "layer": "B.Cu",
        "width": 0.20,
        "points": [(93.88, 20.75), (58.80, 20.75), (58.80, 36.08), (62.61, 36.08)],
    },
]

VIAS = [
    {"name": "j6-3v3-via", "net": "3V3", "at": (90.12, 22.30)},
    {"name": "j6-gnd-via", "net": "GND", "at": (91.38, 23.80)},
    {"name": "j6-sda-via", "net": "I2C_SDA", "at": (92.62, 21.50)},
    {"name": "j6-scl-via", "net": "I2C_SCL", "at": (93.88, 20.75)},
]

def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "::".join(parts)))


GROUND_ZONE_UUID = stable_uuid("zone", "l2-ground-reference")


def generated_uuids() -> set[str]:
    ids: set[str] = set()
    for route in SEGMENTS:
        points = route["points"]
        for index in range(len(points) - 1):
            ids.add(stable_uuid("segment", str(route["name"]), str(index)))
    for via in VIAS:
        ids.add(stable_uuid("via", str(via["name"])))
    ids.add(GROUND_ZONE_UUID)
    return ids


def remove_generated_routes(text: str) -> str:
    ids = generated_uuids()
    result: list[str] = []
    idx = 0
    pattern = re.compile(r"\n  \((segment|via|zone)\b")
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
    net_id = NETS[net]
    return (
        f'  (segment\n'
        f'    (start {start[0]:.2f} {start[1]:.2f})\n'
        f'    (end {end[0]:.2f} {end[1]:.2f})\n'
        f'    (width {width:.2f})\n'
        f'    (layer "{layer}")\n'
        f'    (net {net_id})\n'
        f'    (uuid "{stable_uuid("segment", name, str(index))}")\n'
        f'  )'
    )


def via_block(name: str, net: str, at: tuple[float, float]) -> str:
    net_id = NETS[net]
    return (
        f'  (via\n'
        f'    (at {at[0]:.2f} {at[1]:.2f})\n'
        f'    (size 0.60)\n'
        f'    (drill 0.30)\n'
        f'    (layers "F.Cu" "B.Cu")\n'
        f'    (net {net_id})\n'
        f'    (uuid "{stable_uuid("via", name)}")\n'
        f'  )'
    )


def ground_zone_block() -> str:
    return (
        f'  (zone\n'
        f'    (net 1)\n'
        f'    (net_name "GND")\n'
        f'    (layer "In1.Cu")\n'
        f'    (uuid "{GROUND_ZONE_UUID}")\n'
        f'    (name "L2_GND_REFERENCE")\n'
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
    blocks.append(ground_zone_block())
    return "\n".join(blocks)


def main() -> None:
    text = remove_generated_routes(PCB.read_text(encoding="utf-8")).rstrip()
    if not text.endswith(")"):
        raise SystemExit("PCB file does not end with a closing S-expression")
    body = text[:-1].rstrip()
    PCB.write_text(f"{body}\n{generated_blocks()}\n)\n", encoding="utf-8")
    print("Generated initial routes and L2 ground reference plane")


if __name__ == "__main__":
    main()
