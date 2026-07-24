# setup.md

## Pre-requisitos

- Git instalado.
- Acesso de leitura ao repositorio game-console.
- Para Linux: Ubuntu/Kubuntu 26 (ou proxima) com `sudo`, rede e permissao Flatpak.
- Para Windows 11: conta com direitos de instalacao de drivers e apps.
- Para Android: Poco X3 NFC com acesso a Play Store / sideload controlado.

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
- [ ] core/pc-modern-emulation/windows-11/README.md existe
- [ ] core/pc-modern-emulation/linux-ubuntu-26/README.md existe
- [ ] core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh existe
```

## Execucao inicial

### Linux (emulacao)

```bash
bash core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh
```

Desinstalacao reversa:

```bash
bash core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh --uninstall
```

### Windows 11 e Android

Seguir os READMEs em `core/` (passos manuais).

## Solucao de problemas

| Sintoma | Acao |
|---|---|
| Script nao acha a raiz | Executar a partir de qualquer subpasta localizavel sob `game-console`; se falhar, conferir o nome da pasta raiz |
| Flatpak falha | Conferir rede, Flathub e permissao do usuario |
| apt pede senha | Usar conta com sudo; o script nao contorna autenticacao |
| Host nao e Ubuntu 26 | Validar pacotes equivalentes e registrar desvio em `reports/` |
