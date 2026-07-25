#!/usr/bin/env python3
"""Generate the first RoyalNode PCB placement scaffold.

This places mechanical/placement anchors only. It deliberately does not route
nets and does not claim fabrication readiness for draft footprints.
"""

from __future__ import annotations

import csv
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KICAD_DIR = ROOT / "hardware/kicad/RoyalNode"
PCB = KICAD_DIR / "RoyalNode.kicad_pcb"
FP_DIR = KICAD_DIR / "lib_footprints/RoyalNode.pretty"
SEED = KICAD_DIR / "SCHEMATIC_CAPTURE_SEED_REV_A.csv"
PASSIVE_SEED = KICAD_DIR / "PASSIVE_CAPTURE_SEED_REV_A.csv"
KICAD_FP_ROOT = Path("/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints")
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
        "at": (71.5, 31.0, 0),
        "note": "Composite footprint for two LXWCONN 1x7 socket strips; shifted above the RF corridor.",
    },
    {
        "ref": "J5",
        "value": "SMA edge envelope",
        "file": "J5_SMA_0732511150_DRAFT_ENVELOPE.kicad_mod",
        "library_name": "J5_SMA_0732511150_DRAFT_ENVELOPE",
        "at": (100.0, 41.3, 0),
        "note": "DRAFT envelope only; Molex launch footprint remains blocked.",
    },
    {
        "ref": "J1",
        "value": "XT30PW-M C431092 RC",
        "file": "J_POWER_XT30PW_M_C431092_RC.kicad_mod",
        "library_name": "J_POWER_XT30PW_M_C431092_RC",
        "at": (93.0, 62.0, 0),
        "note": "Imported JLC/EasyEDA footprint; polarity still requires review.",
    },
    {
        "ref": "J2",
        "value": "XT30PW-M C431092 RC",
        "file": "J_POWER_XT30PW_M_C431092_RC.kicad_mod",
        "library_name": "J_POWER_XT30PW_M_C431092_RC",
        "at": (93.0, 78.0, 0),
        "note": "Imported JLC/EasyEDA footprint; polarity still requires review.",
    },
    {
        "ref": "J3",
        "value": "JST-GH XIAO BAT HARNESS",
        "file": "J_LOW_JST_GH_SM02B_GHS_TB_RC.kicad_mod",
        "library_name": "J_LOW_JST_GH_SM02B_GHS_TB_RC",
        "at": (92.0, 36.5, 0),
        "note": "Internal two-wire XIAO underside BAT/GND harness; JST-GH family.",
    },
    {
        "ref": "J4",
        "value": "JST-GH BATTERY NTC",
        "file": "J_LOW_JST_GH_SM02B_GHS_TB_RC.kicad_mod",
        "library_name": "J_LOW_JST_GH_SM02B_GHS_TB_RC",
        "at": (84.5, 88.5, 0),
        "note": "Internal battery-mounted NTC safety harness; JST-GH family.",
    },
    {
        "ref": "J6",
        "value": "JST-GH BME680 I2C",
        "file": "J_LOW_JST_GH_SM04B_GHS_TB_RC.kicad_mod",
        "library_name": "J_LOW_JST_GH_SM04B_GHS_TB_RC",
        "at": (92.0, 27.0, 0),
        "note": "Optional MeshCore-supported environmental I2C port; JST-GH family.",
    },
    {
        "ref": "U1",
        "value": "BQ25798 RQM0029A RC",
        "file": "U1_BQ25798_RQM0029A_RC.kicad_mod",
        "library_name": "U1_BQ25798_RQM0029A_RC",
        "at": (65.0, 75.0, 0),
        "note": "Charger/controller candidate footprint near solar and battery input region.",
    },
    {
        "ref": "L1",
        "value": "XAL7070-222MEC RC",
        "file": "L1_COILCRAFT_XAL7070_222MEC_RC.kicad_mod",
        "library_name": "L1_COILCRAFT_XAL7070_222MEC_RC",
        "at": (65.0, 84.0, 0),
        "note": "BQ25798 charger inductor placement candidate.",
    },
    {
        "ref": "U3",
        "value": "TPS61088 RHL0020A thermal vias RC",
        "file": "U3_TPS61088_RHL0020A_THERMALVIAS_RC.kicad_mod",
        "library_name": "U3_TPS61088_RHL0020A_THERMALVIAS_RC",
        "at": (59.0, 55.0, 0),
        "note": "5 V radio boost converter placement candidate near E22 VCC side.",
    },
    {
        "ref": "L2",
        "value": "XAL7030-222MEC RC",
        "file": "L2_COILCRAFT_XAL7030_222MEC_RC.kicad_mod",
        "library_name": "L2_COILCRAFT_XAL7030_222MEC_RC",
        "at": (66.5, 55.0, 0),
        "note": "TPS61088 boost inductor placement candidate.",
    },
    {
        "ref": "U2",
        "value": "LM66100 DCK0006A SC70-6 RC",
        "file": "U2_LM66100_DCK0006A_SC70_6_RC.kicad_mod",
        "library_name": "U2_LM66100_DCK0006A_SC70_6_RC",
        "at": (84.0, 49.0, 0),
        "note": "XIAO power ideal-diode candidate placement.",
    },
    {
        "ref": "U4",
        "value": "LTC4365 TSOT-23-8 RC",
        "file": "U4_LTC4365_TSOT23_8_RC.kicad_mod",
        "library_name": "U4_LTC4365_TSOT23_8_RC",
        "at": (74.0, 50.0, 0),
        "note": "Solar UV/OV protection controller placement candidate.",
    },
    {
        "ref": "F1",
        "value": "Littelfuse 0483002.DR 1206 RC",
        "file": "F1_LITTELFUSE_483_1206_RC.kicad_mod",
        "library_name": "F1_LITTELFUSE_483_1206_RC",
        "at": (87.0, 54.0, 0),
        "note": "Solar input fuse placement candidate immediately after solar XT30.",
    },
    {
        "ref": "Q1",
        "value": "Infineon PG-DSO-8-27 thermal vias RC",
        "file": "Q_POWER_INFINEON_PG_DSO_8_27_RC.kicad_mod",
        "library_name": "Q_POWER_INFINEON_PG_DSO_8_27_RC",
        "at": (78.0, 56.0, 0),
        "note": "Solar protection back-to-back FET placement candidate.",
    },
    {
        "ref": "Q2",
        "value": "Infineon PG-DSO-8-27 thermal vias RC",
        "file": "Q_POWER_INFINEON_PG_DSO_8_27_RC.kicad_mod",
        "library_name": "Q_POWER_INFINEON_PG_DSO_8_27_RC",
        "at": (78.0, 64.0, 0),
        "note": "BQ25798 solar input selector FET placement candidate.",
    },
    {
        "ref": "Q3",
        "value": "Infineon PG-DSO-8-27 thermal vias RC",
        "file": "Q_POWER_INFINEON_PG_DSO_8_27_RC.kicad_mod",
        "library_name": "Q_POWER_INFINEON_PG_DSO_8_27_RC",
        "at": (78.0, 72.0, 0),
        "note": "BQ25798 USB input selector FET placement candidate.",
    },
]
GENERATED_LIBRARY_NAMES = {str(item["library_name"]) for item in PLACEMENTS}
GENERATED_LIBRARY_NAMES.update(
    {
        "MOD1_XIAO_NRF52840_DRAFT_ENVELOPE",
        "J_POWER_XT30PW_M_DRAFT_ENVELOPE",
    }
)
GENERATED_REFS = {str(item["ref"]) for item in PLACEMENTS}


