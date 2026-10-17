# Stav projektu ProMichAiCam1

Posledn� �iv� ov��en�: **17. 10. 2026, p�ibli�n� 14:12 Europe/Berlin**. Tento soubor je �asov� z�znam; sou�asn� stav za��zen� je p�ed dal�� prac� pot�eba znovu ov��it.

## Ov��eno p��m�m �ten�m za��zen�

- Raspberry Pi 4 Model B Rev 1.5, Debian GNU/Linux 13 (trixie), 64bitov� syst�m.
- Kamera IMX500 je p��tomn� v syst�mov� evidenci I2C.
- Aplikace a u�ivatelsk� slu�ba byly z�sk�ny ze za��zen�. Zdroj aplikace se shoduje SHA256 s origin�lem; u ve�ejn� kopie slu�by byly pouze sjednoceny konce ��dk� na LF. P�vodn� otisky jsou v `docs/PUVOD.md`.
- Model SSD MobileNetV2 FPNLite 320 � 320 je instalovan�.
- `ai-camera.service` byla **inactive/dead**, `MainPID=0`, `UnitFileState=enabled`.
- Aplikace p�i kontrole neposlouchala na portu 8080. Kamera ani slu�ba nebyly p�i �ten� spu�t�ny.
- K�d pro�el kontrolou syntaxe bez spu�t�n� kamery.

## Sou�asn� obsah k�du

- N�hled 960 � 720, po�adovan�ch 15 FPS, detek�n� pr�h 55 %.
- Kreslen� r�me�k�, kategorie a jistoty rozpozn�n�; �esk� popisky vybran�ch kategori� v HTML.
- HTTP pouze na loopback rozhran� za��zen�, port 8080; p��stup pomoc� SSH p�esm�rov�n�.
- Identifikace osob jm�nem ani ukl�d�n� obrazu na disk nejsou implementovan�.

## Dosud neov��eno

- Pozitivn� �iv� detekce s r�me�kem.
- Skute�n� FPS, kvalita �iv�ho obrazu a chov�n� p�i del��m b�hu.
- P�vodn� �pln� historie chatu a jeho p�ed�vac� pozn�mka.
- P�vodn� �pravy WireGuardu na jin�m po��ta�i.
- Dostupnost projektu z dal��ho u�ivatelova ��tu/aplikace se ov��uje samostatn�; nelze ji p�edpokl�dat.

## Nav�z�n�

Nejd��v zkontrolovat aktu�ln� opr�vn�n�, Git stav a dostupnost za��zen� podle `docs/PRIPOJENI.md`. Funk�n� ov��en� n�hledu a detekce znamen� spu�t�n� kamery; prov�st ho v rozsahu u�ivatelova aktu�ln�ho zad�n�. Samotn� obnoven� dokumentace nen� d�kazem �iv� funk�nosti.

## Pravidlo p�ed�n�

Po ka�d� dokon�en� pr�ci uv�st datum, posledn� zm�nu, zp�sob ov��en�, stav slu�by p�i ukon�en� a zb�vaj�c� �koly. P�idat odkaz na commit, pokud je zn�m. Neuchov�vat novou autoritativn� verzi pouze v chatu.
