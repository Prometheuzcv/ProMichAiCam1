# Původ a kontrolní součty

Zdroje byly získány 17. 10. 2026 přímým čtením skutečného zařízení ProMichAiCam1. Původní úplnou předávací poznámku se nepodařilo získat. Tento repozitář vznikl z obnovené kopie, nikoliv z rekonstrukce programu podle fotografie.

| Soubor | SHA256 ověřené původní kopie |
|---|---|
| `app.py` | `3b84ab79fdad8e542e8c218da76d284db7ecf8bc76a44e8adb0334615a665b29` |
| `deploy/ai-camera.service` | `5a7f1dfe13683cfb5833927b266c25504fe46478d797e847c1ffa2c0a6bd05c6` |

Model není v repozitáři. Při obnově měl 3965824 bajtů a SHA256 `c7d92dd1e6dce90ac22aa8d34a8f115ed2505021987aa25dcdfad182409d526c`.

Soubor služby ve veřejném repozitáři má sjednocené konce řádků LF bez změny významu. Jeho SHA256 po sjednocení je `6c4425ce71fec7c01d74917e03a00fe55cd828974bad5d6d0d69db917b198202`. Tabulka výše uchovává otisk původního souboru ze zařízení.

Kontrolní součty popisují tento výchozí checkpoint. Při budoucí úpravě programu se SHA256 přirozeně změní; rozhodující je historie commitů a aktualizovaný stav projektu.

17. 10. 2026 byl program rozšířen o místní stránku `/display` a podporu query stringu pro obnovování streamu. Nastavení snímání a inference nebylo změněno. Nasazený `app.py` po této úpravě má SHA256 `342a2cb6a7f1082270c5b39d9b2dbaf1975417fd674fd1c0cf081ed7413287d4`; předchozí kopie byla před nasazením zálohovaná na zařízení. Spouštěč displeje má SHA256 `81551ab1168a78abdca61d72896a7e906f579412093e55070116a0aadf68289a`.

Veřejná dokumentace úmyslně vynechává osobní a síťové údaje z lokálního diagnostického předání. Repozitář není úplná záloha disku, operačního systému ani modelových binárek.

18. 10. 2026 byl nasazen dohled kamery a aktuální metriky obrazu/inference. Nasazený `app.py` má SHA256 `48d681ae4bdc36b68d10254d18a08d028ab73130480b66056cc562ac75fcf756`; shoda s pracovní kopií byla přímo ověřena. Předchozí soubor a jednotka zůstaly v záloze `~/.local/state/promich-camera/backups/20261018-recovery/`. Při návratu je nutné obnovit oba soubory, zavolat `systemctl --user daemon-reload` a restartovat kamerovou službu. Historické otisky výše zůstávají záznamem původních etap.
