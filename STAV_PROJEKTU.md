# Stav projektu ProMichAiCam1

Poslední živé ověření: **17. 10. 2026, přibližně 14:12 Europe/Berlin**. Tento soubor je časový záznam; současný stav zařízení je před další prací potřeba znovu ověřit.

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

## Pravidlo předání

Po každé dokončené práci uvést datum, poslední změnu, způsob ověření, stav služby při ukončení a zbývající úkoly. Přidat odkaz na commit, pokud je znám. Neuchovávat novou autoritativní verzi pouze v chatu.
