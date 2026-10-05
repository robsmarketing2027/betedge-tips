#!/usr/bin/env python3
"""Download all Puttó draw results from bet.szerencsejatek.hu into a CSV.

Iterates ISO (year, week, day) from START to today; each page lists one day's draws.
Usage: python3 scrape_putto.py [output.csv]
"""
import csv, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

URL = "https://bet.szerencsejatek.hu/jatekok/putto/sorsolasok?year={}&week={}&day={}"
START = date.fromisocalendar(2015, 6, 1)
ROW = re.compile(
    r"<div>(\d{4})\. (\d\d)\. (\d\d)\. (\d\d:\d\d)</div>\s*</td>\s*<td>\s*<div>(\d+)</div>\s*</td>"
    r"\s*<td>\s*<div>([\d, ]+)</div>\s*</td>\s*<td>\s*<div>(\d+)</div>")


def fetch(d: date, retries: int = 6):
    y, w, wd = d.isocalendar()
    for i in range(retries):
        try:
            req = urllib.request.Request(URL.format(y, w, wd), headers={"User-Agent": "Mozilla/5.0"})
            html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
            rows = []
            for yy, mm, dd, hm, no, a, b in ROW.findall(html):
                nums = [int(x) for x in a.split(",")]
                assert len(nums) == 8, (d, no, a)
                rows.append([f"{yy}-{mm}-{dd} {hm}", y, w, wd, int(no), *nums, int(b)])
            return d, rows
        except Exception as e:  # network hiccups: retry with backoff
            err = e
            time.sleep(2 ** i)
    print(f"FAILED {d}: {err}", file=sys.stderr)
    return d, None


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "putto_draws.csv"
    days = [START + timedelta(n) for n in range((date.today() - START).days + 1)]
    results = {}
    with ThreadPoolExecutor(16) as ex:
        for i, (d, rows) in enumerate(ex.map(fetch, days), 1):
            results[d] = rows
            if i % 200 == 0:
                print(f"{i}/{len(days)}", file=sys.stderr)
    failed = [d for d, r in results.items() if r is None]
    with open(out, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["datetime", "iso_year", "iso_week", "iso_day", "draw_no",
                     *[f"A{i}" for i in range(1, 9)], "B"])
        all_rows = sorted((r for rows in results.values() if rows for r in rows), key=lambda r: r[0])
        wr.writerows(all_rows)
    print(f"{len(all_rows)} draws written to {out}; failed days: {failed}", file=sys.stderr)


if __name__ == "__main__":
    main()
