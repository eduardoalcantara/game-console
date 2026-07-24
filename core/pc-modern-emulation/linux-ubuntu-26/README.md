# PC — Linux Ubuntu/Kubuntu 26

O ambiente utiliza Flatpaks para isolamento e facilidade de atualizacao dos emuladores, e Lutris/Proton para os jogos de PC. O suporte a GPU Intel Arc e nativo no kernel.

## Script de setup

Automatizador do ambiente:

```bash
bash core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh
```

Desinstalacao reversa (apenas o que o script instalou/criou):

```bash
bash core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh --uninstall
```

O script segue `rules_scripts.md`: limpeza de tela, cabecalho game-console, descoberta de `REPO_ROOT`, confirmacoes numeradas `0`/`1` e `--uninstall`.

## O que o setup instala

- Pacotes apt: Mesa Vulkan, vulkan-tools, lutris, steam-devices, flatpak.
- Flathub (se ainda nao existir).
- Flatpaks: Ryujinx, RetroArch, ES-DE.
- Diretorios: `~/Games/ROMs/{switch,ps1,snes,n64}` e `~/Games/PC/Blur`.

## Blur via Lutris

1. Abra o Lutris.
2. Clique no icone `+` e selecione `Add locally installed game`.
3. Defina o Runner como Wine e aponte para o executavel modificado do Blur em `~/Games/PC/Blur`.
4. Em Runner options, ative o DXVK e o VKD3D para traduzir DirectX para Vulkan.

## Notas

- Nao versionar ROMs/ISOs.
- Ver `tools-linux.md` e `setup.md`.
- Fonte de dominio: `specs/spec-domain-emulation.md`.
