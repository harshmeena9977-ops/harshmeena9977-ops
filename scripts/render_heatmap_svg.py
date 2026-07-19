import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = REPO_ROOT / "data" / "contributions.json"
DEFAULT_OUTPUT = REPO_ROOT / "contrib-heatmap.svg"
WIDTH = 860
HEIGHT = 190
CELL = 12
GAP = 3
LEFT = 40
TOP = 35
PALETTE = ["#111827", "#0f766e", "#0ea5a4", "#34d399", "#6ee7b7", "#a7f3d0"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a contribution heatmap SVG")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Contribution JSON input path")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="SVG output path")
    parser.add_argument("--width", type=int, default=WIDTH, help="SVG width")
    parser.add_argument("--height", type=int, default=HEIGHT, help="SVG height")
    return parser.parse_args()


def load_contributions(path: Path) -> tuple[dict, dict[str, int]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    contributions = {item["date"]: item["level"] for item in payload.get("days", [])}
    return payload, contributions


def build_svg(payload: dict, contributions: dict[str, int], width: int, height: int) -> str:
    summary = payload.get("summary", {})
    today = datetime.now().date()
    start_date = today - timedelta(days=364)
    start_date -= timedelta(days=(start_date.weekday() + 1) % 7)

    lines: list[str] = []
    lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
.cell {{ }}
.title {{ font-family: monospace; font-size: 14px; fill: #cbd5e1; }}
.meta {{ font-family: monospace; font-size: 12px; fill: #94a3b8; }}
</style>
<text x="40" y="20" class="title">harsh@github ~ $ ./contributions.sh</text>
<text x="40" y="42" class="meta">{payload.get('username', 'unknown')} • {summary.get('active_days', 0)} active days • {summary.get('total_contributions', 0)} total contribution points</text>
''')

    current_date = start_date
    for week in range(53):
        for day in range(7):
            date_string = current_date.isoformat()
            level = max(0, min(contributions.get(date_string, 0), 5))
            x = LEFT + week * (CELL + GAP)
            y = TOP + day * (CELL + GAP)
            lines.append(
                f'''<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[level]}"><title>{date_string}: level {level}</title></rect>'''
            )
            current_date += timedelta(days=1)

    lines.append('''<text x="40" y="155" class="meta">Less</text>''')
    for index in range(6):
        x = 75 + index * 18
        lines.append(f'''<rect x="{x}" y="146" width="12" height="12" rx="3" fill="{PALETTE[index]}" />''')
    lines.append('''<text x="190" y="155" class="meta">More</text></svg>''')
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    payload, contributions = load_contributions(args.input)
    svg = build_svg(payload, contributions, args.width, args.height)
    args.output.write_text(svg, encoding="utf-8")
    print(f"Generated {args.output}")


if __name__ == "__main__":
    main()
