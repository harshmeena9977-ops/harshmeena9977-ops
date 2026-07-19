#!/usr/bin/env python3
"""Generate ASCII identity SVG with terminal-inspired visual."""
from __future__ import annotations

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "harsh-ascii.svg"
WIDTH = 370
HEIGHT = 430

ASCII_ART = [
    "                 .-''''-.",
    "              .-'        '-.",
    "            .'              '.",
    "           /   DATA • AI     \\",
    "          /     ENGINEER     \\",
    "         |   __  __  __  __   |",
    "         |  / / / / / / / /   |",
    "         | /_/ /_/ /_/ /_/    |",
    "         |   PYTHON • SQL     |",
    "          \\      POWER BI     /",
    "           '.    DJANGO     .'",
    "             '-.  REST  .-'",
    "                '------'",
    "",
    "              .-========-.",
    "             /  HARSH MEENA \\",
    "            /   DATA ANALYST \\",
    "           |   AI/ML + BACKEND |",
    "           |   PYTHON • SQL    |",
    "           |   POWER BI • EXCEL|",
    "            \\               /",
    "             '-------------'",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate ASCII identity SVG")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="SVG output path")
    parser.add_argument("--width", type=int, default=WIDTH, help="SVG width")
    parser.add_argument("--height", type=int, default=HEIGHT, help="SVG height")
    return parser.parse_args()


def build_svg(width: int, height: int) -> str:
    lines = []
    lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
.ascii {{ font-family: monospace; font-size: 11px; fill: #cbd5e1; opacity: 0; animation: typeIn 0.45s ease-out forwards; }}
@keyframes typeIn {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: translateX(0); }} }}
.title {{ font-family: monospace; font-size: 14px; fill: #94a3b8; }}
</style>
<text x="20" y="25" class="title">harsh@github ~ $ whoami</text>
''')

    start_y = 55
    for index, line in enumerate(ASCII_ART):
        y = start_y + index * 13
        delay = index * 0.05
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        lines.append(f'''<text x="20" y="{y}" class="ascii" style="animation-delay:{delay:.2f}s">{escaped_line}</text>''')

    lines.append("</svg>")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    svg = build_svg(args.width, args.height)
    args.output.write_text(svg, encoding="utf-8")
    print(f"Generated {args.output}")


if __name__ == "__main__":
    main()
