# Stav projektu ProMichAiCam1

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
