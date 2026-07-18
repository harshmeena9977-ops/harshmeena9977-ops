import json
import re
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

USERNAME = "harshmeena9977-ops"
URL = f"https://github.com/users/{USERNAME}/contributions"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for rect in soup.select("td.ContributionCalendar-day"):
    date = rect.get("data-date")
    count = rect.get("data-level")

    if date:
        days.append({
            "date": date,
            "level": int(count or 0)
        })

# Fallback parser for GitHub markup changes
if not days:
    for element in soup.select("[data-date]"):
        date = element.get("data-date")
        level = element.get("data-level")

        if date and level is not None:
            days.append({
                "date": date,
                "level": int(level)
            })

days = sorted(days, key=lambda x: x["date"])

output = {
    "username": USERNAME,
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "days": days
}

with open("data/contributions.json", "w", encoding="utf-8") as file:
    json.dump(output, file, indent=2)

print(f"Saved {len(days)} contribution days.")