def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "::".join(parts)))


def quote(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def load_seed_nets() -> tuple[dict[str, int], dict[str, dict[str, tuple[str, str]]]]:
    rows = list(csv.DictReader(SEED.open(newline="", encoding="utf-8")))
    passive_rows = list(csv.DictReader(PASSIVE_SEED.open(newline="", encoding="utf-8")))
    pin_nets: dict[str, dict[str, tuple[str, str]]] = {}
    nets: set[str] = set()
    for row in rows:
        ref = row["Reference"]
        pin = row["Pin"]
        net = row["Net"]
        pin_name = row["Pin Name"]
        pin_nets.setdefault(ref, {})[pin] = (net, pin_name)
        if net != "NC":
            nets.add(net)
    for row in passive_rows:
        ref = row["Reference"]
        for pin, net in [("1", row["Pin 1 Net"]), ("2", row["Pin 2 Net"])]:
            pin_nets.setdefault(ref, {})[pin] = (net, f"Terminal {pin}")
            if net != "NC":
                nets.add(net)

    priority = [
        "GND",
        "3V3",
        "BAT_RAW",
        "BQ_SYS",
        "5V_RADIO",
        "RF_915",
        "SOLAR_RAW",
        "SOLAR_FUSED",
        "SOLAR_PROTECTED",
        "USB_VBUS_RAW",
    ]
    ordered = [net for net in priority if net in nets]
    ordered.extend(sorted(nets - set(ordered)))
    return {net: index for index, net in enumerate(ordered, start=1)}, pin_nets


def net_table(net_ids: dict[str, int]) -> str:
    lines = ['  (net 0 "")']
    for net, index in sorted(net_ids.items(), key=lambda item: item[1]):
        lines.append(f'  (net {index} "{quote(net)}")')
    return "\n".join(lines)


def replace_net_table(text: str, net_ids: dict[str, int]) -> str:
    text = re.sub(r'\n  \(net \d+ "[^"]*"\)', "", text)
    marker = "\n\n  (gr_rect"
    if marker not in text:
        raise SystemExit("could not find insertion point for PCB net table")
    return text.replace(marker, f"\n{net_table(net_ids)}{marker}", 1)


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
        has_generated_library = any(f'(footprint "RoyalNode:{name}"' in block for name in GENERATED_LIBRARY_NAMES)
        has_generated_ref = any(f'(property "Reference" "{ref}"' in block for ref in GENERATED_REFS)
        if not (has_generated_library or has_generated_ref):
            result.append(block)
        idx = end
    return "".join(result)


def annotate_pad_block(
    block: str,
    ref: str,
    net_ids: dict[str, int],
    pin_nets: dict[str, dict[str, tuple[str, str]]],
) -> str:
    pad_number = re.search(r'\(pad\s+"?([^"\s)]+)"?', block)
    if not pad_number:
        return block
    pin = pad_number.group(1)
    net, pin_name = pin_nets.get(ref, {}).get(pin, ("NC", ""))
    block = re.sub(r'\n[ \t]*\((?:net|pinfunction|pintype)\s+[^\n]*\)', "", block)
    if net == "NC":
        return block
    if net not in net_ids:
        raise SystemExit(f"missing net id for {ref} pin {pin}: {net}")
    insert = f'\n\t\t(net {net_ids[net]} "{quote(net)}")\n\t\t(pinfunction "{quote(pin_name)}")'
    return block[:-1] + insert + block[-1:]


def annotate_footprint_pads(
    text: str,
    ref: str,
    net_ids: dict[str, int],
    pin_nets: dict[str, dict[str, tuple[str, str]]],
) -> str:
    result: list[str] = []
    idx = 0
    while True:
        match = re.search(r"^[ \t]*\(pad\s+", text[idx:], re.M)
        if not match:
            result.append(text[idx:])
            break
        start = idx + match.start()
        result.append(text[idx:start])
        depth = 0
        end = start
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
        result.append(annotate_pad_block(text[start:end], ref, net_ids, pin_nets))
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
    text = re.sub(r'\n[ \t]*\(tags "[^"]*"\)', "", text)
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


def passive_position(index: int, group: str) -> tuple[float, float, float]:
    if group in {"boost", "radio"}:
        columns = 6
        base_x, base_y = 24.5, 24.5
        pitch_x, pitch_y = 5.6, 4.5
    elif group == "protection":
        columns = 2
        base_x, base_y = 22.0, 38.0
        pitch_x, pitch_y = 4.8, 4.8
    else:
        columns = 6
        base_x, base_y = 24.0, 77.0
        pitch_x, pitch_y = 5.6, 4.0
    column = index % columns
    row = index // columns
    return base_x + column * pitch_x, base_y + row * pitch_y, 0.0


def passive_group(ref: str) -> str:
    if ref in {"R100", "R101", "R102", "R103"}:
        return "protection"
    if ref.startswith("C4") or ref.startswith("R4") or ref in {"C500", "C501", "C502", "C503"}:
        return "boost"
    return "charger"


PASSIVE_POSITION_OVERRIDES = {
    "R404": (26.8, 47.0, 0.0),
    "R405": (22.0, 47.0, 0.0),
    "C500": (58.0, 91.0, 0.0),
    "C501": (64.0, 91.0, 0.0),
    "C502": (70.0, 91.0, 0.0),
    "C503": (93.0, 46.0, 0.0),
}


def passive_placements() -> list[dict[str, object]]:
    counters = {"charger": 0, "boost": 0, "protection": 0}
    items: list[dict[str, object]] = []
    for row in csv.DictReader(PASSIVE_SEED.open(newline="", encoding="utf-8")):
        footprint = row.get("Footprint", "")
        if not footprint:
            continue
        library, name = footprint.split(":", 1)
        group = passive_group(row["Reference"])
        at = PASSIVE_POSITION_OVERRIDES.get(row["Reference"], passive_position(counters[group], group))
        counters[group] += 1
        items.append(
            {
                "ref": row["Reference"],
                "value": row["Value"],
                "file": f"{name}.kicad_mod",
                "library_name": name,
                "library": library,
                "at": at,
                "note": f"Generated {group} passive staging placement from passive capture seed.",
            }
        )
    return items


def standard_footprint_path(item: dict[str, object]) -> Path:
    library = str(item.get("library", ""))
    filename = str(item["file"])
    if library == "RoyalNode":
        return FP_DIR / filename
    if library:
        return KICAD_FP_ROOT / f"{library}.pretty" / filename
    return FP_DIR / filename


def passive_footprint_block(item: dict[str, object]) -> str:
    path = standard_footprint_path(item)
    if not path.exists():
        raise SystemExit(f"missing passive footprint source {path}")
    text = path.read_text(encoding="utf-8").strip()
    text = re.sub(r'\n[ \t]*\(tags "[^"]*"\)', "", text)
    library = str(item["library"])
    library_name = str(item["library_name"])
    ref = str(item["ref"])
    value = str(item["value"])
    x, y, rot = item["at"]  # type: ignore[misc]
    text = text.replace(f'(footprint "{library_name}"', f'(footprint "{library}:{library_name}"', 1)
    text = text.replace('(property "Reference" "REF**"', f'(property "Reference" "{ref}"', 1)
    text = text.replace(f'(property "Value" "{library_name}"', f'(property "Value" "{value}"', 1)
    text = re.sub(
        r'(\(property "Reference" "[^"]+"\n\s+\(at [^\n]+\)\n\s+\(layer "F\.SilkS"\))',
        r"\1\n\t\t(hide yes)",
        text,
        count=1,
    )
    text = re.sub(
        r'(\(property "Value" "[^"]+"\n\s+\(at [^\n]+\)\n\s+\(layer "F\.Fab"\))',
        r"\1\n\t\t(hide yes)",
        text,
        count=1,
    )
    lines = text.splitlines()
    lines.insert(4, f'  (at {x:.2f} {y:.2f} {rot})')
    lines.insert(5, f'  (uuid "{stable_uuid(ref, library, library_name)}")')
    return "\n".join("  " + line if line else line for line in lines)


def main() -> None:
    net_ids, pin_nets = load_seed_nets()
    generated_items = PLACEMENTS + passive_placements()
    GENERATED_REFS.update(str(item["ref"]) for item in generated_items)
    pcb_text = PCB.read_text(encoding="utf-8")
    pcb_text = replace_net_table(pcb_text, net_ids)
    pcb_text = remove_generated_placements(pcb_text).rstrip()
    if not pcb_text.endswith(")"):
        raise SystemExit("PCB file does not end with a closing S-expression")
    body = pcb_text[:-1].rstrip()
    generated_blocks: list[str] = []
    for item in generated_items:
        if str(item.get("library", "")):
            block = passive_footprint_block(item)
        else:
            block = footprint_block(item)
        generated_blocks.append(annotate_footprint_pads(block, str(item["ref"]), net_ids, pin_nets))
    generated = "\n".join(generated_blocks)
    PCB.write_text(f"{body}\n{generated}\n)\n", encoding="utf-8")
    print(f"Placed {len(generated_items)} generated PCB footprint anchors")


if __name__ == "__main__":
    main()
