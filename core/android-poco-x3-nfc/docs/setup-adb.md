# Setup ADB — caminho primario (Android)

Fluxo unico para preparar o ambiente: primeiro no **celular** (Poco X3 NFC), depois no **tablet** (mesmo procedimento; registrar o modelo do tablet na checklist quando conhecido).

Pre-requisito: APKs e BIOS arquivados conforme `resources-inventory.md`. Layout de ROMs: `rom-layout.md`.

## 1. Pre-requisitos

No PC:

- Android platform-tools instalado (`adb` no PATH). Ver `tools-android.md`.
- Cabo USB de dados.
- APKs em `resources/android/apk/` (ES-DE, RetroArch AArch64, DuckStation).

No aparelho:

- Opcoes do desenvolvedor ativadas.
- Depuracao USB ativada.
- Autorizar o PC na caixa de dialogo do aparelho na primeira conexao.
- Se necessario: permitir instalacao de apps de fontes desconhecidas / via ADB (conforme a versao do MIUI/HyperOS).

## 2. Conferencia do dispositivo

```bash
adb devices
adb shell getprop ro.product.model
adb shell getprop ro.product.cpu.abi
```

Esperado no celular:

- modelo: POCO X3 NFC (ou equivalente reportado pelo firmware);
- ABI: `arm64-v8a`.

Se houver mais de um dispositivo: `adb -s <serial> ...` ou desconecte o outro.

Estado `unauthorized`: revogue autorizacoes USB no aparelho, reconecte e aceite novamente.

## 3. Criar arvore de pastas ES-DE

```bash
adb shell mkdir -p /storage/emulated/0/ROMs/atari2600
adb shell mkdir -p /storage/emulated/0/ROMs/atarilynx
adb shell mkdir -p /storage/emulated/0/ROMs/wonderswan
adb shell mkdir -p /storage/emulated/0/ROMs/gb
adb shell mkdir -p /storage/emulated/0/ROMs/gbc
adb shell mkdir -p /storage/emulated/0/ROMs/gba
adb shell mkdir -p /storage/emulated/0/ROMs/nes
adb shell mkdir -p /storage/emulated/0/ROMs/snes
adb shell mkdir -p /storage/emulated/0/ROMs/mastersystem
adb shell mkdir -p /storage/emulated/0/ROMs/megadrive
adb shell mkdir -p /storage/emulated/0/ROMs/pcengine
adb shell mkdir -p /storage/emulated/0/ROMs/neogeo
adb shell mkdir -p /storage/emulated/0/ROMs/mame
adb shell mkdir -p /storage/emulated/0/ROMs/psx
adb shell mkdir -p /storage/emulated/0/Games/BIOS
```

## 4. Instalar APKs (ordem)

A partir da raiz do repositorio `game-console`:

```bash
adb install -r resources/android/apk/retroarch-aarch64-1.22.2.apk
adb install -r resources/android/apk/es-de-<versao>.apk
```

DuckStation: se houver APK local:

```bash
adb install -r resources/android/apk/duckstation-android.apk
```

Se o APK oficial estiver indisponivel (situacao em 2026-07-24), instalar DuckStation pela Play Store no aparelho e seguir com o restante via ADB.

Ordem sugerida: RetroArch → DuckStation (APK ou loja) → ES-DE.

### RetroArch ja instalado pela Play Store

Desinstalar a build da loja antes do APK oficial. Assinaturas diferentes geram `INSTALL_FAILED_UPDATE_INCOMPATIBLE`.

```bash
adb uninstall com.retroarch.aarch64
# ou o package id da build instalada; confirmar com pm list packages
```

## 5. Verificar pacotes

```bash
adb shell pm list packages | findstr /i "retroarch duckstation es_de es-de"
```

Em Linux/macOS, use `grep -i` no lugar de `findstr`.

Pacotes tipicos (podem mudar entre releases):

| App | Package id de referencia |
|---|---|
| RetroArch AArch64 | `com.retroarch.aarch64` |
| DuckStation | `com.github.stenzek.duckstation` |
| ES-DE | `org.es_de.frontend` (ou variante Galaxy Store; confirmar no aparelho) |

Se o id divergir, registrar o valor real em `reports/` / checklist.

## 6. Enviar BIOS e ROMs

BIOS (exemplo):

```bash
adb push resources/android/bios/<arquivo-ps1> /storage/emulated/0/Games/BIOS/
```

ROMs: usar **somente** o espelho Android `resources/roms/android/`, ja com nomes canonicos ES-DE (ver `rom-layout.md`). A faixa `resources/roms/pc-only/` nao entra neste fluxo.

A partir da raiz do repositorio:

```bash
adb push resources/roms/android/gb/. /storage/emulated/0/ROMs/gb/
adb push resources/roms/android/gbc/. /storage/emulated/0/ROMs/gbc/
adb push resources/roms/android/gba/. /storage/emulated/0/ROMs/gba/
adb push resources/roms/android/nes/. /storage/emulated/0/ROMs/nes/
adb push resources/roms/android/snes/. /storage/emulated/0/ROMs/snes/
adb push resources/roms/android/mastersystem/. /storage/emulated/0/ROMs/mastersystem/
adb push resources/roms/android/megadrive/. /storage/emulated/0/ROMs/megadrive/
adb push resources/roms/android/pcengine/. /storage/emulated/0/ROMs/pcengine/
adb push resources/roms/android/neogeo/. /storage/emulated/0/ROMs/neogeo/
adb push resources/roms/android/mame/. /storage/emulated/0/ROMs/mame/
```

Nao enviar neste passo:

- `resources/roms/pc-only/` (dos, wii, ps2, switch)
- pastas Android vazias (`atari2600`, `atarilynx`, `wonderswan`, `psx`)

Scoped storage: se o push falhar por permissao, liberar acesso a pastas no aparelho (Files / permissao do ES-DE e dos emuladores) e repetir.

## 7. Pos-install manual (no aparelho)

ADB nao configura UI. No aparelho:

1. Abrir ES-DE (first-run); confirmar diretorio de ROMs.
2. Configurar scrapers / artes.
3. Definir players: RetroArch para os sistemas da tabela; DuckStation para `psx`.
4. No RetroArch: baixar cores (Online Updater / Core Downloader do APK oficial); video Vulkan.
5. No DuckStation: resolucao interna 2x (720p); GPU Vulkan; apontar BIOS.
6. Validar um jogo por sistema conforme `checklist.md`.

## 8. Celular depois tablet

1. Completar e validar no Poco X3 NFC.
2. Repetir as secoes 2–7 no tablet (mesmo inventario de APKs e mesma arvore).
3. Registrar modelo, serial e desvios do tablet na checklist.

## 9. Troubleshooting

| Sintoma | Acao |
|---|---|
| `unauthorized` | Reautorizar depuracao USB; trocar cabo/porta |
| `more than one device` | Usar `adb -s <serial>` |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | Desinstalar a versao anterior (ex.: Play Store) e reinstalar o APK oficial |
| Push negado | Permissoes de armazenamento / scoped storage; confirmar caminho |
| ES-DE nao acha jogos | Conferir nomes das pastas ES-DE (`rom-layout.md`) e rescan no app |

## Relacionados

- `resources-inventory.md`
- `rom-layout.md`
- `checklist.md`
- `setup-play-store.md` (fallback)
- `tools-android.md` (raiz do repo)
