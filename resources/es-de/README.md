# resources/es-de

Espelho de artefatos do frontend ES-DE.

| Pasta | Conteudo | Git? |
|---|---|---|
| `themes/` | Temas oficiais (grupo GitLab) | Versionado (~530 MB) |
| `downloaded_media/` | Capas, screenshots, videos, etc. (scrape) | **Fora do Git** |
| `gamelists/` | `gamelist.xml` por sistema (metadados) | **Fora do Git** |

## Origem tipica (Razr)

```text
/storage/emulated/0/game-console/ES-DE/downloaded_media/
/storage/emulated/0/game-console/ES-DE/gamelists/
```

Pull:

```bash
adb pull /sdcard/game-console/ES-DE/downloaded_media/. resources/es-de/downloaded_media/
adb pull /sdcard/game-console/ES-DE/gamelists/. resources/es-de/gamelists/
```

Push (reenviar a outro aparelho):

```bash
adb push resources/es-de/downloaded_media/. /sdcard/game-console/ES-DE/downloaded_media/
adb push resources/es-de/gamelists/. /sdcard/game-console/ES-DE/gamelists/
```

Nao versionar capas nem gamelists (tamanho + conteudo de terceiro via ScreenScraper). Manter so o espelho local no Drive.
