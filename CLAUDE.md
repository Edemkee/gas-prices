# CLAUDE.md – projekt döntések és munkaszabályok

A projekt a **dev-workflow** skill szerint működik. Új munkamenet elején: el kell olvasni ezt a fájlt, a `PLAN.md`-t és a `CHANGELOG.md`-t, meg kell nézni a `VERSION`-t és a legutóbbi taget, aztán a `PLAN.md` aktuális vagy következő tételével kell folytatni.

## A projekt röviden

- **Méret:** kis projekt. A FEATURES.md, az ARCHITECTURE.md és a CI opcionális; akkor ajánljuk fel, amikor a projekt nő (pl. Netlify-backend).
- **Oldal:** `src/index.html`, egyetlen önálló HTML-fájl, a diagram kézzel írt SVG. claude.ai artifactként fut: slug `82aa5e36-0b9b-41e0-9bfb-6415d1f198d6`, https://claude.ai/artifact/H8qb55y2bJKe6Ewr1kxdFK
- **Tagelés:** `.github/workflows/tag-release.yml` – merge után a `VERSION` alapján.
- **Előnézet:** külön artifact, slug `5b02d724-566f-4cf2-92fa-8dd3a66be135`, https://claude.ai/artifact/CEq78EWUwDydsbWYSspjkx – mindig az éppen nyitott PR változata, „ELŐNÉZET” sávval, az élő adatok másolatával.
- **Élesítés:** ütemezett feladat `trig_01RXm1aoLFiNW3kZJSYqUNHu`, óránként 7:40 és 21:40 között (CET): ha a `main` verziója újabb, mint az élő oldalé, kiteszi a `main` `src/index.html`-jét. Az utasítás másolata: `ops/deploy-task-prompt.md`.
- **Napi frissítés:** ütemezett feladat `trig_01DvQepk78PsfNFpNJxJjt8F`, minden nap 10:20 (CET, `CRON_TZ=CET`). Az utasítás másolata: `ops/scheduled-task-prompt.md`.
- **Verzió:** a `VERSION` fájlban, a lábléc (`src/index.html`) is mutatja.

## Adatmodell

Kollekció: `prices`, dokumentumazonosító: `YYYY-MM-DD` (budapesti nap). Írni csak a tulajdonos tud (`write: owner`), olvasni mindenki, aki látja az oldalt (`read: view`).

```json
{
  "date": "2026-11-11",
  "updatedAt": "2026-11-11T19:47:00Z",
  "national": { "b95": 602, "src": "holtankoljak.hu" },
  "stations": {
    "omv":     { "b95": 597, "b95p": null, "b100": null, "src": "petromap.eu" },
    "avia":    { "b95": 595, "b95p": null, "b100": null, "src": "petromap.eu" },
    "mpetrol": { "b95": 599, "b95p": null, "b100": null, "src": "petromap.eu" },
    "dallas":  { "b95": null, "b95p": null, "b100": null, "src": null, "note": "nem volt friss ár" }
  }
}
```

Egy nem friss ár rekordja: `{ "b95": 601.3, "src": "fuelo.net", "stale": true, "asOf": "2026-11-08", "note": "nem friss ár" }`; ha nincs dátum, az `asOf` null. Ugyanarra a napra az újabb futás felülírja a rekordot (`set`, `ifVersion`-nel). Az oldal az utolsó 30 rekordot olvassa élőben. Kapacitás: 25 000 dokumentum.

## Munkaszabályok

