# tools-android.md

Ferramentas e comandos relevantes para o alvo Android (celular Poco X3 NFC, depois tablet).

## Ferramentas necessarias

- Android SDK Platform-Tools (`adb`)
- Cabo USB de dados
- APKs oficiais arquivados em `resources/android/apk/` (ver inventario)
- BIOS dumpadas em `resources/android/bios/` quando aplicavel

## Instalacao do platform-tools

Fonte oficial: [platform-tools releases](https://developer.android.com/tools/releases/platform-tools).

Espelho local (fora do Git; ver inventario):

| Arquivo | SO | Versao (`Pkg.Revision`) |
|---|---|---|
| `resources/android/platform-tools-latest-windows.zip` | Windows | 37.0.0 |
| `resources/android/platform-tools-latest-linux.zip` | Linux | 37.0.0 |

### Windows (PowerShell)

```powershell
Expand-Archive -Path "resources\android\platform-tools-latest-windows.zip" -DestinationPath "resources\android\platform-tools-win" -Force
# Adicionar ao PATH do usuario a pasta:
#   <repo>\resources\android\platform-tools-win\platform-tools
```

### Linux

```bash
unzip -o resources/android/platform-tools-latest-linux.zip -d resources/android/platform-tools-linux
# Adicionar ao PATH:
#   export PATH="$PATH:/caminho/para/game-console/resources/android/platform-tools-linux/platform-tools"
```

A pasta extraida `platform-tools/` (e o diretorio-pai sugerido acima) tambem fica fora do versionamento se estiver sob padroes locais; o essencial e o `adb` no PATH.

Verificacao:

```bash
adb version
```

Redownload (quando `latest` mudar de revisao):

```text
https://dl.google.com/android/repository/platform-tools-latest-windows.zip
https://dl.google.com/android/repository/platform-tools-latest-linux.zip
```

## Comandos uteis

```bash
# Dispositivos
adb devices
adb -s <serial> shell getprop ro.product.model
adb shell getprop ro.product.cpu.abi

# Instalacao / remocao
adb install -r resources/android/apk/<arquivo>.apk
adb uninstall <package.id>

# Pacotes
adb shell pm list packages

# Pastas e transferencia
adb shell mkdir -p /storage/emulated/0/game-console/ROMs/snes
adb push <origem> /storage/emulated/0/game-console/ROMs/snes/
adb pull /storage/emulated/0/game-console/ROMs/snes/ ./backup-snes/

# Shell
adb shell
```

## Dependencias do fluxo Android

Documentadas em:

- `core/android-poco-x3-nfc/docs/resources-inventory.md`
- `core/android-poco-x3-nfc/docs/setup-adb.md`
- `core/android-poco-x3-nfc/docs/rom-layout.md`

## Uso recomendado

1. Preencher o inventario de APKs/BIOS.
2. Seguir `setup-adb.md` no celular.
3. Validar com `checklist.md`.
4. Repetir no tablet.

## Observacoes

- Caminho primario: ADB + APKs oficiais. Play Store e fallback restrito.
- ES-DE Android nao esta na Google Play Store.
- Nao versionar APKs, ROMs ou BIOS neste repositorio.
- Scripts ADB automatizados ainda nao existem neste passo.
