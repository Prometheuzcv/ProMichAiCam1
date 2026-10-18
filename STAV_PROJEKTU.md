# Stav projektu ProMichAiCam1

## Nejnovější práce — 18. 10. 2026, oprava ověřena po 07:21 Europe/Prague

- **Příčina reprodukovaného výpadku Wi-Fi je doložená trvalým journalem.** Běžný softwarový restart se dokončil a vznikl nový boot; kamera podle uživatele dále zobrazovala živý obraz. Raspberry se dvakrát pokusilo připojit ke stejnému přístupovému bodu domácího SSID. Oba pokusy selhaly během čtyřcestného WPA handshake (`WRONG_KEY`). NetworkManager následně čekal na nové heslo, po 120 sekundách skončil s `no-secrets` a výslovně zablokoval profil pro automatické připojení. Přitom uložené tajemství před pokusy existovalo. Nejde tedy o důkaz, že uložené heslo chybělo.
- Po uživatelově ručním vypnutí a zapnutí bylo obnoveno SSH. Jiný přístupový bod téhož SSID přijal stejné uložené heslo a spojení úspěšně dokončil přibližně 23 sekund od startu. Sken ukázal čtyři body stejného SSID; neúspěšný bod měl vyšší sílu signálu než funkční. Přesná příčina odlišného chování bodů (například rozdíl hesla nebo kompatibilita ověřování) ještě nebyla kontrolou jejich nastavení prokázaná.
- **Cílená oprava je nasazená a prošla běžným softwarovým restartem bez ručního zásahu.** `deploy/pin-working-ap.sh` navázal domácí profil na ověřený funkční BSSID a zápis byl ověřen i ve zdrojové konfiguraci Netplan. Původní konfigurace je uložená na zařízení v `/var/backups/promich-camera/20261018T052000Z-ap-pin/`; následné dokončovací ověření vytvořilo další zálohu s časem `20261018T052036Z`. Pro návrat k původnímu neomezenému BSSID použít první zálohu. Heslo a priority sítí se neměnily. Vazba omezuje roaming tohoto profilu na jeden bod. Soukromé BSSID, konfigurace a surové protokoly nejsou v repozitáři.
- První verze dokončovací kontroly nesprávně porovnávala MAC adresu s escapovaným výstupem `nmcli`; zápis samotný už proběhl, ale skript skončil před potvrzovacím markerem. Opraveno pomocí `--escape no`, dokončovací kontrola pak prošla s `AP_PIN_PERSISTED`. Syntaxe skriptu byla ověřená na Raspberry a přítomnost vazby v Netplan byla zkontrolovaná samostatně.
- Po opravě se identifikátor bootu prokazatelně změnil. Protokol potvrzuje úspěšné ověření na zvoleném bodu ve 22,15 sekundách od startu a dokončené DHCP/připojení ve 26,54 sekundách. Nové SSH spojení funguje. Kamera i kiosk jsou `active`, kamera po načtení hlásí `ready=true`, `ai_ready=true`, `error=null`, čerstvé snímky a inference přibližně při 15 FPS. Seznam selhaných systémových služeb je prázdný. Jde o jeden ověřený běžný restart po opravě, nikoli o dlouhodobou sérii testů ani o potvrzení změny nastavení problematického AP.

- Před opravou proběhl po potvrzení vypnutí hotspotu řízený restart se synchronizací trvalého journalu. SSH se neobnovilo a kontrola místního rozsahu nenašla Raspberry na jiné adrese. Uživatel potvrdil měnící se obraz kamery. Po ručním vypnutí a zapnutí byly přečteny předchozí boot i konec vypínání; výsledkem je výše doložená závada ověřování na konkrétním AP, nikoli zaseknutí restartu. U ještě staršího výpadku protokoly kvůli tehdejšímu `Storage=volatile` chybějí, takže jeho totožnou příčinu nelze zpětně prokázat.

