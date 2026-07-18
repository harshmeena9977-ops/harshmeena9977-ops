import json
from datetime import datetime, timedelta

WIDTH = 860
HEIGHT = 170

CELL = 12
GAP = 3

LEFT = 40
TOP = 35

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0"
]

with open("data/contributions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

contributions = {
    item["date"]: item["level"]
    for item in data["days"]
}

today = datetime.now().date()

# Last 365 days
start_date = today - timedelta(days=364)

# Align to Sunday
start_date -= timedelta(days=(start_date.weekday() + 1) % 7)

svg = []

svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>
    .cell {{
        opacity: 0;
        transform-box: fill-box;
        transform-origin: center;
        animation: reveal 0.35s ease-out forwards;
    }}

    @keyframes reveal {{
        from {{
            opacity: 0;
            transform: translateY(-8px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .title {{
        font-family: monospace;
        font-size: 14px;
        fill: #8b949e;
    }}

    .footer {{
        font-family: monospace;
        font-size: 12px;
        fill: #8b949e;
    }}
</style>

<text x="40" y="20" class="title">
harsh@github ~ $ ./contributions.sh
</text>
''')

# Generate 53 weeks x 7 days
current_date = start_date

for week in range(53):

    for day in range(7):

        date_string = current_date.isoformat()

        level = contributions.get(date_string, 0)
        level = max(0, min(level, 5))

        x = LEFT + week * (CELL + GAP)
        y = TOP + day * (CELL + GAP)

        delay = (week * 7 + day) * 0.008

        svg.append(f'''
<rect
    class="cell"
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="3"
    fill="{PALETTE[level]}"
    style="animation-delay:{delay:.3f}s">
    <title>{date_string}: contribution level {level}</title>
</rect>
''')

        current_date += timedelta(days=1)

svg.append('''
<text x="40" y="155" class="footer">
Less
</text>
''')

for i in range(6):

    x = 75 + i * 18

    svg.append(f'''
<rect
    x="{x}"
    y="146"
    width="12"
    height="12"
    rx="3"
    fill="{PALETTE[i]}"/>
''')

svg.append('''
<text x="190" y="155" class="footer">
More
</text>

</svg>
''')

with open("contrib-heatmap.svg", "w", encoding="utf-8") as file:
    file.write("".join(svg))

print("Animated contribution heatmap generated successfully.")
