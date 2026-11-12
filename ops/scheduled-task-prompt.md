# Napi frissítés – ütemezett feladat

- Név: Benzinárak napi frissítése
- Azonosító: `trig_01DvQepk78PsfNFpNJxJjt8F`
- Ütemezés: `CRON_TZ=CET 20 10 * * *` (minden nap 10:20, CET; a holtankoljak hétköznap 10 óráig közli a napi országos átlagot)
- Futás: a felhőben, minden alkalommal új munkamenetben, automatikus jóváhagyással
- Ez a fájl a feladat utasításainak verziókezelt másolata. Ha az utasítás változik, itt is frissíteni kell, ugyanabban a PR-ban.

## Utasítás (szó szerint)

```
Feladat: frissítsd a "Benzinárak – XVIII–XIX. kerület környéke" weboldal mai benzinárait. Ez egy automatikus, felügyelet nélküli futás – ne kérdezz, ne hozz létre új oldalt, és ne módosítsd az oldal HTML-jét. Csak a mai napi adatdokumentumot írd az oldal adatbázisába.

Az oldal: artifact slug 82aa5e36-0b9b-41e0-9bfb-6415d1f198d6 (https://claude.ai/artifact/H8qb55y2bJKe6Ewr1kxdFK). Az adatbázis-eszközöket ToolSearch-csel töltsd be: "select:mcp__claude-artifacts__db_get,mcp__claude-artifacts__db_write,mcp__claude-artifacts__db_query".

1) Határozd meg a mai dátumot Europe/Budapest időzónában (YYYY-MM-DD) – ez a dokumentum azonosítója.

2) Gyűjtsd össze minden kúthoz a MAI benzinárakat (Ft/liter). A legfontosabb a b95 (normál 95-ös benzin). Opcionális: b95p = prémium 95-ös, b100 = 100-as benzin – ha nem találod, legyen null.
   - omv = OMV, Budapest XXIII., Nagykőrösi út 349. Elsődleges forrás: WebFetch https://petromap.eu/hu/station/omv-budapest-9e4502 (a "Benzin ma X Ft" a 95-ös ár). Tartalék: WebSearch "holtankoljak OMV Nagykőrösi út 349".
   - avia = AVIA, Budapest X., Keresztúri út 108/a. Elsődleges forrás: WebFetch https://petromap.eu/hu/station/avia-budapest-f1b709 ("Benzin ma X Ft"). Tartalék: WebSearch "holtankoljak AVIA Keresztúri út 108".
   - mpetrol = M.Petrol ("az elefántos"), Budapest XIX., Citroën utca 2. (1194). Petromapon "M.Petrol Budapest 2" néven szerepel (koordináta 47.4368, 19.1438): WebFetch https://petromap.eu/hu/station/m-petrol-budapest-0758e5. Tartalék: https://es.fuelo.net/gasstation/id/65124?lang=hu.
   - dallas = Dallas, Budapest X., Száva utca 5–7. Próbáld: WebSearch "petromap Dallas Száva utca", "holtankoljak Dallas Száva utca", és https://gr.fuelo.net/gasstation/id/87324.
   - national = országos átlag: WebSearch "holtankoljak üzemanyagár mai átlagár" vagy WebFetch https://holtankoljak.hu/ – a mai (vagy a legutóbbi hétköznapi) 95-ös benzin országos átlagár b95-be.

   Szabályok:
   - Csak a fent megnevezett városi kutak árát használd. Autópályás kút (M0, M1, M3, M5, M7 stb. pihenő vagy autópálya mellett) árát SOHA ne vedd fel, akkor sem, ha ugyanabba a láncba tartozik.
   - FRISS ár: láthatóan mai vagy tegnapi (dátum, "ma" jelölés vagy friss "frissítve" időbélyeg). Ilyenkor "stale": false.
   - NEM FRISS ár: ha nincs friss ár, de találsz régebbi dátumú vagy dátum nélküli árat ehhez a kúthoz (pl. fuelo.net), azt is felveheted, de csak akkor, ha a 95-ös ár legfeljebb 5%-kal tér el a mai országos átlagtól (a fuelo.net néha becsült, sokkal magasabb értéket mutat – azt hagyd ki). Ilyenkor "stale": true, "asOf": a forrás szerinti dátum (YYYY-MM-DD), vagy null, ha nincs dátum; "note": "nem friss ár".
   - Ha semmilyen elfogadható ár nincs: b95/b95p/b100 = null, src = null, stale = false, note = "nem volt friss ár". (Az oldal ilyenkor magától a legutóbbi ismert árat mutatja, felkiáltójellel.)
   - Soha ne becsülj, ne számolj, ne vegyél át más kút árát, és ne másold át a tegnapi árat a mai rekordba.

3) Írd be a dokumentumot: db_write a slug-gal, op "set", path "prices/<mai dátum>". Ha a dokumentum már létezik (előbb nézd meg db_get-tel), add meg az ifVersion-t a db_get által visszaadott verzióval. Pontos séma:
{
  "date": "YYYY-MM-DD",
  "updatedAt": "<most, ISO 8601 UTC>",
  "national": { "b95": <szám vagy null>, "src": "holtankoljak.hu" },
  "stations": {
    "omv":     { "b95": n|null, "b95p": n|null, "b100": n|null, "src": "<forrás domain>"|null, "stale": true|false, "asOf": "YYYY-MM-DD"|null, "note": "<opcionális>" },
    "avia":    { ...ugyanígy... },
    "mpetrol": { ...ugyanígy... },
    "dallas":  { ...ugyanígy... }
  }
}
Az "asOf" mező csak nem friss árnál kell; friss árnál elhagyható. A számok sima JSON számok legyenek (pl. 597 vagy 598.9), ne szövegek.

4) Ellenőrzés: db_get a "prices/<mai dátum>" dokumentumra, és nézd meg, hogy a beírt értékek megegyeznek az összegyűjtöttekkel.

5) A végén küldj egy rövid magyar összefoglalót (SendUserMessage-dzsel, ha elérhető): a mai 95-ös árak kutanként, és melyik kúthoz nem volt friss adat.
```