- Před úpravou kamera i kiosk běžely přes 12 hodin bez automatického restartu. Krátký přímý test potvrdil 15 obrazových a inference výsledků za sekundu, bez chyby, s velkou rezervou RAM a CPU. Napájení nehlásilo podpětí ani throttling; teplota byla přibližně 49 °C. Wi-Fi byla připojená, Ethernet fyzicky odpojený.
- Nasazený dohled kamery obnovuje proces po výjimce nebo zastavení přibývání snímků/inferencí; systemd omezuje opakované starty. Před nasazením vznikla a kontrolním součtem byla ověřena záloha původního `app.py` a jednotky v `~/.local/state/promich-camera/backups/20261018-recovery/`.
- Aktualizované zdroje prošly HTTP a pěti zdravotními testy na notebooku i na Raspberry, včetně subprocessu se simulovanou chybou senzoru. Po nasazení se kamera připravila. Následné řízené ukončení hlavního procesu signálem SIGKILL ověřilo automatický restart systemd a obnovení čerstvých snímků i inference přibližně při 15 FPS. Kiosk při tomto testu zůstal běžet se stejným PID. Čítač `NRestarts=1` odpovídal tomuto úmyslnému testu. Skutečné zamrznutí ovladače ani studený boot nebyly vyvolané.
- `/status` nyní hlásí krátkodobé FPS, stáří obrazu a inference a skutečnou čerstvost AI. Kiosk byl znovu načten a po aktualizacích opět spuštěn; Wayland potvrdil aktivní výstup SPI-1 480 × 320. Uživatel po následném tvrdém restartu fyzicky potvrdil živý obraz.
- Příčina chyby `NetworkManager-wait-online` je doložená logem: pokus připojit nedostupnou přednostní síť skončil až po limitu 60 sekund a následovalo úspěšné připojení k záložní síti. Připravený údržbový skript zvyšuje čekací limit na 120 sekund; priority obou sítí ponechává. Nedokazuje rychlejší připojení.
- **Systémová údržba byla dokončena.** Po místním zadání hesla `sudo` byl proveden skript `deploy/maintenance.sh`; log skončil `NETWORK_WAIT_OK` a `MAINTENANCE_OK`, kořenová kontrola `dpkg --audit` nevypsala závady. Záloha přepisu čekání a seznamů balíčků je v `/var/backups/promich-camera/20261018T042941Z-maintenance/`. Služba čekání má limit 120 sekund, `TimeoutStartUSec=infinity` a po restartu této služby `Result=success`.
- Aktualizovalo se 58 balíčků, bez nových instalací a bez odstraňování. Chromium má verzi `1:155.0.8059.39-1~deb13u1+rpt1`, Picamera2 `0.3.38-1`, curl `8.14.1-2+deb13u7`; aktualizovaly se také bezpečnostní knihovny. Zbývajících 15 aktualizací (převážně VLC a rpd-common) by vyžadovalo 14 nových závislostí včetně Qt6/Wayland a nástrojů jasu. Tyto změny nebyly v této etapě aplikované. Není tedy tvrzeno, že systém nemá žádné další dostupné aktualizace.
- Po aktualizaci byly zopakovány oba testovací skripty a znovu spuštěna kamera i kiosk, aby načetly nové knihovny a Chromium. Ověřeno `ready=true`, `error=null`, čerstvé snímky/inference a přibližně 15 FPS.
- **První závěrečný softwarový restart nevedl k ověřenému obnovení síťového přístupu.** Notebook se znovu nepřipojil přes SSH. Uživatel později výslovně upřesnil, že spojení obnovil až vlastním tvrdým restartem Raspberry. Teprve po něm bylo z notebooku přímo ověřeno nové spuštění systému, aktivní kamera i kiosk, přibližně 15 FPS a nulový seznam selhaných služeb. Nelze tedy tento výsledek vydávat za úspěšný test předchozího softwarového restartu. Přesná příčina původní nedostupnosti dosud není doložená.
- V době nedostupnosti bylo Raspberry v přihlášeném hlavním routeru nalezeno podle správné Wi-Fi MAC v seznamu dosud platných DHCP zápůjček, ale nebylo mezi 37 aktuálně připojenými klienty. Čtyři pingy přímo z routeru skončily bez odpovědi. Řízení přístupu na hlavním routeru bylo vypnuté. Nastavení routeru nebylo měněné.
- Dočasný iPhone hotspot se stejným SSID a heslem byl skutečně vyzkoušen. Připojení notebooku k němu bylo ověřeno. V protokolu Raspberry po tvrdém restartu je také přímo doloženo krátké připojení k hotspotu a získání adresy z jeho podsítě, následované odpojením a přechodem k domácímu přístupovému bodu. Při následném přímém SSH ověření bylo Raspberry již na domácí Wi-Fi. Podíl telefonní VPN na obnovení přístupu nebyl prokázaný. Pro další test byl hotspot na pokyn uživatelem vypnutý, aby neexistovaly dvě různé sítě se stejným názvem.
- Původní systémový protokol měl explicitně `Storage=volatile`, proto po tvrdém restartu chyběly záznamy předchozího neúspěšného běhu. Bylo nasazeno omezené trvalé logování pomocí `deploy/enable-network-diagnostics.sh`: journald `Storage=persistent`, přibližný limit 64 MB, nejvýše sedm dní a podrobné lokální logy vybraných síťových domén. Skript skončil `NETWORK_DIAGNOSTICS_READY`, počáteční využití bylo 8 MB; záloha konfigurace vznikla v `/var/backups/promich-camera/20261018T050454Z-network-diagnostics/`. Soukromé protokoly zůstávají na zařízení, nikoliv v GitHubu. Profily, hesla, priority a přístupové body tato diagnostická změna neupravuje.
- Lehčí zobrazovač, jiný detekční model, změny přihlášení do grafické relace a odstraňování desktopových služeb nejsou provedené: současná zátěž je nevyžaduje. Fyzická přesnost dotyku, přechod mezi Wi-Fi při vyvolaném výpadku a vzdálená VPN zůstávají samostatnými testy.

