# Changelog

## v0.3.0 - 2026-11-12
### Added
- Legutóbbi ismert ár: ha egy kúthoz aznap nincs friss ár, a legutóbbi ismert ár látszik „!” jellel és a legutóbbi frissítés dátumával – a kártyákon, a diagramon (üres karika), a buborékban és a táblázatban is
- Új adatmezők: `stale`, `asOf`; a napi feladat nem friss árat is felvehet, 5%-os korláttal az országos átlaghoz
- Projektstruktúra a dev-workflow szerint: `src/`, `ops/`, `tests/`, README, VERSION, CHANGELOG, .gitignore
- Smoke teszt (`tests/smoke_test.py`) headless Chrome-mal, mintaadattal
- A napi feladat utasítása verziókezelve: `ops/scheduled-task-prompt.md`

## v0.2.0 - 2026-11-11
### Changed
- AVIA: a vecsési kút (Üllői út 812.) helyett a Keresztúri út 108/a-n lévő kút (X. ker.), mert a vecsésihez nem volt friss ár
### Added
- Szabály: autópályás árak egyik láncból sem kerülhetnek be
- Verziószám a láblécben

## v0.1.0 - 2026-11-11
### Added
- Első kiadás: mai árkártyák, üzemanyag-fajta választó (95, prémium 95, 100), 30 napos diagram kikapcsolható kutakkal, táblázatos nézet, világos és sötét mód
- Adattárolás az artifact adatbázisában (`prices/YYYY-MM-DD`)
- Napi ütemezett frissítés 7:03-kor (Europe/Budapest)

> A v0.1.0–v0.3.0 még git nélkül készült (akkor v0.1–v0.3 néven). Az első commit a v0.3.0 állapota; a korábbi verziók csak ebben a naplóban szerepelnek.
