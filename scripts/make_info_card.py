#!/usr/bin/env python3
"""Generate neofetch-style info card SVG."""
from __future__ import annotations

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "info-card.svg"
WIDTH = 490
HEIGHT = 430

LINES = [
    ("NAME", "Harsh Meena"),
    ("ROLE", "Data Analyst"),
    ("FOCUS", "AI/ML + Backend"),
    ("EDUCATION", "B.Tech CSE '25"),
    ("", ""),
    ("STACK", "Python • SQL • Power BI"),
    ("BACKEND", "Django • REST APIs"),
    ("ANALYTICS", "Pandas • Excel • DAX"),
    ("", ""),
    ("PROJECTS", "End-to-End Analytics"),
    ("STATUS", "Open to Opportunities"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate neofetch-style info card SVG")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="SVG output path")
    parser.add_argument("--width", type=int, default=WIDTH, help="SVG width")
    parser.add_argument("--height", type=int, default=HEIGHT, help="SVG height")
    return parser.parse_args()


def build_svg(width: int, height: int) -> str:
    lines = []
    lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
.title {{ font-family: monospace; font-size: 18px; font-weight: bold; fill: #e2e8f0; }}
.subtitle {{ font-family: monospace; font-size: 13px; fill: #94a3b8; }}
.key {{ font-family: monospace; font-size: 13px; font-weight: bold; fill: #cbd5e1; }}
.value {{ font-family: monospace; font-size: 13px; fill: #f8fafc; }}
.line {{ stroke: #334155; stroke-width: 1; opacity: 0.6; }}
.row {{ opacity: 0; animation: fadeIn 0.55s ease-out forwards; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateX(8px); }} to {{ opacity: 1; transform: translateX(0); }} }}
</style>
<text x="20" y="30" class="title">HARSH@GITHUB</text>
<text x="20" y="52" class="subtitle">────────────────────────────────────────────</text>
<text x="20" y="78" class="subtitle">DATA • AI • SOFTWARE</text>
<line x1="20" y1="92" x2="465" y2="92" class="line"/>
''')

    start_y = 120
    for index, (key, value) in enumerate(LINES):
        if not key and not value:
            continue
        y = start_y + index * 24
        delay = index * 0.11
        lines.append(f'''<g class="row" style="animation-delay:{delay:.2f}s"><text x="20" y="{y}" class="key">{key}</text><text x="145" y="{y}" class="value">{value}</text></g>''')

    lines.append('''<line x1="20" y1="405" x2="465" y2="405" class="line"/><text x="20" y="425" class="subtitle">STATUS: BUILDING • LEARNING • SHIPPING</text></svg>''')
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    svg = build_svg(args.width, args.height)
    args.output.write_text(svg, encoding="utf-8")
    print(f"Generated {args.output}")


if __name__ == "__main__":
    main()
