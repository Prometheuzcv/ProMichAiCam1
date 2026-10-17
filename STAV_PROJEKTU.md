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

- Pozitivní živá detekce s rámečkem.
- Skutečné FPS, kvalita živého obrazu a chování při delším běhu.
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
- Ethernet zůstává připojený. Samostatný test po fyzickém odpojení kabelu, restartu a ztrátě jedné z Wi-Fi sítí dosud neproběhl.
- Připojování k libovolným otevřeným sítím není nastavené. VPN klient na Raspberry a vzdálený přístup přes mobilní hotspot dosud nejsou nastavené ani ověřené.
- Kamerová služba zůstává neaktivní; kamera nebyla spuštěna.

## GPIO displej 3,5 palce — diagnostika 17. 10. 2026

- Uživatel připojil displej označený 3.5inch RPi Display, 480 × 320, XPT2046; hlásí bílé podsvícení. Provedení odpovídá rodině MPI3501/ILI9486.
- Přímá kontrola zjistila vypnuté SPI v device tree a chybějící overlay displeje v bootovací konfiguraci. Labwc má pouze virtuální výstup NOOP; fyzický SPI displej není registrovaný.
- Systém již obsahuje moduly DRM ILI9486, ADS7846 a overlay piscreen s volbou drm. Připravená lokální oprava přidá dtparam=spi=on a dtoverlay=piscreen,drm,speed=16000000,rotate=0; původní konfiguraci zálohuje a zachová ostatní nastavení.
- Oprava zatím nebyla zapsána do zařízení: vyžaduje místní zadání hesla pro sudo. Následně je potřeba restart a ověření registrace displeje, skutečného obrazu a dotyku.
- Po posledním startu zařízení je kamerová služba aktivní, MainPID při kontrole 1347, aktivní od 15:00:20 Europe/Berlin. Diagnostika službu nespouštěla ani nezastavovala; dřívější záznam inactive je historický.

## Pravidlo předání

Po každé dokončené práci uvést datum, poslední změnu, způsob ověření, stav služby při ukončení a zbývající úkoly. Přidat odkaz na commit, pokud je znám. Neuchovávat novou autoritativní verzi pouze v chatu.
