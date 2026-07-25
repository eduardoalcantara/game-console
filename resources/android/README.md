# resources/android

Contrato da pasta de recursos locais para o alvo Android (celular, depois tablet).

## O que entra aqui

| Subpasta | Conteudo |
|---|---|
| `apk/` | APKs: RetroArch (automatizavel), ES-DE (manual), DuckStation se disponivel |
| `bios/` | BIOS dumpadas pelo operador (manual) |
| `config/` | `retroarch.cfg` (e overrides) puxados apos calibracao na GUI; ver `config/README.md` |

Biblioteca de ROMs:

- `resources/roms/android/` — envio aos aparelhos Android
- `resources/roms/pc-only/` — so PC (Wii, PS2, Switch, DOS, …)

Ver `resources/roms-structure.md` e `core/android-poco-x3-nfc/docs/rom-layout.md`.

Inventario normativo: `core/android-poco-x3-nfc/docs/resources-inventory.md`.

## O que nunca e commitado

- Arquivos `.apk`, `.apks`, `.xapk`, `.apkm`, `.aab`, `.obb`
- Compactados (`.7z`, `.zip`, `.rar`, `.tar*`) usados para transporte dos binarios
- BIOS, ROMs, ISOs e dumps
- Links ou espelhos de terceiros como fonte canonica

O Git versiona apenas este README e os `.gitkeep`. Binarios ficam locais (cobertos por `.gitignore`).

## Convencao de nomes (APK)

```text
es-de-<versao>.apk
retroarch-aarch64-<versao>.apk
duckstation-<data-ou-versao>.apk
```

Exemplo: `retroarch-aarch64-1.20.0.apk`, `duckstation-2025-05-01.apk`.

Excecao: quando o canal oficial ja entrega um nome versionado (caso do ES-DE, `ES-DE_3.4.1-58.apk`), manter o nome original e registrar no inventario.

## Convencao de nomes (BIOS)

Usar nomes descritivos curtos sem espacos; nao publicar hashes de dumps ilegais em issues publicas se isso expor a origem. Registrar versao/hash apenas no inventario local do operador.

## Fluxo

1. Conferir `resources-inventory.md` (colunas Manual / Automatizavel).
2. Garantir RetroArch em `apk/` (ja baixado se inventario estiver atualizado).
3. Operador coloca BIOS; DuckStation via Play Store ou APK proprio (ES-DE ja arquivado).
4. Instalar via ADB conforme `core/android-poco-x3-nfc/docs/setup-adb.md`.
