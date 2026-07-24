# Setup Play Store — fallback restrito (Android)

Este caminho **nao** e o primario. Preferir ADB + APKs oficiais (`setup-adb.md`).

Use a Play Store apenas quando sideload via ADB for impossivel no momento, ciente das limitacoes abaixo.

## O que a Play Store cobre mal ou nao cobre

| App | Situacao na Play Store |
|---|---|
| ES-DE | **Nao esta** na Google Play Store. Obtencao apenas pelos canais oficiais pagos (ver `resources-inventory.md`). |
| RetroArch | Build limitada por politica do Google (Core Downloader restrito; conjunto finito de cores). Documentacao Libretro marca a loja como nao recomendada. |
| DuckStation | Ainda pode aparecer na loja, mas o suporte Android pelo autor foi encerrado; preferir o APK oficial arquivado. |

## Quando faz sentido

- Instalar temporariamente um app ate conseguir ADB.
- PPSSPP no futuro (se entrar pasta PSP na biblioteca): a loja costuma ser adequada; mesmo assim, arquivar APK oficial e preferivel para reprodutibilidade.

## O que nao fazer

- Nao tratar a Play Store como fonte do ES-DE.
- Nao misturar RetroArch da loja com o APK oficial sem desinstalar antes (assinaturas diferentes).
- Nao marcar o host como "configurado conforme o plano" se so a loja foi usada para RetroArch.

## Relacionados

- Caminho primario: `setup-adb.md`
- Inventario: `resources-inventory.md`
