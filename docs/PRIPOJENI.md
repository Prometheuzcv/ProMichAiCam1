# P�ipojen� k za��zen�

Tento dokument neobsahuje adresy konkr�tn� soukrom� s�t�, u�ivatelsk� hesla ani kl��e. Ty z�st�vaj� v konfiguraci schv�len�ch po��ta��.

## �ten� projektu

Ve�ejn� repozit�� lze ��st webov�m/Git n�strojem nebo st�hnout jako ZIP. Soukrom� ��et �i aplikace pot�ebuje pro z�pis vlastn� GitHub opr�vn�n�. Automatickou dostupnost konektoru v jin�m ��tu nep�edpokl�dat.

## P��stup k Raspberry

Na p�ipraven�m m�stn�m po��ta�i nebo st�l�m MiniPC je c�lov�m rozhran�m alias:

```sh
ssh promich-camera
```

Alias nen� ve�ejn� slu�ba ani univerz�ln� p�ihla�ovac� �daj. Funguje pouze tam, kde vlastn�k nakonfiguroval cestu k za��zen�, individu�ln� SSH kl�� a ov��en� kl�� serveru. Ka�d� nov� po��ta� vy�aduje vlastn� autorizaci.

Nejprve ov��it identitu a stav, nap��klad:

```sh
ssh promich-camera 'hostname; systemctl --user is-active ai-camera.service'
```

N�hled aplikace je ur�en� pro loopback za��zen� na portu 8080. Po v�slovn� zadan�m spu�t�n� kamery lze ze schv�len�ho m�stn�ho po��ta�e pou��t:

```sh
ssh -N -L 127.0.0.1:8088:127.0.0.1:8080 promich-camera
```

Potom se n�hled otev�r� lok�ln� na `http://127.0.0.1:8088/`. Samotn� p�esm�rov�n� aplikaci nespust�.

## Kdy� p�ipojen� chyb�

Ov��it nejprve mo�nosti prost�ed� a jeho p��stup do s�t�. Znovu neprohled�vat n�hodn� star� chaty. Vlastn�k za��zen� rozhoduje o autorizaci dal��ho po��ta�e; p�ihla�ovac� �daje se nevkl�daj� do chatu ani Gitu.
