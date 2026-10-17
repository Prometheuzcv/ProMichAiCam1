# ProMichAiCam1

AI kamera se Sony IMX500 na Raspberry Pi. Tento repozit�� obsahuje zdrojov� k�d a p�ed�vac� stav projektu pro pokra�ov�n� z r�zn�ch po��ta�� a aplikac�.

## Za�ni zde

1. P�e�ti [STAV_PROJEKTU.md](STAV_PROJEKTU.md): datum posledn�ho ov��en�, skute�n� stav a zb�vaj�c� pr�ce.
2. P�e�ti [AGENTS.md](AGENTS.md): pravidla pr�ce a aktualizace p�ed�n�.
3. Pro pr�ci se za��zen�m pou�ij [n�vod k p�ipojen�](docs/PRIPOJENI.md). Schv�len� po��ta� pot�ebuje vlastn� p��stup do p��slu�n� s�t� a SSH autorizaci.
4. Po dokon�en� pr�ce aktualizuj stav, ulo� zm�ny do Gitu a ov�� jejich dostupnost na GitHubu.

## Obsah

| Soubor | ��el |
|---|---|
| `app.py` | Python aplikace: kamera, inference, detek�n� r�me�ky, HTTP n�hled |
| `deploy/ai-camera.service` | Definice u�ivatelsk� systemd slu�by |
| `STAV_PROJEKTU.md` | Posledn� ov��en� stav a dal�� pr�ce |
| `AGENTS.md` | Pokyny pro asistenta p�i nav�z�n� |
| `docs/PRIPOJENI.md` | P�ipojen� p�es m�stn� SSH alias bez zve�ejn�n� adres �i kl��� |
| `docs/PROVOZ.md` | Provozn� parametry a z�vislosti |
| `docs/PUVOD.md` | P�vod zdroje a kontroln� sou�ty |

## Nav�z�n� v nov�m chatu

Zkop�ruj odkaz na tento repozit�� a napi�:

> Pokra�ujeme v projektu ProMichAiCam1 podle tohoto repozit��e. P�e�ti README.md, STAV_PROJEKTU.md a AGENTS.md. Nejd��v ov�� dostupnost projektu a p��padn�ho za��zen�. �ekni, kter� stav je dolo�en� a co z�st�v� neov��en�.

Ve�ejn� dostupnost repozit��e umo��uje jeho �ten� bez GitHub p�ihl�en� prost�ednictv�m dostupn�ho webov�ho nebo Git n�stroje. Z�pis zm�n vy�aduje opr�vn�n�. P��stup k za��zen� je samostatn� a cloudov� chat ho nemus� m�t.

Hesla, soukrom� kl��e, s�ov� adresy konkr�tn� instalace a �pln� provozn� v�pisy pat�� mimo tento ve�ejn� repozit��.
