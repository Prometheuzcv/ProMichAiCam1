# ProMichAiCam1

AI kamera se Sony IMX500 na Raspberry Pi. Tento repozitář obsahuje zdrojový kód a předávací stav projektu pro pokračování z různých počítačů a aplikací.

## Začni zde

1. Přečti [STAV_PROJEKTU.md](STAV_PROJEKTU.md): datum posledního ověření, skutečný stav a zbývající práce.
2. Přečti [AGENTS.md](AGENTS.md): pravidla práce a aktualizace předání.
3. Pro práci se zařízením použij [návod k připojení](docs/PRIPOJENI.md). Schválený počítač potřebuje vlastní přístup do příslušné sítě a SSH autorizaci.
4. Po dokončení práce aktualizuj stav, ulož změny do Gitu a ověř jejich dostupnost na GitHubu.

## Obsah

| Soubor | Účel |
|---|---|
| `app.py` | Python aplikace: kamera, inference, detekční rámečky, HTTP náhled |
| `deploy/ai-camera.service` | Definice uživatelské systemd služby |
| `STAV_PROJEKTU.md` | Poslední ověřený stav a další práce |
| `AGENTS.md` | Pokyny pro asistenta při navázání |
| `docs/PRIPOJENI.md` | Připojení přes místní SSH alias bez zveřejnění adres či klíčů |
| `docs/PROVOZ.md` | Provozní parametry a závislosti |
| `docs/PUVOD.md` | Původ zdroje a kontrolní součty |

## Navázání v novém chatu

Zkopíruj odkaz na tento repozitář a napiš:

> Pokračujeme v projektu ProMichAiCam1 podle tohoto repozitáře. Přečti README.md, STAV_PROJEKTU.md a AGENTS.md. Nejdřív ověř dostupnost projektu a případného zařízení. Řekni, který stav je doložený a co zůstává neověřené.

Veřejná dostupnost repozitáře umožňuje jeho čtení bez GitHub přihlášení prostřednictvím dostupného webového nebo Git nástroje. Zápis změn vyžaduje oprávnění. Přístup k zařízení je samostatný a cloudový chat ho nemusí mít.

Hesla, soukromé klíče, síťové adresy konkrétní instalace a úplné provozní výpisy patří mimo tento veřejný repozitář.
