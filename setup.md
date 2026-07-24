# setup.md

## Pre-requisitos

- Git instalado.
- Acesso de leitura ao repositorio game-console.
- Para Linux: Ubuntu/Kubuntu 26 (ou proxima) com `sudo`, rede e permissao Flatpak.
- Para Windows 11: conta com direitos de instalacao de drivers e apps.
- Para Android: Poco X3 NFC (depois tablet) com depuracao USB / ADB; APKs oficiais em `resources/android/` (ES-DE pago via canal oficial).

## Instalacao (clone / uso local)

1. Clonar ou abrir o repositorio na pasta raiz `game-console`.
2. Confirmar que existem `spec_root.md`, `flow.md`, `rules.md` e `core/`.
3. Ler `readme.md` e o README do alvo em `core/`.

## Bootstrap documental

Ja realizado na inicializacao do repositorio. Nao ha script de bootstrap da raiz neste momento.

## Variaveis de ambiente

Nenhuma variavel obrigatoria para uso documental.

Scripts Bash usam `REPO_ROOT` detectado em runtime (pasta raiz `game-console`).

## Verificacoes

```text
# Na raiz do repositorio
- [ ] spec_root.md existe
- [ ] core/android-poco-x3-nfc/README.md existe
- [ ] core/android-poco-x3-nfc/docs/resources-inventory.md existe
- [ ] core/android-poco-x3-nfc/docs/setup-adb.md existe
- [ ] resources/android/README.md existe
- [ ] tools-android.md existe
- [ ] core/pc-modern-emulation/windows-11/README.md existe
- [ ] core/pc-modern-emulation/linux-ubuntu-26/README.md existe
- [ ] core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh existe
```

## Execucao inicial

### Android (caminho primario)

1. Baixar/comprar APKs e preencher `core/android-poco-x3-nfc/docs/resources-inventory.md`.
2. Colocar arquivos em `resources/android/apk/` e `resources/android/bios/`.
3. Seguir `core/android-poco-x3-nfc/docs/setup-adb.md` no celular (Poco X3 NFC).
4. Validar com `core/android-poco-x3-nfc/docs/checklist.md`.
5. Repetir no tablet.

Ferramentas: `tools-android.md`. Fallback Play Store (restrito): `core/android-poco-x3-nfc/docs/setup-play-store.md`.

### Linux (emulacao)

```bash
bash core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh
```

Desinstalacao reversa:

```bash
bash core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh --uninstall
```

### Windows 11

Seguir `core/pc-modern-emulation/windows-11/README.md` (passos manuais).

## Solucao de problemas

| Sintoma | Acao |
|---|---|
| Script nao acha a raiz | Executar a partir de qualquer subpasta localizavel sob `game-console`; se falhar, conferir o nome da pasta raiz |
| Flatpak falha | Conferir rede, Flathub e permissao do usuario |
| apt pede senha | Usar conta com sudo; o script nao contorna autenticacao |
| Host nao e Ubuntu 26 | Validar pacotes equivalentes e registrar desvio em `reports/` |
| `adb devices` vazio / unauthorized | Cabo de dados, depuracao USB, reautorizar PC |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | Desinstalar build anterior (ex.: Play Store) antes do APK oficial |
