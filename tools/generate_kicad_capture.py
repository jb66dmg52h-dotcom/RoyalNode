#!/usr/bin/env python3
"""Generate the first RoyalNode KiCad schematic capture from the pin seed.

This is intentionally a capture scaffold, not a finished schematic. It places
the project-local symbols and attaches deterministic global labels from the
CSV pin map so reviewers can inspect the electrical intent inside KiCad.
"""

from __future__ import annotations

import csv
import re
import uuid
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KICAD_DIR = ROOT / "hardware/kicad/RoyalNode"
SEED = KICAD_DIR / "SCHEMATIC_CAPTURE_SEED_REV_A.csv"
PASSIVE_SEED = KICAD_DIR / "PASSIVE_CAPTURE_SEED_REV_A.csv"
SYMBOL_LIB = KICAD_DIR / "lib_symbols/RoyalNode.kicad_sym"
SCHEMATIC = KICAD_DIR / "RoyalNode.kicad_sch"

NAMESPACE = uuid.UUID("8cf8a6b7-5ff4-40ed-b9a3-bca28c567834")
WIRE_STUB_MM = 7.62

SYMBOL_MAP = {
    "MOD1": ("RoyalNode:RN_XIAO_nRF52840_SOCKET", "XIAO nRF52840", (55.88, 66.04)),
    "MOD2": ("RoyalNode:RN_E22_900M33S", "E22-900M33S", (55.88, 127.00)),
    "U1": ("RoyalNode:RN_BQ25798RQMR", "BQ25798RQMR", (149.86, 69.85)),
    "U2": ("RoyalNode:RN_LM66100DCKR", "LM66100DCKR", (248.92, 41.91)),
    "U3": ("RoyalNode:RN_TPS61088RHLR", "TPS61088RHLR", (248.92, 97.79)),
    "U4": ("RoyalNode:RN_LTC4365ITS8_1", "LTC4365ITS8-1", (149.86, 137.16)),
    "Q1": ("RoyalNode:RN_ISA170170N04LMDS", "ISA170170N04LMDS", (248.92, 149.86)),
    "Q2": ("RoyalNode:RN_ISA170170N04LMDS", "ISA170170N04LMDS", (248.92, 195.58)),
    "Q3": ("RoyalNode:RN_ISA170170N04LMDS", "ISA170170N04LMDS", (248.92, 241.30)),
    "J1": ("RoyalNode:RN_XT30PW_M", "XT30PW-M SOLAR", (55.88, 204.47)),
    "J2": ("RoyalNode:RN_XT30PW_M", "XT30PW-M BATTERY", (55.88, 233.68)),
    "J3": ("RoyalNode:RN_JST_GH_2", "JST-GH XIAO BAT HARNESS", (149.86, 204.47)),
    "J4": ("RoyalNode:RN_JST_GH_2", "JST-GH BATTERY NTC", (149.86, 233.68)),
    "J5": ("RoyalNode:RN_SMA_EDGE", "Molex 0732511150 SMA", (55.88, 266.70)),
    "F1": ("RoyalNode:RN_TWO_PIN_POWER_PART", "Littelfuse 0483002.DR", (55.88, 184.15)),
    "L1": ("RoyalNode:RN_TWO_PIN_POWER_PART", "Coilcraft XAL7070-222MEC", (149.86, 170.18)),
    "L2": ("RoyalNode:RN_TWO_PIN_POWER_PART", "Coilcraft XAL7030-222MEC", (248.92, 124.46)),
}

FOOTPRINT_MAP = {
    "MOD1": "RoyalNode:MOD1_XIAO_NRF52840_SOCKET_C53202181_RC",
    "MOD2": "RoyalNode:MOD2_E22_900M33S_JLC_C22399506_RC",
    "U1": "RoyalNode:U1_BQ25798_RQM0029A_RC",
    "U2": "RoyalNode:U2_LM66100_DCK0006A_SC70_6_RC",
    "U3": "RoyalNode:U3_TPS61088_RHL0020A_THERMALVIAS_RC",
    "U4": "RoyalNode:U4_LTC4365_TSOT23_8_RC",
    "Q1": "RoyalNode:Q_POWER_INFINEON_PG_DSO_8_27_RC",
    "Q2": "RoyalNode:Q_POWER_INFINEON_PG_DSO_8_27_RC",
    "Q3": "RoyalNode:Q_POWER_INFINEON_PG_DSO_8_27_RC",
    "J1": "RoyalNode:J_POWER_XT30PW_M_C431092_RC",
    "J2": "RoyalNode:J_POWER_XT30PW_M_C431092_RC",
    "J3": "RoyalNode:J_LOW_JST_GH_SM02B_GHS_TB_RC",
    "J4": "RoyalNode:J_LOW_JST_GH_SM02B_GHS_TB_RC",
    "L1": "RoyalNode:L1_COILCRAFT_XAL7070_222MEC_RC",
    "L2": "RoyalNode:L2_COILCRAFT_XAL7030_222MEC_RC",
}

