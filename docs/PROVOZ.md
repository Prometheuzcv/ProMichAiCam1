# Provoz a z�vislosti

Zdrojov� program je `app.py`. P�i aktu�ln� zji�t�n�m uspo��d�n� je na za��zen� v adres��i `~/ai-camera/app.py`. Jednotka `deploy/ai-camera.service` pou��v� tento adres�� relativn� k domovu p�ihl�en�ho u�ivatele.

## Z�vislosti zji�t�n� p�i obnov� 17. 10. 2026

| Bal��ek | Zji�t�n� verze |
|---|---|
| `imx500-all` | `1.14.0-1` |
| `imx500-models` | `1:1.0.0-1` |
| `python3-opencv` | `4.10.0+dfsg-5` |
| `python3-picamera2` | `0.3.37-1` |
| `rpicam-apps` | `1.14.0-1` |

Jde o bal��ky instalovan� v tehdej��m syst�mu za��zen�; tento seznam nen� tvrzen�m o aktu�ln�ch nejnov�j��ch verz�ch ani samostatn�m instala�n�m skriptem. Picamera2 a IMX500 pot�ebuj� kompatibiln� syst�mov� knihovny a hardware.

## Model a parametry

Model o�ek�van� aplikac�:

```text
/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk
```

N�hled: 960 � 720, RGB888, po�adavek 15 FPS, �est buffer�, JPEG kvalita 80. Detek�n� pr�h 0.55, nejv��e 1.5 sekundy star� posledn� v�sledek AI. �t�tky a p�evod sou�adnic vych�zej� z intrinsics modelu.

## HTTP cesty

- `/`: HTML n�hled.
- `/status`: stav aplikace v JSON.
- `/snapshot.jpg`: aktu�ln� JPEG, pokud je sn�mek dostupn�.
- `/stream.mjpg`: MJPEG stream.

Server poslouch� pouze na `127.0.0.1:8080`. Webov� server se spou�t� spole�n� s kamerov�m vl�knem. Spu�t�n� `app.py` tedy znamen� spu�t�n� kamery.

## Slu�ba

U�ivatelsk� systemd jednotka `ai-camera.service`, `Restart=on-failure`, prodleva 5 sekund. P�i obnov� byla povolen�, ale neaktivn�. Stav `enabled` s�m o sob� nepotvrzuje b��c� kameru.
