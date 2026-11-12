# Benzinárak – XVIII–XIX. kerület környéke

Egy weboldal, amely négy budapesti benzinkút napi benzinárait és az országos átlagot mutatja, 30 napos trenddiagrammal. Minden reggel automatikusan frissül.

Figyelt kutak: OMV (XXIII., Nagykőrösi út 349.), AVIA (X., Keresztúri út 108/a), M.Petrol (XIX., Citroën utca 2.), Dallas (X., Száva utca 5–7.), valamint az országos átlag (holtankoljak.hu).

Repó: https://github.com/Edemkee/gas-prices

## Hogyan működik

- **Oldal:** `src/index.html`, egyetlen önálló HTML-fájl, külső könyvtár nélkül. Jelenleg claude.ai artifactként fut: https://claude.ai/artifact/H8qb55y2bJKe6Ewr1kxdFK
- **Adatok:** az artifact saját adatbázisában, napi egy rekorddal (`prices/YYYY-MM-DD`). Az adatmodell leírása a `CLAUDE.md`-ben van.
- **Napi frissítés:** egy ütemezett Claude-feladat minden nap 7:03-kor (budapesti idő) összegyűjti az árakat, és beírja az adatbázisba. Az utasítása: `ops/scheduled-task-prompt.md`.
- Ha egy kúthoz aznap nincs friss ár, az oldal a legutóbbi ismert árat mutatja, „!” jellel.

## Futtatás helyben

A `src/index.html` böngészőben megnyitható, de adatbázis nélkül csak az üres állapotot mutatja. Mintaadattal a smoke teszt rendereli le (lent).

## Tesztelés

```
pip install playwright
python3 tests/smoke_test.py                  # ha a Playwright saját Chromiumja telepítve van
CHROME=/path/to/chrome python3 tests/smoke_test.py
```

A teszt kitalált mintaadattal, világos és sötét módban, asztali és mobil szélességben rendereli az oldalt, és ellenőrzi a kártyákat, a „!” jelölést, a diagramot és a kutak ki-be kapcsolását. A képernyőképek a `tests/out/` mappába kerülnek (ez nincs verziókezelve).

## Dokumentumok

- `PLAN.md` – teendők, ötletek, állapotokkal
- `CLAUDE.md` – döntések és munkaszabályok
- `CHANGELOG.md` – verziónkénti változások
- `VERSION` – aktuális verzió
