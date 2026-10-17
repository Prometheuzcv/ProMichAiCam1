# Místní displej s živým náhledem

Displej 3.5inch RPi Display 480 × 320 s odporovým dotykem XPT2046 odpovídá zapojením rodině MPI3501/ILI9486. Ověřená instalace používá Raspberry Pi 4B, Debian 13 a prostředí labwc.

## Ovladač a obraz

V `/boot/firmware/config.txt` je v sekci `[all]`:

```ini
dtparam=spi=on
dtoverlay=piscreen,drm,speed=16000000,rotate=0
```

Změna byla provedena lokálním pomocníkem se zálohou původní konfigurace pod `/var/backups/promich-display/`. Není potřeba měnit obraz systému ani spouštět starší instalační skripty LCD-show. Používá se instalovaný DRM ovladač `ili9486` a dotykový ovladač `ads7846`.

## Automatický náhled

- Kamera běží jako uživatelská služba `ai-camera.service`.
- Aplikace nabízí místní stránku `http://127.0.0.1:8080/display`. Ta zobrazuje MJPEG s detekčními rámečky přes celou obrazovku, se zachováním poměru stran a malým stavovým řádkem.
- Po startu grafické relace soubor `~/.config/labwc/autostart` spustí uživatelskou službu `ai-camera-display.service`. Ta spustí `~/ai-camera/display-kiosk.py` a Chromium v režimu kiosk.
- Náhled nevyžaduje dotyk ani přístup k internetu. Počká na místní HTTP server a poté zobrazuje stav načítání kamery. Po přerušení spojení stránka opakuje připojení.
- Prohlížeč používá samostatný profil `~/.local/state/promich-camera/chromium`; žádná hesla se v něm pro tuto funkci nezadávají. Překladové nabídky a výzva ke klíčence jsou vypnuté pouze pro tento náhled.
- Původní systémový autostart je zachován. Kiosk se spouští až z grafické relace; samotná jednotka displeje je statická a nemusí být `enabled`.

Zdrojové soubory jsou v `deploy/`: jednotka, spouštěč a úryvky konfigurace labwc. Při obnově patří spouštěč do `~/ai-camera/display-kiosk.py`, jednotka do `~/.config/systemd/user/ai-camera-display.service`. Úryvek autostartu je potřeba sloučit s existujícím souborem. Pokud uživatelský autostart předtím neexistoval, musí také spouštět `/bin/sh /etc/xdg/labwc/autostart &`, aby zůstaly systémové funkce.

## Dotyk a kliknutí

Při živém měření byly zaznamenané skutečné stisky, uvolnění a souřadnice panelu. Uživatelská konfigurace labwc obsahovala pouze mapování dotyku a vynechávala výjimku pro levý klik na plochu. Výchozí chování labwc pak může levým kliknutím otevřít menu plochy, což působí jako pravé tlačítko.

Do existující konfigurace byly doplněné běžné myší vazby a prázdná vazba `Root / Left / Press`, stejně jako v systémové konfiguraci Raspberry Pi. Dotyk zůstává mapovaný na `SPI-1` s emulací myši. Viz `deploy/labwc-touch.fragment.xml`. Přesnost souřadnic a potřebná síla stisku vyžadují samostatné fyzické ověření. Parametry tlaku v jádře nebyly měněné bez kalibračních podkladů.

## Kontrola a návrat

```sh
systemctl --user status ai-camera.service ai-camera-display.service
curl --max-time 5 http://127.0.0.1:8080/status
wlr-randr
```

Při přihlášení přes SSH může `wlr-randr` potřebovat `WAYLAND_DISPLAY=wayland-0`; adresář `XDG_RUNTIME_DIR` musí patřit danému uživateli.

Zastavení samotného kiosku bez zastavení kamery:

```sh
systemctl --user stop ai-camera-display.service
```

Pro trvalé vypnutí automatického náhledu odstranit pouze označený blok `BEGIN/END ProMichAiCam1 display` z uživatelského autostartu. Původní aplikace, autostart i konfigurace dotyku byly před nasazením zálohované v `~/.local/state/promich-camera/backups/`.

Ověření a jeho omezení jsou zaznamenané v `STAV_PROJEKTU.md`. Zachycené obrazy místní kamery a soukromé provozní výpisy se do veřejného repozitáře neukládají.

HTTP regresní test bez přístupu ke kameře lze spustit z kořene repozitáře příkazem `python3 tests/test_http.py`. Ověří obě HTML stránky, stav a MJPEG cestu s query stringem používaným při obnovení spojení; nejde o náhradu testu fyzické kamery.

Podklady: [oficiální návod Raspberry Pi pro kiosk v labwc](https://www.raspberrypi.com/tutorials/how-to-use-a-raspberry-pi-in-kiosk-mode/), [zdroj overlaye piscreen](https://github.com/raspberrypi/linux/blob/rpi-6.18.y/arch/arm/boot/dts/overlays/piscreen-overlay.dts), [dokumentace konfigurace labwc](https://labwc.github.io/labwc-config.5.html).
