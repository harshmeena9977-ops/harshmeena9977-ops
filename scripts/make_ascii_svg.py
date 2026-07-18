from pathlib import Path

WIDTH = 370
HEIGHT = 430

ASCII_ART = [
    "                 .-''''-.",
    "              .-'        '-.",
    "            .'              '.",
    "           /                  \\",
    "          /     .------.       \\",
    "         |     /  .--.  \\       |",
    "         |    |  (    )  |      |",
    "         |    |   '--'   |      |",
    "         |     \\        /       |",
    "          \\     '------'       /",
    "           '.                .'",
    "             '-.          .-'",
    "                '--------'",
    "",
    "              .-========-.",
    "             /            \\",
    "            /              \\",
    "           |   DATA        |",
    "           |   ANALYST     |",
    "           |               |",
    "           |   PYTHON      |",
    "           |   SQL         |",
    "           |   POWER BI    |",
    "            \\              /",
    "             '------------'",
]

svg = []

svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>
.ascii {{
    font-family: monospace;
    font-size: 11px;
    fill: #8b949e;
    opacity: 0;
    animation: typeIn 0.5s ease-out forwards;
}}

@keyframes typeIn {{
    from {{
        opacity: 0;
        transform: translateX(-10px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

.title {{
    font-family: monospace;
    font-size: 14px;
    fill: #8b949e;
}}
</style>

<text x="20" y="25" class="title">
harsh@github ~ $ whoami
</text>
''')

start_y = 55

for index, line in enumerate(ASCII_ART):

    y = start_y + index * 14
    delay = index * 0.08

    escaped_line = (
        line
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    svg.append(f'''
<text
    x="20"
    y="{y}"
    class="ascii"
    style="animation-delay:{delay:.2f}s">
    {escaped_line}
</text>
''')

svg.append("</svg>")

Path("harsh-ascii.svg").write_text(
    "".join(svg),
    encoding="utf-8"
)

print("ASCII SVG generated successfully.")
