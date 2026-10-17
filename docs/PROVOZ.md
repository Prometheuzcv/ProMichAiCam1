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

## Model a parametry

Model očekávaný aplikací:

```text
/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk
```

Náhled: 960 × 720, RGB888, požadavek 15 FPS, šest bufferů, JPEG kvalita 80. Detekční práh 0.55, nejvýše 1.5 sekundy starý poslední výsledek AI. Štítky a převod souřadnic vycházejí z intrinsics modelu.

## HTTP cesty

- `/`: HTML náhled.
- `/status`: stav aplikace v JSON.
- `/snapshot.jpg`: aktuální JPEG, pokud je snímek dostupný.
- `/stream.mjpg`: MJPEG stream.

Server poslouchá pouze na `127.0.0.1:8080`. Webový server se spouští společně s kamerovým vláknem. Spuštění `app.py` tedy znamená spuštění kamery.

## Služba

Uživatelská systemd jednotka `ai-camera.service`, `Restart=on-failure`, prodleva 5 sekund. Při obnově byla povolená, ale neaktivní. Stav `enabled` sám o sobě nepotvrzuje běžící kameru.
