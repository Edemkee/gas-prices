# Videókártya-árak napi frissítése – ütemezett feladat

- Név: Videókártya-árak napi frissítése
- Ütemezés: `CRON_TZ=CET 35 10 * * *` (minden nap 10:35, CET; 15 perccel a benzinárak után, hogy a két futás ne torlódjon)
- Futás: a felhőben, minden alkalommal új munkamenetben, automatikus jóváhagyással
- Mit csinál: a három Gigabyte videókártya aznapi Árukereső-legolcsóbb árát és Alza-árát beírja az élő oldal adatbázisába (`gpus/YYYY-MM-DD`)
- Ez a fájl a feladat utasításának verziókezelt másolata. Ha az utasítás változik, itt is frissíteni kell, ugyanabban a PR-ban.
- Ha a feladat elveszik, ebből a fájlból kell újra létrehozni: a név, az ütemezés és az utasítás szó szerint. Az azonosítót az ütemező adja, ezért itt nem szerepel; az aktuális a `CLAUDE.md`-ben van.

## Utasítás (szó szerint)

```
Feladat: frissítsd a "Benzinárak" weboldal videókártya-részének mai árait. Ez egy automatikus, felügyelet nélküli futás – ne kérdezz, ne hozz létre új oldalt, és ne módosítsd az oldal HTML-jét. Csak a mai napi videókártya-dokumentumot írd az oldal adatbázisába; a "prices" kollekcióhoz (benzinárak) ne nyúlj.

Az oldal: artifact slug 82aa5e36-0b9b-41e0-9bfb-6415d1f198d6 (https://claude.ai/artifact/H8qb55y2bJKe6Ewr1kxdFK). Az adatbázis-eszközöket ToolSearch-csel töltsd be: "select:mcp__claude-artifacts__db_get,mcp__claude-artifacts__db_write".

1) Határozd meg a mai dátumot Europe/Budapest időzónában (YYYY-MM-DD) – ez a dokumentum azonosítója.

2) A három kártya (pontosan ezek a gyártói cikkszámok; más változat – ICE/fehér, WINDFORCE, AERO, AORUS, OC nélküli GAMING – NEM számít):
   - g5070ti_gaming = GIGABYTE GeForce RTX 5070 Ti GAMING OC 16G, cikkszám GV-N507TGAMING OC-16GD
   - g5070ti_eagle  = GIGABYTE GeForce RTX 5070 Ti EAGLE OC SFF 16G, cikkszám GV-N507TEAGLE OC-16GD (a fekete; az "EAGLE OC ICE" más termék)
   - g5080_gaming   = GIGABYTE GeForce RTX 5080 GAMING OC 16G, cikkszám GV-N5080GAMING OC-16GD

3) Árukereső legolcsóbb ár ("low", Ft) és ajánlatszám ("offers") kártyánként. Csak olyan számot vehetsz fel, amit EBBEN a futásban WebFetch-csel magáról az oldalról olvastál ki. A WebSearch találati kivonataiban látható árak régi pillanatképek – azokat SOHA ne használd árként.
   - 5070 Ti (mindkét kártya): WebFetch https://www.arukereso.hu/videokartya-c3142/rtx-5070-ti/?orderby=1 – a terméksor "X Ft-tól" értéke a low, a "N ajánlat" az offers. Ha a kártya nincs a listán vagy a lekérés nem sikerül: https://www.arukereso.hu/videokartya-c3142/gigabyte/geforce-rtx-5070-ti-gaming-oc-16gb-gddr7-256bit-gv-n507tgaming-oc-16gd-p1180973089/ illetve https://www.arukereso.hu/videokartya-c3142/gigabyte/geforce-rtx-5070-ti-eagle-oc-sff-16gb-gddr7-256bit-gv-n507teagle-oc-16gd-p1181566441/ (ott a legalacsonyabb ajánlat a low).
   - 5080: WebFetch https://www.arukereso.hu/videokartya-c3142/f:gigabyte,rtx-5080/?orderby=1, ha nem sikerül: https://www.arukereso.hu/videokartya-c3142/rtx-5080/, végül https://www.arukereso.hu/videokartya-c3142/gigabyte/geforce-rtx-5080-gaming-oc-16gb-gddr7-256bit-gv-n5080gaming-oc-16gd-p1173406816/.
   - Minden URL-t legfeljebb kétszer próbálj. Ha egyik sem ad árat: low = null, offers = null, és a note-ba: "az Árukereső nem volt elérhető".

4) Alza ár ("alza", Ft) és készlet ("alzaStock", rövid szöveg, pl. "Raktáron > 5 db") kártyánként, WebFetch-csel:
   - g5070ti_gaming: https://www.alza.hu/gigabyte-geforce-rtx-5070-ti-gaming-oc-16g-d12814009.htm
   - g5070ti_eagle:  https://www.alza.hu/gigabyte-geforce-rtx-5070-ti-eagle-oc-sff-16g-d12814012.htm
   - g5080_gaming:   https://www.alza.hu/gigabyte-geforce-rtx-5080-gaming-oc-16g-d12766429.htm
   Az új termék aktuális (akciós, ha van) bruttó ára kell. Bontott, használt, "Unsealed" vagy "bontott" ajánlat árát ne vedd fel. Ha nincs ár, vagy a termék nem kapható: alza = null, és az alzaStock-ba írd, amit az oldal mond (pl. "Nem kapható").

5) Szabályok:
   - Soha ne becsülj, ne számolj, ne vegyél át más kártya árát, és ne másold át a tegnapi árat a mai rekordba. A hiányzó árat az oldal magától a legutóbbi ismert árral pótolja, "!" jellel.
   - Ha a low nagyobb, mint az alza (ugyanarra a kártyára), mindkét számot írd be változatlanul, és a note-ba: "az Alza ára alacsonyabb az Árukereső legolcsóbbnál".
   - A számok sima JSON egész számok legyenek (pl. 535680), ne szövegek.

6) Írd be a dokumentumot: db_write a slug-gal, op "set", path "gpus/<mai dátum>". Ha a dokumentum már létezik (előbb nézd meg db_get-tel), add meg az ifVersion-t a db_get által visszaadott verzióval. Pontos séma:
{
  "date": "YYYY-MM-DD",
  "updatedAt": "<most, ISO 8601 UTC>",
  "cards": {
    "g5070ti_gaming": { "low": n|null, "offers": n|null, "alza": n|null, "alzaStock": "<szöveg>"|null, "note": "<opcionális>" },
    "g5070ti_eagle":  { ...ugyanígy... },
    "g5080_gaming":   { ...ugyanígy... }
  }
}

7) Ellenőrzés: db_get a "gpus/<mai dátum>" dokumentumra, és nézd meg, hogy a beírt értékek megegyeznek az összegyűjtöttekkel.

8) A végén küldj egy rövid magyar összefoglalót (SendUserMessage-dzsel, ha elérhető): kártyánként a mai Árukereső-legolcsóbb és Alza-ár, és melyik forrás nem volt elérhető.
```
