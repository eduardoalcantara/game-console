# tools-android.md

Ferramentas e comandos relevantes para o alvo Android (celular Poco X3 NFC, depois tablet).

## Ferramentas necessarias

- Android SDK Platform-Tools (`adb`)
- Cabo USB de dados
- APKs oficiais arquivados em `resources/android/apk/` (ver inventario)
- BIOS dumpadas em `resources/android/bios/` quando aplicavel

## Instalacao do platform-tools

Fonte oficial: `https://developer.android.com/tools/releases/platform-tools`

Extrair e adicionar o diretorio ao PATH do usuario, ou invocar `adb` pelo caminho completo.

Verificacao:

```bash
adb version
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
adb shell mkdir -p /storage/emulated/0/ROMs/snes
adb push <origem> /storage/emulated/0/ROMs/snes/
adb pull /storage/emulated/0/ROMs/snes/ ./backup-snes/

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