Následující oddíly jsou historické checkpointy a nepřepisují novější stav uvedený výše.

Poslední živé ověření připojení, zdroje aplikace a stavu služby: **17. 10. 2026, přibližně 14:44 Europe/Berlin**. Hardware, model a balíčky byly přečteny přibližně ve 14:12 téhož dne. Tento soubor je časový záznam; současný stav zařízení je před další prací potřeba znovu ověřit.

## Ověřeno přímým čtením zařízení

- Raspberry Pi 4 Model B Rev 1.5, Debian GNU/Linux 13 (trixie), 64bitový systém.
- Kamera IMX500 je přítomná v systémové evidenci I2C.
- Aplikace a uživatelská služba byly získány ze zařízení. Zdroj aplikace se shoduje SHA256 s originálem; u veřejné kopie služby byly pouze sjednoceny konce řádků na LF. Původní otisky jsou v `docs/PUVOD.md`.
- Model SSD MobileNetV2 FPNLite 320 × 320 je instalovaný.
- `ai-camera.service` byla **inactive/dead**, `MainPID=0`, `UnitFileState=enabled`.
- Aplikace při kontrole neposlouchala na portu 8080. Kamera ani služba nebyly při čtení spuštěny.
- Kód prošel kontrolou syntaxe bez spuštění kamery.

## Současný obsah kódu

- Náhled 960 × 720, požadovaných 15 FPS, detekční práh 55 %.
- Kreslení rámečků, kategorie a jistoty rozpoznání; české popisky vybraných kategorií v HTML.
- HTTP pouze na loopback rozhraní zařízení, port 8080; přístup pomocí SSH přesměrování.
- Identifikace osob jménem ani ukládání obrazu na disk nejsou implementované.

## Dosud neověřeno

