"""Smoke test for src/index.html.

Renders the page in headless Chrome with a mocked `claude.use("db")` that serves
sample (fake) price records, then checks the main behaviour:
  - the five cards render, with the latest price
  - a missing day falls back to the last known price and shows the "!" badge
  - a record stored as stale (stale: true) shows the "!" badge
  - a station that never had a price shows "nincs adat"
  - the chart renders, and clicking a legend chip hides that series
  - the graphics card board (collection "gpus") renders its three cards, carries a
    missing Árukereső price over with "!", switches to the Alza prices, and draws its chart
  - no JavaScript errors

Run:  python3 tests/smoke_test.py            (needs: pip install playwright, plus Chrome/Chromium)
      CHROME=/path/to/chrome python3 tests/smoke_test.py
Screenshots go to tests/out/ (git-ignored).
"""
import asyncio
import datetime
import json
import os
import pathlib
import sys

from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "src" / "index.html"
OUT = ROOT / "tests" / "out"


def sample_days():
    """10 days of fake data. Last day: omv fresh, avia missing (carried over),
    mpetrol stored stale, dallas never had a price."""
    base = datetime.date(2026, 11, 2)
    days = []
    for i in range(10):
        d = base + datetime.timedelta(days=i)
        last = i == 9
        days.append({
            "date": d.isoformat(),
            "updatedAt": f"{d.isoformat()}T06:05:00Z",
            "national": {"b95": 610 - i},
            "stations": {
                "omv": {"b95": 605 - i, "src": "petromap.eu"},
                "avia": {"b95": None if last else 603 - i, "src": None if last else "petromap.eu"},
                "mpetrol": ({"b95": 590, "src": "fuelo.net", "stale": True, "asOf": "2026-11-08"}
                            if last else {"b95": 600 - i, "src": "petromap.eu"}),
                "dallas": {"b95": None, "src": None, "note": "nem volt friss ár"},
            },
        })
    return days


def sample_gpu_days():
    """6 days of fake graphics card prices. Last day: 5070 Ti Gaming OC fresh,
    5070 Ti Eagle without an Árukereső price (carried over) but with an Alza price,
    5080 Gaming OC fresh."""
    base = datetime.date(2026, 11, 6)
    days = []
    for i in range(6):
        d = base + datetime.timedelta(days=i)
        last = i == 5
        days.append({
            "date": d.isoformat(),
            "updatedAt": f"{d.isoformat()}T09:40:00Z",
            "cards": {
                "g5070ti_gaming": {"low": 500000 - i * 1000, "offers": 20, "alza": 510000},
                "g5070ti_eagle": ({"low": None, "offers": None, "alza": 470000, "alzaStock": "Raktáron",
                                   "note": "az Árukereső nem volt elérhető"}
                                  if last else {"low": 480000, "offers": 15, "alza": 471000}),
                "g5080_gaming": {"low": 650000 + i * 2000, "offers": 30, "alza": None},
            },
        })
    return days


def mocked_html():
    html = PAGE.read_text(encoding="utf-8")
    data = {"prices": sample_days(), "gpus": sample_gpu_days()}
    mock = (
        "<script>window.claude={use:async n=>n==='db'?{collection:(c)=>({orderBy:()=>({limit:()=>({"
        "onSnapshot:(cb)=>{setTimeout(()=>cb({metadata:{fromCache:false},docs:(%s[c]||[]).map(d=>({data:()=>d}))}),30);"
        "return()=>{}}})})})}:null};</script>" % json.dumps(data)
    )
    return html.replace("<body>", "<body>" + mock, 1)


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    test_file = OUT / "smoke.html"
    test_file.write_text(mocked_html(), encoding="utf-8")
    failures = []

    def check(cond, msg):
        print(("ok   " if cond else "FAIL ") + msg)
        if not cond:
            failures.append(msg)

    async with async_playwright() as p:
        kw = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
        browser = await p.chromium.launch(**kw)
        for scheme, width in (("light", 1000), ("dark", 390)):
            page = await browser.new_page(viewport={"width": width, "height": 900}, color_scheme=scheme)
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            await page.goto(test_file.as_uri())
            await page.wait_for_timeout(500)
            tag = f"[{scheme} {width}px]"

            cards = await page.locator("#cards .card").all_inner_texts()
            check(len(cards) == 5, f"{tag} 5 cards rendered")
            omv, avia, mpetrol, dallas = cards[0], cards[1], cards[2], cards[3]
            check("596" in omv and "!" not in omv, f"{tag} OMV shows fresh latest price without '!'")
            check("595" in avia and "!" in avia and "nov. 10." in avia,
                  f"{tag} AVIA missing day falls back to last known price with '!' and its date")
            check("590" in mpetrol and "!" in mpetrol and "nov. 8." in mpetrol,
                  f"{tag} M.Petrol stored-stale price shows '!' with asOf date")
            check("nincs adat" in dallas, f"{tag} Dallas without any price shows 'nincs adat'")

            check(await page.locator("#chart svg path").count() >= 3, f"{tag} chart lines rendered")
            hollow = await page.locator('#chart svg circle[stroke-width="2"]').count()
            check(hollow > 0, f"{tag} chart has markers")

            before = await page.locator("#chart svg path").count()
            await page.locator('.chip[data-key="omv"]').click()
            await page.wait_for_timeout(100)
            after = await page.locator("#chart svg path").count()
            check(after == before - 1, f"{tag} toggling OMV removes its line")
            await page.locator('.chip[data-key="omv"]').click()

            # graphics card board
            g = await page.locator("#g-cards .card").all_inner_texts()
            check(len(g) == 3, f"{tag} 3 graphics card cards rendered")
            if len(g) == 3:
                check("495 000" in g[0].replace("\u00a0", " ") and "!" not in g[0],
                      f"{tag} 5070 Ti Gaming OC shows its fresh Árukereső price")
                check("480 000" in g[1].replace("\u00a0", " ") and "!" in g[1] and "nov. 10." in g[1],
                      f"{tag} 5070 Ti Eagle without today's Árukereső price shows last known with '!'")
                check("Alza ár ma: 470 000" in g[1].replace("\u00a0", " "),
                      f"{tag} 5070 Ti Eagle card shows today's Alza price as cross-check")
            check(await page.locator("#g-chart svg path").count() == 3, f"{tag} graphics card chart lines rendered")
            await page.locator('#g-tabs [data-fuel="alza"]').click()
            await page.wait_for_timeout(100)
            g2 = await page.locator("#g-cards .card").all_inner_texts()
            check(len(g2) == 3 and "470 000" in g2[1].replace("\u00a0", " ") and "nincs adat" in g2[2],
                  f"{tag} switching to Alza shows Alza prices ('nincs adat' where Alza has none)")
            await page.locator('#g-tabs [data-fuel="low"]').click()

            await page.screenshot(path=str(OUT / f"smoke-{scheme}.png"), full_page=True)
            check(not errors, f"{tag} no JavaScript errors {errors if errors else ''}")
            await page.close()
        await browser.close()

    print("\n" + ("PASSED" if not failures else f"FAILED: {len(failures)} check(s)"))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    asyncio.run(main())