- **Verziózás (dev-workflow):** `MAJOR.MINOR.PATCH`, PR-onként egy emelés. Funkció vagy érdemi változás: MINOR +1, PATCH nullázva; 0.9.x után **0.10.0** jön, nem 1.0.0. Apró javítás: PATCH +1. MAJOR csak a felhasználó kifejezett kérésére.
- Minden változás külön branchen és PR-ban megy (`feature/...`, `fix/...`, `docs/...`) az `Edemkee/gas-prices` repóban; a merge a felhasználóé. Merge után a `main`-en a tag (`vX.Y.Z`) automatikusan elkészül (`tag-release` workflow); Claude a következő munkamenetben ellenőrzi, hogy megvan-e. A válaszban mindig benne van a PR linkje.
- A változás előtt fusson a `tests/smoke_test.py`, és csak akkor commitolunk, ha átment.
- Commit előtt a staged diffet át kell nézni titkos adatra (kulcs, token, jelszó, személyes adat).
- Az oldal módosítása: `src/index.html` szerkesztése, smoke teszt, PR. **Az élő artifactra Claude kézzel nem publikál**; azt merge után az élesítő feladat teszi ki.
- **Előnézet minden PR-nál:** a PR megnyitásakor (és minden új commit után) `python3 ops/make_preview.py "PR #<n> · v<VERSION>" /home/claude/preview/index.html`, majd `publish_files` az előnézeti artifactra (`mode: patch`, `as: index.html`). Előtte az élő `prices` rekordokat át kell másolni az előnézet adatbázisába (élő: `db_query`, előnézet: `db_write` `set`, meglévő dokumentumnál `ifVersion`-nel), változtatás nélkül. Az előnézet linkje a PR-leírásba és a válaszba is bekerül.
- Ha a napi feladat utasítása változik: a feladatot is frissíteni kell (`update_trigger`), és az `ops/scheduled-task-prompt.md`-t is, ugyanabban a PR-ban.
- Az adatbázisba kitalált vagy mintaadat soha nem kerül. A teszt csak mockolt adatbázissal dolgozik.

## Döntések (legújabb felül)