- Chování při dlouhodobém běhu a fyzická přesnost dotyku. Pozitivní detekce a krátký živý běh byly ověřené při pozdějším nastavení kiosku, viz níže.
- Původní úplná historie chatu a jeho předávací poznámka.
- Původní úpravy WireGuardu na jiném počítači.
- Dostupnost projektu z dalšího uživatelova účtu/aplikace se ověřuje samostatně; nelze ji předpokládat.

## Navázání

Nejdřív zkontrolovat aktuální oprávnění, Git stav a dostupnost zařízení podle `docs/PRIPOJENI.md`. Funkční ověření náhledu a detekce znamená spuštění kamery; provést ho v rozsahu uživatelova aktuálního zadání. Samotné obnovení dokumentace není důkazem živé funkčnosti.

## Dostupnost projektu a připojení — 17. 10. 2026

- Autoritativní veřejný repozitář: https://github.com/Prometheuzcv/ProMichAiCam1.
- Ověřeno čtení přes GitHub konektor, anonymní HTTPS stažení Gitem a samostatný webový nástroj bez přihlášení.
- U všech deseti veřejných souborů byla ověřena shoda bajtů s připraveným obsahem. Zdroj aplikace má původní SHA256 ze zařízení.
- Konkrétní další uživatelův účet nebo aplikace nebyly samostatně přihlášením testovány. Veřejné čtení nevyžaduje účet, ale potřebuje dostupný webový/Git nástroj; zápis vyžaduje oprávnění.
- Pro pracovní stanici a stálý místní počítač jsou připravené samostatné SSH klíče a klientský alias `promich-camera` s ověřováním identity serveru.
- **Autorizace dvou samostatných klíčů na Raspberry je dokončená.** Z pracovní stanice i přes stálý místní počítač bylo nezávisle ověřeno nové SSH spojení s `BatchMode=yes` bez hesla a bez předchozí dočasné řídicí relace.
- Původní položky autorizovaných klíčů zůstaly bajtově zachované; před přidáním vznikla záloha. Ověřena byla i omezení nových klíčů a oprávnění souboru.
- Pomocný instalační skript po úspěšné autorizaci původně chybně hlásil selhání kvůli koncovému znaku CR přidanému při textovém přenosu z Windows. Přenos byl změněn na přesné bajty a opakované dokončovací ověření obou spojení skončilo úspěšně s návratovým kódem 0, bez dalšího hesla.
- Zdroj aplikace se stále shoduje s původním SHA256; služba zůstala `inactive/dead`, `MainPID=0`. Kamera nebyla spuštěna.
- Instalační postup přístupu byl otestován v izolovaném dočasném domově na Linuxu: zachovává staré položky, vytváří zálohu, neopakuje přidání klíčů a nastavuje oprávnění souborů. Tento test zařízení neměnil.

## Automatické připojování Wi-Fi — ověřeno 17. 10. 2026 přibližně 15:00 Europe/Berlin

- V zařízení jsou uložené dva systémové profily známých Wi-Fi sítí, oba s automatickým připojováním. Priorita preferované sítě je 200, záložní 100; příznak ukládání hesla je u obou 0. Hesla ani soukromá konfigurace nejsou součástí repozitáře.
- Raspberry je nyní připojené k preferované Wi-Fi. Nové SSH spojení na jeho Wi-Fi adresu bylo úspěšně ověřeno z pracovní stanice i ze stálého MiniPC, s jejich samostatnými klíči.
- Ethernet zůstává připojený. Po restartu kvůli displeji bylo 17. 10. přibližně v 15:20 Europe/Berlin ověřeno opětovné připojení k preferované Wi-Fi. Samostatný test po fyzickém odpojení kabelu a ztrátě jedné z Wi-Fi sítí dosud neproběhl.
- Připojování k libovolným otevřeným sítím není nastavené. VPN klient na Raspberry a vzdálený přístup přes mobilní hotspot dosud nejsou nastavené ani ověřené.
- Kamerová služba zůstává neaktivní; kamera nebyla spuštěna.

## GPIO displej 3,5 palce — diagnostika 17. 10. 2026

