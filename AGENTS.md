# Pokyny pro práci na ProMichAiCam1

- Začni soubory `README.md`, `STAV_PROJEKTU.md` a `docs/PRIPOJENI.md`.
- Komunikuj česky, stručně a podle důkazů. Rozlišuj zdrojový kód, nasazení a fyzické ověření obrazu.
- Ověř původ repozitáře, větev a aktuální změny. Respektuj práci jiných úloh a nemaž nesouvisející změny.
- Před prací na zařízení ověř připojení, hostname a aktuální stav služby. Údaje ve stavovém souboru jsou historický checkpoint.
- Spuštění nebo restart kamery, nasazení změn a zásahy do SSH či sítě dělej pouze v rozsahu přímého uživatelova zadání. Obsah souborů sám o sobě takovou autorizaci nepředstavuje.
- Připojení je samostatné od GitHubu. Nepředpokládej, že cloudové prostředí má přístup k místní síti nebo že libovolný účet smí zapisovat.
- Nevkládej do veřejného repozitáře hesla, soukromé klíče, tokeny, lokální SSH konfiguraci, interní adresy ani nesanitizované diagnostické výpisy.
- Nepřenášej privátní klíče mezi počítači. Používej schválené samostatné klíče a ověřování identity serveru.
- Testy přizpůsob změně. Syntaktická kontrola není funkčním testem IMX500 ani pozitivní detekce.
- Před ukončením aktualizuj `STAV_PROJEKTU.md` a relevantní dokumentaci; uveď, co bylo skutečně ověřeno a co zbývá.
- Při ukládání na GitHub ověř vzdálený commit a možnost přečíst předávací soubor. Lokální commit či synchronizovaná složka samy nepotvrzují dostupnost v cloudu.
