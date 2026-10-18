# Software kamery a možnosti AI

Ověřeno podle nasazeného zdroje a živé kontroly 18. 10. 2026. Přehled možností není tvrzením, že jsou všechny funkce implementované.

## Co skutečně běží

Vlastní Python aplikace `app.py` používá Picamera2 a jeho podporu IMX500, OpenCV a jednoduchý místní HTTP server. Při kontrole byly instalované Picamera2 `0.3.38-1`, OpenCV `4.10.0+dfsg-5`, `imx500-all` `1.14.0-1` a `imx500-models` `1:1.0.0-1`.

Model `imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk` se nahrává do AI akcelerátoru Sony IMX500 v kameře. Kamera provádí inferenci a Raspberry přijímá výsledky, převádí souřadnice, kreslí rámečky a připravuje JPEG. V tomto modelu označení `pp` znamená zahrnuté následné zpracování na IMX500. OpenCV v našem programu nepočítá celou neuronovou síť na CPU Raspberry.

Oficiální podklady: [architektura AI Camera](https://www.raspberrypi.com/documentation/accessories/ai-camera.html) a [IMX500 Model Zoo](https://github.com/raspberrypi/imx500-models).

## Aktuální funkce a nastavení

- Detekce běžných objektů: předtrénovaný model s kategoriemi COCO, název, skóre a rámeček každého výsledku.
- AI vstup 320 × 320; zobrazovaný obraz 960 × 720. Jde o různá rozlišení. Větší náhled sám nezvýší detail vstupu modelu.
- Požadavek 15 FPS, práh zobrazení 0,55, JPEG kvalita 80; výsledky starší než 1,5 sekundy se nevykreslují.
- HTTP náhled, MJPEG, snímek JPEG a JSON stav; místní celoobrazovkový displej přes Chromium.
- Automatický start, sledování čerstvosti obrazu/inference a obnovení po chybě procesu.
- Při živé kontrole 18. 10. běželo přibližně 15 snímků i výsledků inference za sekundu. Byla rovněž zachycena detekce person. Jde o naměřenou aktuální funkci, nikoli o test přesnosti všech kategorií.

## Co lze doplnit do aplikace

Počítání průchodů vyžaduje sledování objektů v čase a definici čáry či zóny. Hlídání prostoru vyžaduje pravidla a časové filtrování. Ukládání událostí vyžaduje úložiště a pravidla uchovávání. Tyto funkce nejsou součástí dosavadního detekčního náhledu. Stejně tak není implementovaná databáze osob, rozpoznávání totožnosti, OCR ani čtení SPZ.

Na zařízení jsou i modely pro jiné úlohy: například NanoDet/EfficientDet pro detekci, HigherHRNet/PoseNet pro polohu těla, DeepLabv3Plus pro segmentaci a klasifikační modely. Jejich přítomnost neznamená, že běží. Aktivní aplikace zpracovává detekční výstupy jednoho konkrétního modelu; pro jinou úlohu je nutné upravit zpracování a zobrazení výsledků. Novější katalog modelů může obsahovat soubory, které v instalovaném balíčku ještě nejsou.

## Omezení a směr další práce

Model rozpoznává naučené kategorie; samotný provoz ho neučí nové předměty. Malé či vzdálené objekty, světlo a ostrost ovlivňují výsledek. Kamera má 12,3MP snímač a ruční mechanické ostření; aktuální detekce nevyužívá plné rozlišení jako vstup AI. Viz [specifikace](https://www.raspberrypi.com/products/ai-camera/).

Vlastní model musí vyhovět podporovaným operacím a prostředkům IMX500 a projít kvantizací/převodem a zabalením. Příprava se obvykle provádí na výkonnějším počítači. Viz [nasazení modelů](https://www.raspberrypi.com/documentation/accessories/ai-camera.html#model-deployment).

Nejprve určit konkrétní cíl (počítání osob, hlídání zóny, konkrétní předmět), pak vybrat model a doplnit logiku. Pi 4B současnou detekci s akcelerátorem kamery prokazatelně obsluhuje. Výkon nových funkcí musí být změřený samostatně.
