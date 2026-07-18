from pathlib import Path

WIDTH = 490
HEIGHT = 430

lines = [
    ("NAME", "Harsh Meena"),
    ("ROLE", "Data Analyst"),
    ("FOCUS", "AI/ML + Backend"),
    ("EDUCATION", "B.Tech CSE '25"),
    ("", ""),
    ("STACK", "Python • SQL • Power BI"),
    ("BACKEND", "Django • REST APIs"),
    ("ANALYTICS", "Pandas • Excel • DAX"),
    ("", ""),
    ("PROJECTS", "5+ End-to-End"),
    ("DATA", "22,000+ Records"),
    ("STATUS", "Open to Opportunities"),
]

svg = []

svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.title {{
    font-family: monospace;
    font-size: 18px;
    font-weight: bold;
    fill: #8b949e;
}}

.subtitle {{
    font-family: monospace;
    font-size: 13px;
    fill: #8b949e;
}}

.key {{
    font-family: monospace;
    font-size: 13px;
    font-weight: bold;
    fill: #8b949e;
}}

.value {{
    font-family: monospace;
    font-size: 13px;
    fill: #8b949e;
}}

.line {{
    stroke: #8b949e;
    stroke-width: 1;
    opacity: 0.5;
}}

.row {{
    opacity: 0;
    animation: fadeIn 0.5s ease-out forwards;
}}

@keyframes fadeIn {{
    from {{
        opacity: 0;
        transform: translateX(10px);
    }}

    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

</style>

<text x="20" y="30" class="title">
HARSH@GITHUB
</text>

<text x="20" y="52" class="subtitle">
────────────────────────────────────────────
</text>

<text x="20" y="78" class="subtitle">
DATA • AI • SOFTWARE
</text>

<line x1="20" y1="92" x2="465" y2="92" class="line"/>
''')

start_y = 120

for index, (key, value) in enumerate(lines):

    if not key and not value:
        continue

    y = start_y + index * 24
    delay = index * 0.12

    svg.append(f'''
<g class="row" style="animation-delay:{delay:.2f}s">

<text
    x="20"
    y="{y}"
    class="key">
    {key}
</text>

<text
    x="145"
    y="{y}"
    class="value">
    {value}
</text>

</g>
''')

svg.append('''
<line x1="20" y1="405" x2="465" y2="405" class="line"/>

<text x="20" y="425" class="subtitle">
STATUS: BUILDING • LEARNING • SHIPPING
</text>

</svg>
''')

Path("info-card.svg").write_text(
    "".join(svg),
    encoding="utf-8"
)

print("Info card generated successfully.")
