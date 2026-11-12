# Automatikus élesítés – ütemezett feladat

- Név: Benzinárak élesítés
- Ütemezés: `CRON_TZ=CET 40 7-21 * * *` (óránként, 7:40 és 21:40 között, CET)
- Futás: a felhőben, minden alkalommal új munkamenetben, automatikus jóváhagyással
- Mit csinál: ha a GitHub `main` ágán újabb verzió van, mint az élő artifacton, kiteszi a `main` `src/index.html`-jét az élő artifactra. Ha nincs újabb verzió, azonnal leáll.
- Ez a fájl a feladat utasításának verziókezelt másolata. Ha az utasítás változik, itt is frissíteni kell, ugyanabban a PR-ban.

## Utasítás (szó szerint)

```
Feladat: a "Benzinárak" élő oldal automatikus élesítése. Ez egy felügyelet nélküli, óránkénti ellenőrzés – ne kérdezz, és az adatbázishoz ne nyúlj.

Élő artifact: slug 82aa5e36-0b9b-41e0-9bfb-6415d1f198d6. Forrás: a nyilvános https://github.com/Edemkee/gas-prices repó main ága (VERSION fájl és src/index.html).
Az artifact-eszközöket ToolSearch-csel töltsd be: "select:mcp__claude-artifacts__get_artifact,mcp__claude-artifacts__read_artifact,mcp__claude-artifacts__publish_files".

1) A main verziója és oldala. Bash-ben:
   git clone --depth 1 https://github.com/Edemkee/gas-prices /home/claude/gp-deploy
   Ha a clone nem sikerül, ugyanezt a két fájlt a GitHub REST API-ból töltsd le pontosan, bájtra egyezően:
   gh api -H 'Accept: application/vnd.github.raw' 'repos/Edemkee/gas-prices/contents/VERSION?ref=main' > /home/claude/gp-deploy/VERSION
   gh api -H 'Accept: application/vnd.github.raw' 'repos/Edemkee/gas-prices/contents/src/index.html?ref=main' > /home/claude/gp-deploy/src/index.html
   (előtte: mkdir -p /home/claude/gp-deploy/src). Ha egyik út sem működik, állj le, és küldj egy rövid magyar üzenetet a hibáról (SendUserMessage, ha elérhető).
   Ellenőrizd: a VERSION tartalma MAJOR.MINOR.PATCH alakú, és a src/index.html láblécében pontosan ez szerepel: <div class="status">v<VERSION></div>. Ha nem egyezik, ne élesíts; küldj rövid üzenetet.

2) Az élő verzió: read_artifact a fenti sluggal, és keresd meg a <div class="status">vX.Y.Z</div> részt. Ha nincs ilyen, az élő verziót tekintsd 0.0.0-nak.

3) Döntés (szemantikus verzió-összehasonlítás, számonként):
   - Ha a main verziója NEM nagyobb, mint az élőé: nincs teendő. Azonnal állj le, üzenet nélkül.
   - Ha nagyobb: folytasd a 4. lépéssel.

4) Élesítés: get_artifact a sluggal (ebből jön a base_version és a read érték). Utána publish_files: slug a fenti, base_version a get_artifact verziója, mode "patch", label "v<VERSION>", files: [{"as": "index.html", "path": "/home/claude/gp-deploy/src/index.html"}]. Ha a read érték "users" vagy "org", add meg shared_live-ként. Ütközés (conflict) esetén egyszer kérd le újra a get_artifact-ot, és próbáld újra.

5) Ellenőrzés: read_artifact újra, és nézd meg, hogy a lábléc most v<VERSION>. A végén küldj egy egysoros magyar üzenetet: "Élesítve: vRÉGI → vÚJ".

Soha ne módosítsd az artifact adatbázisát, ne írj bele a repóba, és csak a main ágról élesíts (PR-branchről soha).
```