- **2026-11-12 – PR-előnézet külön artifacton, az élő adatok másolatával.** A PR megnyitásakor Claude kiteszi a PR változatát az előnézeti artifactra „ELŐNÉZET” sávval (`ops/make_preview.py`), és átmásolja az élő árakat. *Indok:* a felhasználó a PR merge előtt akarja látni a változást, hogy a hibák még a PR-ba kerülhessenek; az élő adatok másolata nem kitalált adat.
- **2026-11-12 – Automatikus élesítés merge után, óránkénti ütemezett feladattal (7:40–21:40, CET).** *Indok:* a felhasználó kérte, hogy a merge után ne kézzel kelljen élesíteni. A GitHub nem tud közvetlenül artifactot frissíteni, és a merge-ről a Claude-munkamenet nem kap értesítést, ezért egy rendszeres ellenőrzés kell; a felhasználó a 8 és 22 óra közötti óránkénti gyakoriságot választotta (a perc a torlódás elkerülésére 40). Merge után legfeljebb kb. egy óra múlva élesedik.
- **2026-11-12 – A napi frissítés 10:20-kor fut, CET időzónában** (`CRON_TZ=CET 20 10 * * *`). *Indok:* a 7:03-as első futás nem mai adatot hozott: a holtankoljak hétköznap 10 óráig teszi közzé a napi országos átlagot (2026-11-12-én 08:43-kor jelent meg), és a kutak árai is a tegnapiak voltak. A felhasználó a két lehetőség (7:03 + 10:20, vagy csak 10:20) közül a csak 10:20-at választotta, és a CET időzónát kérte. A `CET` IANA-zóna ugyanúgy vált nyári időre (CEST), mint az `Europe/Budapest`, így a futás egész évben helyi idő szerint 10:20-kor indul.
- **2026-11-12 – Tagelés automatikusan, GitHub Actions-szel** (`.github/workflows/tag-release.yml`). Minden `main`-re kerülő push (merge) után a workflow kiolvassa a `VERSION`-t, és ha még nincs `vX.Y.Z` tag, létrehozza és feltölti. Kézzel is indítható (Actions → Tag release → Run workflow). *Indok:* a Claude-munkamenetből a tag létrehozása minden úton tiltott (git push, REST `git/refs` és `git/tags`, release-ek: 403); a workflow a GitHub saját jogosultságával fut, így a tagelés nem a felhasználóra marad.
- **2026-11-12 – A repó nyilvános, ezért bele csak olyan kerülhet, ami bárki szeme elé kerülhet.** Az artifact-link és az ütemezett feladat azonosítója rendben van (mindkettő csak a tulajdonosnak nyílik meg); e-mail-cím, token vagy személyes adat nem kerülhet be. *Indok:* a repó nyilvános láthatósággal jött létre.
- **2026-11-12 – A commitokba és a PR-leírásba nem kerül Claude session-link** (`Claude-Session: …`, `https://claude.ai/code/session_…`). A `Co-Authored-By: Claude …` sor marad. *Indok:* a felhasználó kérése; a dev-workflow skillben is.
- **2026-11-12 – A PR-t Claude nyitja meg a GitHub REST API-n keresztül** (`gh api repos/Edemkee/gas-prices/pulls`). A GraphQL (`gh pr …`) a munkamenetből tiltott, a REST működik. *Indok:* így a PR-link azonnal a válaszba kerülhet.
- **2026-11-12 – A repóban be van kapcsolva a Secret Protection és a push protection.** *Indok:* dev-workflow, 7. fejezet.
- ~~2026-11-12 – A tageket a felhasználó tölti fel a saját gépéről.~~ Felváltotta az automatikus tagelés (lásd fent).
- **2026-11-12 – Minden változásról szóló válaszban benne van az új PR linkje** (dev-workflow, 2. fejezet). *Indok:* a felhasználó közvetlenül onnan nézi át és olvasztja be.
- **2026-11-12 – A repó: `Edemkee/gas-prices` (**nyilvános**), alapág: `main`.** A commitok szerzője `Edemkee <Edemkee@users.noreply.github.com>`, a Claude társszerző. *Indok:* a felhasználó választása; a noreply cím nem fedi fel a valódi e-mail-címet.
- ~~2026-11-12 – Amíg nincs GitHub-remote, a változás helyi branchen készül, és fast-forwarddal kerül a `main`-re.~~ Lezárva: a v0.3.3-tól minden változás PR-ral megy.
- **2026-11-12 – Minden dokumentum neve nagybetűs** (README.md, CLAUDE.md, PLAN.md, CHANGELOG.md, és ha lesznek: FEATURES.md, ARCHITECTURE.md), a dev-workflow skillben is. *Indok:* a felhasználó kérése.
- **2026-11-12 – A dev-workflow skill bevezetése.** A korábbi v0.1–v0.3 a skill szerint 0.1.0–0.3.0. A minor léptetés szabálya változatlan (0.9 után 0.10); új a PATCH szám az apró javításokra. *Indok:* a felhasználó kérte; a két szabály összefér.
- **2026-11-12 – Projektméret: kis projekt.** Kötelező: README, .gitignore, VERSION, PLAN.md, CLAUDE.md, CHANGELOG.md. A FEATURES.md, az ARCHITECTURE.md és a CI később jön, ha a projekt nő. *Indok:* egyetlen HTML-oldal és egy ütemezett feladat.
- **2026-11-12 – Könyvtárszerkezet:** `src/` (oldal), `ops/` (ütemezett feladat utasítása), `tests/` (smoke teszt). *Indok:* a skill GitHub-kész struktúrát kér.
- **2026-11-12 – Helyi git repo, első commit a v0.3.0 állapota, tag `v0.3.0`.** A v0.1.0 és v0.2.0 csak a CHANGELOG-ban szerepel. *Indok:* ezek git nélkül készültek; utólag kitalált commitokat nem gyártunk.
- **2026-11-11 – A Netlify-átköltözés opció marad (plan 16.), nem döntés.** *Indok:* előbb a GitHub-kapcsolat kell, és a petromap felhasználási feltételeit is meg kell nézni.
- **2026-11-11 – Nem friss ár kétféleképpen jöhet létre:** (1) az oldal viszi tovább az előző napok rekordjából, a rekordban null marad, nem másolunk; (2) a napi feladat egy régebbi vagy dátum nélküli árat `stale: true` és `asOf` mezővel ír be, de csak akkor, ha legfeljebb 5%-kal tér el az országos átlagtól. *Indok:* a rekordból mindig látszik, mi volt valóban aznapi; a fuelo.net becsült értékeit (pl. 656,2 Ft ugyanazzal a számmal két kútnál, a 602 Ft-os átlag mellett) a korlát kiszűri.
- **2026-11-11 – Legutóbbi ismert ár „!” jellel, mind a négy kútra.** A diagramon a vonal csak a friss árakon fut át; a nem friss nap üres karika. Ez felülírja a korábbi „inkább nincs adat, mint régi ár” szabályt. *Indok:* a felhasználó kérése.
- **2026-11-11 – A GitHub-integráció teendő marad;** a felhasználó otthon, a saját gépéről köti össze. *Indok:* a felhasználó döntése.
- **2026-11-11 – AVIA: a Keresztúri út 108/a (X. ker.) a vecsési Üllői út 812. helyett.** Forrás: https://petromap.eu/hu/station/avia-budapest-f1b709. *Indok:* a vecsésihez nem volt friss ár; a Keresztúri úti városi kút „ma” jelölésű árral, és a két budapesti AVIA közül ez van közelebb (a másik a Vágóhíd utcai).
- **2026-11-11 – Irányelv: autópályás árak egyik láncból sem kellenek.** Csak városi kutak; a napi feladat autópályás kút árát akkor sem veheti fel, ha ugyanabból a láncból van. *Indok:* a felhasználó kifejezett kérése.
- **2026-11-11 – Nincs visszamenőleges 30 napos feltöltés.** *Indok:* kutankénti árelőzmény nyilvánosan nem elérhető (a petromapon regisztráció kell hozzá); kitalált adatot nem írunk.
- **2026-11-11 – A diagram x-tengelye mindig az utolsó 30 nap; hiányzó napnál megszakad a vonal.** *Indok:* hiányzó nap fölötti összekötés nem létező adatot sugallna.
- ~~**2026-11-11 – A frissítés 7:03-kor fut, nem pontosan 7:30-kor.**~~ Felváltotta a 10:20-as futás (2026-11-12). *Indok:* így 7:30-ra biztosan kész; a kerek időpontokban torlódhat az ütemező.
- **2026-11-11 – Az M.Petrol Citroën utcai kút a petromapon „M.Petrol Budapest 2”** (koordináta 47.4368, 19.1438). *Indok:* a petromap nem írja ki az utcanevet; a koordináta alapján azonosítottuk.
- **2026-11-11 – Elsődleges forrás a petromap.eu** (a kút oldalán a „Benzin ma X Ft”), az országos átlagé a holtankoljak.hu. *Indok:* csak a petromap ad kutanként mai jelölésű árat, ami gépileg olvasható; a holtankoljak kútoldalai JavaScripttel töltődnek.
- **2026-11-11 – Írási jog csak a tulajdonosé, olvasás mindenkié, aki látja az oldalt.** *Indok:* a napi feladat a tulajdonos nevében ír; a nézők ne tudják átírni az árakat.
- **2026-11-11 – Perzisztencia: az artifact saját adatbázisa,** napi egy dokumentum. *Indok:* az oldal közvetlenül olvassa, nincs szükség külső szerverre.
- **2026-11-11 – Üzemanyag: elsősorban a 95-ös benzin;** a prémium 95 és a 100-as opcionális mező. *Indok:* „benzin főleg, de mindegyik fajta”, később „a 95-ös elég”.
- **2026-11-11 – Figyelt kutak:** OMV Nagykőrösi út 349. (XXIII.), AVIA (lásd fent), M.Petrol Citroën utca 2. (XIX.), Dallas Száva utca 5–7. (X.). *Indok:* a felhasználó választása.
