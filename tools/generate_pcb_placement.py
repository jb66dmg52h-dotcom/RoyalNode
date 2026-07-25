#!/usr/bin/env python3
"""Generate the first RoyalNode PCB placement scaffold.

This places mechanical/placement anchors only. It deliberately does not route
nets and does not claim fabrication readiness for draft footprints.
"""

from __future__ import annotations

import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KICAD_DIR = ROOT / "hardware/kicad/RoyalNode"
PCB = KICAD_DIR / "RoyalNode.kicad_pcb"
FP_DIR = KICAD_DIR / "lib_footprints/RoyalNode.pretty"
NAMESPACE = uuid.UUID("72281bec-369e-4e5b-a74d-54cf1dc496b3")

PLACEMENTS = [
    {
        "ref": "MOD2",
        "value": "E22-900M33S C22399506 RC",
        "file": "MOD2_E22_900M33S_JLC_C22399506_RC.kicad_mod",
        "library_name": "MOD2_E22_900M33S_JLC_C22399506_RC",
        "at": (42.0, 54.0, 180),
        "note": "Pin 21 faces the SMA/RF corridor; factory-installed PCBA item.",
    },
    {
        "ref": "MOD1",
        "value": "XIAO nRF52840 socket C53202181 RC",
        "file": "MOD1_XIAO_NRF52840_SOCKET_C53202181_RC.kicad_mod",
        "library_name": "MOD1_XIAO_NRF52840_SOCKET_C53202181_RC",
        "at": (71.5, 34.0, 0),
        "note": "Composite footprint for two LXWCONN 1x7 socket strips.",
    },
    {
        "ref": "J5",
        "value": "SMA edge envelope",
        "file": "J5_SMA_0732511150_DRAFT_ENVELOPE.kicad_mod",
        "library_name": "J5_SMA_0732511150_DRAFT_ENVELOPE",
        "at": (90.0, 41.3, 0),
        "note": "DRAFT envelope only; Molex launch footprint remains blocked.",
    },
    {
        "ref": "J1",
        "value": "XT30PW-M C431092 RC",
        "file": "J_POWER_XT30PW_M_C431092_RC.kicad_mod",
        "library_name": "J_POWER_XT30PW_M_C431092_RC",
        "at": (83.0, 62.0, 0),
        "note": "Imported JLC/EasyEDA footprint; polarity still requires review.",
    },
    {
        "ref": "J2",
        "value": "XT30PW-M C431092 RC",
        "file": "J_POWER_XT30PW_M_C431092_RC.kicad_mod",
        "library_name": "J_POWER_XT30PW_M_C431092_RC",
        "at": (83.0, 76.5, 0),
        "note": "Imported JLC/EasyEDA footprint; polarity still requires review.",
    },
]
GENERATED_LIBRARY_NAMES = {str(item["library_name"]) for item in PLACEMENTS}
GENERATED_LIBRARY_NAMES.update(
    {
        "MOD1_XIAO_NRF52840_DRAFT_ENVELOPE",
        "J_POWER_XT30PW_M_DRAFT_ENVELOPE",
    }
)


def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "::".join(parts)))


def remove_generated_placements(text: str) -> str:
    result: list[str] = []
    idx = 0
    while True:
        start = text.find('\n  (footprint ', idx)
        if start == -1:
            result.append(text[idx:])
            break
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
        if not any(f'(footprint "RoyalNode:{name}"' in block for name in GENERATED_LIBRARY_NAMES):
            result.append(block)
        idx = end
    return "".join(result)


def footprint_block(item: dict[str, object]) -> str:
    text = (FP_DIR / str(item["file"])).read_text(encoding="utf-8").strip()
    library_name = str(item["library_name"])
    ref = str(item["ref"])
    value = str(item["value"])
    x, y, rot = item["at"]  # type: ignore[misc]

    if text.startswith("(module "):
        raise SystemExit(f"{item['file']} is legacy module syntax; use a KiCad-10-native footprint")
    text = text.replace(f'(footprint "{library_name}"', f'(footprint "RoyalNode:{library_name}"', 1)
    text = text.replace(f'(property "Reference" "{library_name.split("_")[0] if "_" in library_name else ref}"', f'(property "Reference" "{ref}"', 1)
    text = text.replace('(property "Reference" "J?"', f'(property "Reference" "{ref}"', 1)
    text = text.replace('(property "Reference" "J5"', f'(property "Reference" "{ref}"', 1)
    text = text.replace('(property "Reference" "MOD1"', f'(property "Reference" "{ref}"', 1)
    text = text.replace('(property "Reference" "MOD2"', f'(property "Reference" "{ref}"', 1)
    text = text.replace('(property "Reference" "REF**"', f'(property "Reference" "{ref}"', 1)
    text = text.replace('(property "Value" "E22-900M33S C22399506 RC"', f'(property "Value" "{value}"', 1)
    text = text.replace('(property "Value" "XIAO nRF52840 socket C53202181 RC"', f'(property "Value" "{value}"', 1)
    text = text.replace('(property "Value" "XIAO nRF52840 DRAFT ENVELOPE"', f'(property "Value" "{value}"', 1)
    text = text.replace('(property "Value" "SMA EDGE DRAFT ENVELOPE"', f'(property "Value" "{value}"', 1)
    text = text.replace('(property "Value" "XT30PW-M C431092 RC"', f'(property "Value" "{value}"', 1)
    text = text.replace('(property "Value" "XT30PW-M DRAFT ENVELOPE"', f'(property "Value" "{value}"', 1)

    lines = text.splitlines()
    lines.insert(4, f'  (at {x:.2f} {y:.2f} {rot})')
    lines.insert(5, f'  (uuid "{stable_uuid(ref, library_name)}")')
    return "\n".join("  " + line if line else line for line in lines)


def main() -> None:
    pcb_text = PCB.read_text(encoding="utf-8")
    pcb_text = remove_generated_placements(pcb_text).rstrip()
    if not pcb_text.endswith(")"):
        raise SystemExit("PCB file does not end with a closing S-expression")
    body = pcb_text[:-1].rstrip()
    generated = "\n".join(footprint_block(item) for item in PLACEMENTS)
    PCB.write_text(f"{body}\n{generated}\n)\n", encoding="utf-8")
    print(f"Placed {len(PLACEMENTS)} generated PCB footprint anchors")


if __name__ == "__main__":
    main()
