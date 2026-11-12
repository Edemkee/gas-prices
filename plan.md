# Plan

Állapotok: `open`, `in progress`, `rejected`, `done`. Egyszerre legfeljebb egy tétel lehet `in progress`. A döntések indoklása a `CLAUDE.md`-ben van.

| # | Tétel | Állapot | Megjegyzés |
|---|-------|---------|------------|
| 1 | Négy kút beazonosítása, források felkutatása | done | v0.1.0 |
| 2 | Weboldal: mai árkártyák, fajtaválasztó, 30 napos diagram kikapcsolható kutakkal, táblázat, sötét mód | done | v0.1.0 |
| 3 | Perzisztencia: artifact adatbázis, `prices/YYYY-MM-DD`, csak a tulajdonos írhatja | done | v0.1.0 |
| 4 | Napi ütemezett frissítés 7:03-kor | done | v0.1.0; utasítás: `ops/scheduled-task-prompt.md` |
| 5 | AVIA csere: Vecsés → Keresztúri út 108/a | done | v0.2.0 |
| 6 | Autópályás árak kizárása | done | v0.2.0, a felhasználó irányelve |
| 7 | Legutóbbi ismert ár „!” jellel, mind a négy kútra | done | v0.3.0 |
| 8 | Dev-workflow struktúra: README, VERSION, CHANGELOG, .gitignore, `src/`, `ops/`, `tests/` | done | v0.3.0 |
| 9 | Smoke teszt headless Chrome-mal | done | v0.3.0, `tests/smoke_test.py` |
| 10 | GitHub repo összekapcsolása, push, `v0.3.0` tag | open | a felhasználó otthon, a saját gépéről köti össze; a helyi repo és az első commit kész |
| 11 | GitHub secret scanning és push protection bekapcsolása | open | a repo beállításaiban, a 10. után |
| 12 | Az első napi futások átnézése (nov. 12–14.): melyik forrás működik | open | |
| 13 | Dallas (Száva u.): döntés, ha egy hét után sincs ára | open | most nincs ismert ára; a fuelo 656,2 Ft-os becslése ki van szűrve |
| 14 | Napi JSON-export a repóba (`data/YYYY-MM-DD.json`) biztonsági mentésként | open | a 10. után |
| 15 | Figyelmeztetés az oldalon, ha a legutóbbi frissítés több napos | open | |
| 16 | Átköltözés Netlify-ra: oldal + Scheduled Function + Netlify Blobs | open | opció; lásd a megjegyzést lent |
| 17 | CI: GitHub Actions a smoke teszttel minden PR-en | open | kis projekt, opcionális; a 10. után |
| 18 | Gázolaj fül | open | ötlet |
| 19 | A legolcsóbb kút kiemelése a kártyák között | open | ötlet |
| 20 | Heti vagy havi átlag a táblázat alján | open | ötlet |
| 21 | Vecsési AVIA (Üllői út 812.) | rejected | nincs hozzá friss ár; a 5. váltotta |
| 22 | 30 napos visszamenőleges feltöltés | rejected | kutankénti árelőzmény nyilvánosan nem elérhető; kitalált adatot nem írunk |
| 23 | fuelo.net becsült értékei forrásként | rejected | ugyanaz a szám több kútnál, jóval az átlag fölött (656,2 Ft vs. 602 Ft) |

## Megjegyzés a 16. tételhez (Netlify)

- **Időzítés:** a Scheduled Function UTC szerinti cronnal fut, így óraátállításkor a 7:03-as budapesti időt kezelni kell. Egy futás legfeljebb 30 másodpercig tarthat, és csak az éles deployon fut.
- **Tárolás:** Netlify Blobs; a mostani artifact-adatbázisból egyszer át kell menteni az adatokat.
- **Különbség:** fix kód olvasná ki a petromap „Benzin ma X Ft” szövegét. Ez gyors és olcsó, de ha az oldal megváltozik, csendben elromlik. A Claude-os feladat meghagyható ellenőrzőnek.
- **Előtte:** a petromap felhasználási feltételeit el kell olvasni (van fizetős, jóváhagyáshoz kötött fejlesztői API-juk).
