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

## Zachování důkazů při problémech Wi-Fi

`deploy/enable-network-diagnostics.sh` vyžaduje root a před změnou zálohuje vlastní případné existující přepisy. Zapíná trvalý journald s `SystemMaxUse=64M`, `SystemMaxFileSize=8M`, `SystemKeepFree=512M` a `MaxRetentionSec=7day`. Přepíše distribuční `Storage=volatile`; protokoly tak mohou přežít restart. Při tvrdém odpojení napájení nemusí být úplně poslední záznamy uložené.

Pro NetworkManager zapíná DEBUG pouze v doménách CORE, DEVICE, WIFI, SUPPLICANT, IP4 a DHCP4, za běhu i pro následující start. Nespouští síťové připojení znovu ani nemění Wi-Fi profily. Protokoly obsahují soukromé síťové údaje a nesmí se vkládat do veřejného repozitáře. Po vyřešení problému je vhodné podrobnou síťovou úroveň vrátit na INFO; trvalé omezené systémové logování může zůstat.

Po testu lze místně porovnat `journalctl --list-boots`, `journalctl -b -1 -u NetworkManager` a `journalctl -b -k`. Pro intervaly používat `-o short-monotonic`, protože synchronizace hodin po startu může posunout kalendářní čas. Stavové soubory musí rozlišovat obyčejný softwarový restart, fyzické odpojení napájení a pouhé opětovné přihlášení přes SSH.

## Stejný název Wi-Fi, různý výsledek ověřování

Při reprodukovaném výpadku 18. 10. byl v journalu doložen sled: asociace ke konkrétnímu BSSID, selhání WPA handshake s `WRONG_KEY`, čekání na nové heslo, `no-secrets` a zablokování automatického připojování profilu. Jiný bod stejného SSID přijal stejné uložené heslo. Samotné hlášení `WRONG_KEY` neprokazuje, že bylo nesprávně uložené heslo; je potřeba porovnat výsledek na jednotlivých bodech a případně jejich skutečné nastavení.

`deploy/pin-working-ap.sh` přijímá jméno aktuálního profilu a jeho ověřený funkční BSSID jako dva místní argumenty. Vyžaduje root, ověřuje hostname i aktuální spojení, zálohuje `/etc/netplan` a `/etc/NetworkManager/system-connections` do kořenového adresáře s oprávněním 700 pod `/var/backups/promich-camera/`. Pomocí `nmcli connection modify` nastaví `802-11-wireless.bssid`. Ověří změnu i její trvalý zápis do Netplan; běžící spojení nerestartuje. Výsledek potvrzuje marker `AP_PIN_PERSISTED`. Zálohy obsahují tajné údaje a zůstávají pouze na zařízení.

Vazba na BSSID omezuje domácí profil na jediný bod. Pokud tento bod nebude dostupný, profil se nepřipojí k jinému bodu stejného SSID. Ostatní uložené síťové profily zůstávají beze změny. Toto chování odpovídá [dokumentaci NetworkManageru](https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nm-settings-nmcli.html). Po opravě je nutné ověřit nový boot ID, skutečně vybraný BSSID, DHCP, nové SSH spojení a čerstvý obraz i inference.

Pro návrat použít jako root `nmcli connection modify '<místní profil>' 802-11-wireless.bssid ''`, pokud byl původní BSSID prázdný; jinak obnovit hodnotu uloženou v `previous-bssid` v záloze. Poté ověřit trvalé uložení a provést samostatně sledovaný restart. Plné zálohy se nemají slepě přepisovat přes novější nesouvisející změny sítě.

## Cyklické připojování a porovnávání signálu

`deploy/wifi-supervisor.py` běží přes systémový timer `promich-wifi-supervisor.timer` každých přibližně 60 sekund, poprvé 45 sekund od bootu. Vyžaduje přesně dva výslovně vybrané uložené profily. Jejich UUID, SSID a případný BSSID získá instalační skript z NetworkManageru a uloží pouze místně do `/etc/promich-camera/wifi-supervisor.json` s oprávněním 600. Hesla nekopíruje. Profily, jejich priority a automatické připojování nemění; síť nadále spravuje NetworkManager.

- Při odpojené Wi-Fi nebo stavu failed střídavě žádá NetworkManager o připojení k prvnímu a druhému profilu. Počet kol není omezený. Výslovná aktivace umožňuje další pokus i po blokaci automatického připojení kvůli `no-secrets`. Probíhající asociaci, ověřování či DHCP nechává dokončit. Interval je interval kontrol, nikoli záruka dokončení připojení během minuty.
- Při fungujícím spojení porovnává čerstvé skeny nejvýše jednou za 300 sekund. Před přepnutím musí mít druhý profil dostupný bod se signálem alespoň 60 % a náskokem alespoň 20 procentních bodů oproti aktuálnímu bodu. Podmínka musí platit ve dvou po sobě jdoucích kontrolách. Po zahájení přepnutí následuje nejméně 900sekundová prodleva před dalším přepnutím podle signálu.
- Případná vazba profilu na BSSID se respektuje i při porovnávání: jiný bod stejného SSID není kandidát. Neznámé aktivní profily se nepřepínají. Vypnutou nebo nedostupnou Wi-Fi tento dohled sám nezapíná.
- Při neúspěšném přechodu a následném odpojení zkusí předchozí profil, poté opět střídá oba. Používá pouze existující profily, nikdy ne otevřenou síť ani žádost o nové heslo.

Tato pravidla porovnávají **sílu signálu**, nikoli skutečnou propustnost, latenci, vytížení AP nebo rychlost internetu. Vyšší procento signálu samo o sobě nedokazuje rychlejší síť. S jediným Wi-Fi rozhraním nelze před přepnutím současně změřit skutečný datový výkon druhé sítě. Přepnutí může přerušit vzdálené SSH; místní kamerové služby dohled nerestartuje.

Instalace: jako root spustit `deploy/install-wifi-supervisor.sh '<první UUID>' '<druhé UUID>'` ze složky obsahující také Python skript a obě systemd jednotky. Před změnami se zazálohují případné existující soubory do `/var/backups/promich-camera/`. Instalátor ověří typ a automatické připojování obou profilů i systémové uložení hesla, nainstaluje službu a timer a spustí první kontrolu. Dočasnou podrobnou diagnostiku NetworkManageru vrátí na INFO; omezené trvalé systémové logování zůstává zapnuté.

Ověření: `systemctl status promich-wifi-supervisor.timer`, `systemctl show promich-wifi-supervisor.service -p Result`, `journalctl -u promich-wifi-supervisor.service` a `python3 tests/test_wifi_supervisor.py`. Politiku střídání a přepínání testují izolované testy; samy o sobě nepotvrzují fyzický přechod na druhou síť. Pro návrat vypnout `systemctl disable --now promich-wifi-supervisor.timer` a případný právě běžící oneshot; původní síťové profily zůstaly zachované. Obnovovat starší soubory pouze po porovnání se zálohou a aktuálními změnami.