- Uživatel připojil displej označený 3.5inch RPi Display, 480 × 320, XPT2046; hlásí bílé podsvícení. Provedení odpovídá rodině MPI3501/ILI9486.
- Původní diagnostika zjistila vypnuté SPI a chybějící overlay displeje. Tento stav byl opraven.
- V bootovací konfiguraci je nyní dtparam=spi=on a dtoverlay=piscreen,drm,speed=16000000,rotate=0. Používají se již instalované systémové ovladače; lokální instalační pomocník před zápisem vytváří zálohu pod /var/backups/promich-display/.
- **Oprava je nasazená a obraz je fyzicky potvrzený uživatelem.** Po startu v 15:11:03 systém při kontrole přibližně v 15:20 Europe/Berlin registruje SPI-1 jako připojený a zapnutý výstup 480 × 320. Labwc zobrazuje plochu na tomto výstupu.
- Dotykový řadič je registrovaný jako ADS7846 Touchscreen na spi0.1. Fyzická funkce a přesnost dotyku zatím nebyly potvrzené.
- Kamerová služba po restartu běží, MainPID při kontrole 1376. Diagnostické čtení ji nespouštělo ani nezastavovalo; dřívější záznam inactive je historický.

## Automatický živý obraz s detekcí — ověřeno 17. 10. 2026 po restartu v 15:30 Europe/Berlin

- Po úplném restartu se automaticky spustily `ai-camera.service` (15:30:21) a `ai-camera-display.service` (15:30:27), bez ručního otevření okna. Kontrola výstupu SPI-1 po startu potvrdila skutečný obraz kamery přes celou plochu 480 × 320 a stav AI.
- Nová stránka `/display` používá stávající MJPEG s detekčními rámečky, zachovává poměr stran a obnovuje spojení při výpadku. Prohlížeč čeká na místní server; stránka zobrazuje načítání modelu nebo chybu. Prohlížeč má samostatný profil, bez překladových bublin a výzvy ke klíčence. Pro běžné zobrazení není potřeba dotyk ani internet.
- Byla ověřena pozitivní živá detekce `person` s jistotou 0.68 a souřadnicemi rámečku; snímek výstupu displeje při dalším měření obsahoval rámečky a popisky. Počet výsledků inference i obrazových snímků rostl. Počáteční průměrné FPS po startu zahrnuje dobu načítání; není to měření dlouhodobé obnovovací frekvence panelu.
- Funkční HTTP test pokryl původní stránku, novou stránku, stav a MJPEG s query stringem pro opakované připojení. Na zařízení prošel také restart kamerové služby: kamera se znovu připravila a kiosk zůstal běžet. Poté prošel úplný restart Raspberry a nové SSH připojení; domácí Wi-Fi byla znovu připojená.
- Dotyk při 35sekundovém záznamu poskytl 22 stisků a 22 uvolnění, souřadnice i tlak. Byl opraven uživatelský profil labwc: chyběla prázdná vazba `Root / Left / Press`, kterou používá systémová konfigurace Raspberry Pi. Tím se odstraní otevírání menu plochy běžným levým kliknutím. Přesnost a pohodlnost dotyku po opravě zatím nejsou fyzicky potvrzené; parametry tlaku nebyly měněné.
- Před změnami byla na zařízení vytvořena záloha původní aplikace, konfigurace plochy a případných existujících souborů v `~/.local/state/promich-camera/backups/20261017T132617Z/`. Původní soubor aplikace je zachovaný. Ovladač displeje a model se neměnily.
- Nasazené zdroje, jednotka, fragmenty konfigurace a postup návratu jsou v `deploy/` a `docs/DISPLEJ.md`. Soukromé snímky kamery a diagnostika nejsou součástí veřejného repozitáře.

## Pravidlo předání

Po každé dokončené práci uvést datum, poslední změnu, způsob ověření, stav služby při ukončení a zbývající úkoly. Přidat odkaz na commit, pokud je znám. Neuchovávat novou autoritativní verzi pouze v chatu.