CAPTURED_ORDER = [
    "MOD1",
    "MOD2",
    "U1",
    "U2",
    "U3",
    "U4",
    "Q1",
    "Q2",
    "Q3",
    "J1",
    "J2",
    "J3",
    "J4",
    "J5",
    "F1",
    "L1",
    "L2",
]

PASSIVE_SYMBOL = "RoyalNode:RN_TWO_PIN_POWER_PART"
PWR_FLAG_SYMBOL = "RoyalNode:RN_PWR_FLAG"
PWR_FLAGS = [
    ("PF1", "GND", (15.24, 241.30)),
    ("PF2", "USB_VBUS_RAW", (15.24, 248.92)),
    ("PF3", "SOLAR_FUSED", (15.24, 256.54)),
    ("PF4", "SOLAR_PROTECTED", (15.24, 264.16)),
    ("PF5", "BAT_RAW", (15.24, 271.78)),
    ("PF6", "BQ_VBUS", (15.24, 279.40)),
]


def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "::".join(parts)))


def quote(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def parse_pin_blocks(symbol_name: str, lib_text: str) -> dict[str, tuple[float, float, int]]:
    start = lib_text.find(f'  (symbol "{symbol_name}"')
    if start < 0:
        raise SystemExit(f"missing symbol {symbol_name}")
    end = lib_text.find("\n  (symbol \"", start + 1)
    if end < 0:
        end = len(lib_text)
    block = lib_text[start:end]

    pins: dict[str, tuple[float, float, int]] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        if "(pin " not in lines[i]:
            i += 1
            continue
        pin_lines = [lines[i]]
        depth = lines[i].count("(") - lines[i].count(")")
        i += 1
        while i < len(lines) and depth > 0:
            pin_lines.append(lines[i])
            depth += lines[i].count("(") - lines[i].count(")")
            i += 1
        pin_block = "\n".join(pin_lines)
        at = re.search(r"\(at\s+([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)\)", pin_block)
        number = re.search(r'\(number\s+"([^"]+)"', pin_block)
        if at and number:
            pins[number.group(1)] = (float(at.group(1)), float(at.group(2)), int(float(at.group(3))))
    return pins


def top_level_symbol_block(symbol_name: str, lib_text: str) -> str:
    start = lib_text.find(f'  (symbol "{symbol_name}"')
    if start < 0:
        raise SystemExit(f"missing symbol {symbol_name}")
    end = lib_text.find("\n  (symbol \"", start + 1)
    if end < 0:
        end = lib_text.rfind("\n)")
    block = lib_text[start:end].rstrip()
    return block.replace(f'(symbol "{symbol_name}"', f'(symbol "RoyalNode:{symbol_name}"', 1)


def symbol_short_name(lib_id: str) -> str:
    return lib_id.split(":", 1)[1]


def label_endpoint(symbol_x: float, symbol_y: float, pin_x: float, pin_y: float) -> tuple[float, float, int]:
    abs_x = symbol_x + pin_x
    abs_y = symbol_y - pin_y
    if pin_x <= 0:
        return abs_x - WIRE_STUB_MM, abs_y, 180
    return abs_x + WIRE_STUB_MM, abs_y, 0


def wire_for_pin(ref: str, pin: str, symbol_x: float, symbol_y: float, pin_x: float, pin_y: float) -> str:
    pin_abs_x = symbol_x + pin_x
    pin_abs_y = symbol_y - pin_y
    label_x, label_y, _ = label_endpoint(symbol_x, symbol_y, pin_x, pin_y)
    return f'''  (wire
    (pts
      (xy {pin_abs_x:.2f} {pin_abs_y:.2f})
      (xy {label_x:.2f} {label_y:.2f})
    )
    (stroke
      (width 0)
      (type default)
    )
    (uuid "{stable_uuid("wire", ref, pin)}")
  )'''


def global_label(ref: str, pin: str, net: str, x: float, y: float, angle: int) -> str:
    return f'''  (global_label "{quote(net)}"
    (shape bidirectional)
    (at {x:.2f} {y:.2f} {angle})
    (fields_autoplaced yes)
    (effects
      (font
        (size 1.27 1.27)
      )
      (justify left)
    )
    (uuid "{stable_uuid("label", ref, pin, net)}")
    (property "Intersheetrefs" "${{INTERSHEET_REFS}}"
      (at {x:.2f} {y:.2f} {angle})
      (effects
        (font
          (size 1.27 1.27)
        )
        (hide yes)
      )
    )
  )'''


def no_connect(ref: str, pin: str, symbol_x: float, symbol_y: float, pin_x: float, pin_y: float) -> str:
    return f'''  (no_connect
    (at {symbol_x + pin_x:.2f} {symbol_y - pin_y:.2f})
    (uuid "{stable_uuid("nc", ref, pin)}")
  )'''


def placed_symbol(
    ref: str,
    lib_id: str,
    value: str,
    x: float,
    y: float,
    pins: list[str],
    *,
    footprint: str = "",
    in_bom: bool = True,
    on_board: bool = True,
) -> str:
    pin_entries = "\n".join(
        f'''    (pin "{quote(pin)}"
      (uuid "{stable_uuid("pin", ref, pin)}")
    )'''
        for pin in pins
    )
    return f'''  (symbol
    (lib_id "{quote(lib_id)}")
    (at {x:.2f} {y:.2f} 0)
    (unit 1)
    (exclude_from_sim no)
    (in_bom {"yes" if in_bom else "no"})
    (on_board {"yes" if on_board else "no"})
    (dnp no)
    (uuid "{stable_uuid("symbol", ref)}")
    (property "Reference" "{quote(ref)}"
      (at {x:.2f} {y - 24.0:.2f} 0)
      (effects
        (font
          (size 1.27 1.27)
        )
      )
    )
    (property "Value" "{quote(value)}"
      (at {x:.2f} {y + 24.0:.2f} 0)
      (effects
        (font
          (size 1.27 1.27)
        )
      )
    )
    (property "Footprint" "{quote(footprint)}"
      (at {x:.2f} {y:.2f} 0)
      (effects
        (font
          (size 1.27 1.27)
        )
        (hide yes)
      )
    )
    (property "Datasheet" "~"
      (at {x:.2f} {y:.2f} 0)
      (effects
        (font
          (size 1.27 1.27)
        )
        (hide yes)
      )
    )
{pin_entries}
    (instances
      (project "RoyalNode"
        (path "/{stable_uuid("path", ref)}"
          (reference "{quote(ref)}")
          (unit 1)
        )
      )
    )
  )'''


def text_block(text: str, x: float, y: float, size: float = 1.8) -> str:
    return f'''  (text "{quote(text)}"
    (exclude_from_sim no)
    (at {x:.2f} {y:.2f} 0)
    (effects
      (font
        (size {size:.2f} {size:.2f})
      )
      (justify left top)
    )
    (uuid "{stable_uuid("text", text, str(x), str(y))}")
  )'''


def passive_position(index: int) -> tuple[float, float]:
    rows_per_column = 22
    column = index // rows_per_column
    row = index % rows_per_column
    return 335.28 + column * 50.80, 35.56 + row * 7.62


def main() -> None:
    rows = list(csv.DictReader(SEED.open(newline="", encoding="utf-8")))
    passive_rows = list(csv.DictReader(PASSIVE_SEED.open(newline="", encoding="utf-8")))
    by_ref: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_ref[row["Reference"]].append(row)

    lib_text = SYMBOL_LIB.read_text(encoding="utf-8")
    symbol_pins = {
        ref: parse_pin_blocks(symbol_short_name(symbol[0]), lib_text)
        for ref, symbol in SYMBOL_MAP.items()
    }
    used_symbol_names = sorted(
        {symbol_short_name(SYMBOL_MAP[ref][0]) for ref in CAPTURED_ORDER}
        | {symbol_short_name(PASSIVE_SYMBOL), symbol_short_name(PWR_FLAG_SYMBOL)}
    )
    embedded_symbols = "\n".join(top_level_symbol_block(name, lib_text) for name in used_symbol_names)

    body: list[str] = []
    body.append(text_block(
        "Generated Rev A capture scaffold from SCHEMATIC_CAPTURE_SEED_REV_A.csv.\\n"
        "Symbols use global labels for reviewable net intent; final passives, footprints, and routed wires remain pending.",
        20.0,
        20.0,
        1.6,
    ))
    body.append(text_block(
        "Two-terminal power-path parts and support passives are captured with RN_TWO_PIN_POWER_PART.\\n"
        "Exact passive footprints remain pending footprint release and layout review.",
        202.0,
        268.0,
        1.3,
    ))

    for ref in CAPTURED_ORDER:
        lib_id, value, (x, y) = SYMBOL_MAP[ref]
        seed_pins = [row["Pin"] for row in by_ref[ref]]
        available_pins = symbol_pins[ref]
        missing = [pin for pin in seed_pins if pin not in available_pins]
        if missing:
            raise SystemExit(f"{ref} missing pins in symbol: {', '.join(missing)}")
        body.append(placed_symbol(ref, lib_id, value, x, y, seed_pins, footprint=FOOTPRINT_MAP.get(ref, "")))
        for row in by_ref[ref]:
            pin = row["Pin"]
            net = row["Net"]
            pin_x, pin_y, _ = available_pins[pin]
            if net == "NC":
                body.append(no_connect(ref, pin, x, y, pin_x, pin_y))
                continue
            lx, ly, angle = label_endpoint(x, y, pin_x, pin_y)
            body.append(wire_for_pin(ref, pin, x, y, pin_x, pin_y))
            body.append(global_label(ref, pin, net, lx, ly, angle))

    passive_pins = parse_pin_blocks(symbol_short_name(PASSIVE_SYMBOL), lib_text)
    for index, row in enumerate(passive_rows):
        ref = row["Reference"]
        value = row["Value"]
        x, y = passive_position(index)
        body.append(placed_symbol(ref, PASSIVE_SYMBOL, value, x, y, ["1", "2"], footprint=row.get("Footprint", "")))
        for pin, net in [("1", row["Pin 1 Net"]), ("2", row["Pin 2 Net"])]:
            pin_x, pin_y, _ = passive_pins[pin]
            lx, ly, angle = label_endpoint(x, y, pin_x, pin_y)
            body.append(wire_for_pin(ref, pin, x, y, pin_x, pin_y))
            body.append(global_label(ref, pin, net, lx, ly, angle))

    pwr_flag_pins = parse_pin_blocks(symbol_short_name(PWR_FLAG_SYMBOL), lib_text)
    for ref, net, (x, y) in PWR_FLAGS:
        body.append(placed_symbol(ref, PWR_FLAG_SYMBOL, "PWR_FLAG", x, y, ["1"], in_bom=False, on_board=False))
        pin_x, pin_y, _ = pwr_flag_pins["1"]
        lx, ly, angle = label_endpoint(x, y, pin_x, pin_y)
        body.append(wire_for_pin(ref, "1", x, y, pin_x, pin_y))
        body.append(global_label(ref, "1", net, lx, ly, angle))

    schematic = f'''(kicad_sch
  (version 20250114)
  (generator "royalnode_capture_generator")
  (generator_version "1")
  (uuid "{stable_uuid("schematic", "root")}")
  (paper "A3")
  (title_block
    (title "RoyalNode Rev A")
    (date "2026-07-24")
    (rev "A")
    (company "RoyalNode")
    (comment 1 "Solar-powered 2 W LoRa repeater carrier")
    (comment 2 "Generated from SCHEMATIC_CAPTURE_SEED_REV_A.csv")
  )
  (lib_symbols
{embedded_symbols}
  )
{chr(10).join(body)}
)
'''
    SCHEMATIC.write_text(schematic, encoding="utf-8")
    print(f"Generated {SCHEMATIC.relative_to(ROOT)}")
    print(f"Captured references: {', '.join(CAPTURED_ORDER)}")
    print(f"Captured passives: {len(passive_rows)}")
    print(f"Captured power flags: {len(PWR_FLAGS)}")


if __name__ == "__main__":
    main()
