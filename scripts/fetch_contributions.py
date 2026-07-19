#!/usr/bin/env python3
"""
Fetch GitHub contribution calendar for a user and save as data/contributions.json.

Improvements:
- argparse support (--username / -u)
- directory creation
- HTTP timeout and status validation
- graceful network error handling
- robust parsing with clear failures
- small validation for reasonable number of day cells
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

DEFAULT_USERNAME = "harshmeena9977-ops"
DEFAULT_TIMEOUT = 30
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "contributions.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; HarshPortfolio/1.0)"
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Fetch GitHub contributions calendar")
    p.add_argument("-u", "--username", default=DEFAULT_USERNAME, help="GitHub username")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout seconds")
    return p.parse_args()


def fetch_contributions_html(username: str, timeout: int) -> str:
    url = f"https://github.com/users/{username}/contributions"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
    except requests.RequestException as e:
        raise SystemExit(f"Network error while fetching contributions for {username}: {e}")
    if resp.status_code != 200:
        raise SystemExit(f"Failed to fetch contributions page (HTTP {resp.status_code}) for {username} at {url}")
    return resp.text


def extract_days_from_html(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    days = []

    # Primary selector: the ContributionCalendar table uses td elements with data-date
    for rect in soup.select("td.ContributionCalendar-day"):
        date = rect.get("data-date")
        level = rect.get("data-level")
        if date:
            try:
                lvl = int(level) if level is not None else 0
            except ValueError:
                lvl = 0
            days.append({"date": date, "level": max(0, min(lvl, 5))})

    # Fallback: search any element with data-date/data-level attributes (more robust)
    if not days:
        for el in soup.select("[data-date]"):
            date = el.get("data-date")
            level = el.get("data-level")
            if date and level is not None:
                try:
                    lvl = int(level)
                except ValueError:
                    lvl = 0
                days.append({"date": date, "level": max(0, min(lvl, 5))})

    return sorted(days, key=lambda x: x["date"])


def validate_days(days: List[Dict]) -> None:
    if not days:
        raise SystemExit("Parsing failed: no contribution day elements were found (GitHub markup may have changed).")
    # Expect roughly 365 days (53 weeks * 7 day grid = 371 possible cells). Allow some tolerance.
    if len(days) < 300:
        # Not fatal but warn and fail to avoid silently producing incomplete data.
        raise SystemExit(f"Unexpected number of contribution day cells found: {len(days)} (expected ~365). Parsing likely failed.")


def save_output(username: str, days: List[Dict]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output = {
        "username": username,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "days": days,
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2)
    print(f"Saved {len(days)} contribution days to {OUTPUT_FILE}")


def main() -> None:
    args = parse_args()
    html = fetch_contributions_html(args.username, args.timeout)
    days = extract_days_from_html(html)
    validate_days(days)
    save_output(args.username, days)


if __name__ == "__main__":
    main()
