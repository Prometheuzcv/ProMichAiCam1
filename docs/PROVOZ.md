# Provoz a závislosti

Zdrojový program je `app.py`. Při aktuálně zjištěném uspořádání je na zařízení v adresáři `~/ai-camera/app.py`. Jednotka `deploy/ai-camera.service` používá tento adresář relativně k domovu přihlášeného uživatele.

## Závislosti zjištěné při obnově 17. 10. 2026

| Balíček | Zjištěná verze |
|---|---|
| `imx500-all` | `1.14.0-1` |
| `imx500-models` | `1:1.0.0-1` |
| `python3-opencv` | `4.10.0+dfsg-5` |
| `python3-picamera2` | `0.3.37-1` |
| `rpicam-apps` | `1.14.0-1` |

Jde o balíčky instalované v tehdejším systému zařízení; tento seznam není tvrzením o aktuálních nejnovějších verzích ani samostatným instalačním skriptem. Picamera2 a IMX500 potřebují kompatibilní systémové knihovny a hardware.

Při údržbě 18. 10. 2026 byla Picamera2 aktualizovaná na `0.3.38-1` a Chromium na `1:155.0.8059.39-1~deb13u1+rpt1`. Po načtení nových knihoven byl znovu ověřen skutečný běh kamery a inference. Detekční model ani nastavení snímání se neměnily. Přesný rozsah aktualizací a ponechané balíčky jsou ve stavovém souboru.

## Model a parametry

Model očekávaný aplikací:

```text
/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk
```

Náhled: 960 × 720, RGB888, požadavek 15 FPS, šest bufferů, JPEG kvalita 80. Detekční práh 0.55, nejvýše 1.5 sekundy starý poslední výsledek AI. Štítky a převod souřadnic vycházejí z intrinsics modelu.

## HTTP cesty

- `/`: HTML náhled.
- `/display`: celoobrazovkový náhled pro místní displej; bez ovládacích prvků, s obnovováním spojení.
- `/status`: stav aplikace v JSON.
- `/snapshot.jpg`: aktuální JPEG, pokud je snímek dostupný.
- `/stream.mjpg`: MJPEG stream.

Server poslouchá pouze na `127.0.0.1:8080`. Webový server se spouští společně s kamerovým vláknem. Spuštění `app.py` tedy znamená spuštění kamery.

Po přidání místního kiosku přijímají HTTP cesty také query string. Ten slouží k obnovení MJPEG spojení; nemění detekční model ani parametry kamery. Automatické zobrazení po startu popisuje [DISPLEJ.md](DISPLEJ.md).

## Služba

Uživatelská systemd jednotka `ai-camera.service`, `Restart=on-failure`, prodleva 5 sekund. Při obnově byla povolená, ale neaktivní. Stav `enabled` sám o sobě nepotvrzuje běžící kameru.

## Dohled a obnova — 18. 10. 2026

Samostatné dohledové vlákno ukončí celý proces návratovým kódem 1 při zachycené chybě kamerového vlákna nebo při zastavení přibývání dat. Systemd tak může kameru znovu spustit i tehdy, když by HTTP server jinak zůstal živý. Limity používají monotónní čas:

- první snímek: do 300 sekund od startu procesu, aby byl prostor pro studené načítání firmwaru;
- další snímky: nejvýše 15 sekund bez postupu;
- první inference: do 60 sekund od prvního snímku;
- další inference: nejvýše 30 sekund bez postupu.

Jednotka dovoluje nejvýše pět spuštění v 600 sekundách. Při trvalé závadě tedy nevzniká nekonečná rychlá smyčka; po nápravě může být potřeba `systemctl --user reset-failed ai-camera.service` a nové spuštění. Způsob zobrazení ani detekční model se nemění.

`fps` je nyní frekvence v posledních třech sekundách. `/status` přidává `inference_fps`, monotónně měřené `frame_age` a `inference_age` v sekundách a `ai_ready`. Před prvním výsledkem je stáří `null`; staré vzorky postupně expirují. Kumulativní čítač už není důkazem současně aktivní AI. Nový stavový řádek kiosku začne platit až po načtení nové stránky.

Ověření bez fyzické kamery: `python3 tests/test_health.py` a `python3 tests/test_http.py`. Testy pokrývají limity rozběhu, zastavení snímků a inference, propadnutí starých metrik a skutečné ukončení subprocessu při simulované chybě senzoru. Provozní test a omezení viz `STAV_PROJEKTU.md`.

## Připravená systémová údržba

`deploy/maintenance.sh` se spouští pouze výslovně a jako root na cílovém zařízení. Zálohuje seznam balíčků a případné existující přepisy čekání na síť. Nastaví `NM_ONLINE_TIMEOUT=120`, zachová profily a priority Wi-Fi a ověří běh čekací služby. Důvodem je doložený přechod z nedostupné přednostní sítě, který trval déle než původních 60 sekund. Tato změna nezrychluje asociaci a sama neověřuje příští boot.

Poté obnoví katalog APT, uloží plán aktualizace a provede `apt-get upgrade` s `--no-remove`; existující lokální konfigurační soubory zachová. Aktualizace není automaticky spuštěná kamerovou službou. Po dokončení je nutné ověřit služby, knihovny a kiosk; případný restart systému se posuzuje zvlášť. Záloha seznamu balíčků není obraz SD karty ani automatický návrat všech aktualizací.
