# Připojení k zařízení

Tento dokument neobsahuje adresy konkrétní soukromé sítě, uživatelská hesla ani klíče. Ty zůstávají v konfiguraci schválených počítačů.

## Čtení projektu

Veřejný repozitář lze číst webovým/Git nástrojem nebo stáhnout jako ZIP. Soukromý účet či aplikace potřebuje pro zápis vlastní GitHub oprávnění. Automatickou dostupnost konektoru v jiném účtu nepředpokládat.

## Přístup k Raspberry

Na připraveném místním počítači nebo stálém MiniPC je cílovým rozhraním alias:

```sh
ssh promich-camera
```

Alias není veřejná služba ani univerzální přihlašovací údaj. Funguje pouze tam, kde vlastník nakonfiguroval cestu k zařízení, individuální SSH klíč a ověřený klíč serveru. Každý nový počítač vyžaduje vlastní autorizaci.

K 17. 10. 2026 přibližně 14:44 Europe/Berlin bylo ověřeno samostatné spojení bez hesla z vlastníkovy připravené pracovní stanice i ze stálého místního počítače. Používají rozdílné klíče a kontrolují identitu serveru. Tato připojení nepotřebují původní dočasnou přihlašovací relaci. Nový počítač nebo jiná cloudová aplikace tím automaticky autorizované nejsou.

Nejprve ověřit identitu a stav, například:

```sh
ssh promich-camera 'hostname; systemctl --user is-active ai-camera.service'
```

Náhled aplikace je určený pro loopback zařízení na portu 8080. Po výslovně zadaném spuštění kamery lze ze schváleného místního počítače použít:

```sh
ssh -N -L 127.0.0.1:8088:127.0.0.1:8080 promich-camera
```

Potom se náhled otevírá lokálně na `http://127.0.0.1:8088/`. Samotné přesměrování aplikaci nespustí.

## Když připojení chybí

Ověřit nejprve možnosti prostředí a jeho přístup do sítě. Znovu neprohledávat náhodně staré chaty. Vlastník zařízení rozhoduje o autorizaci dalšího počítače; přihlašovací údaje se nevkládají do chatu ani Gitu.
