# tools-linux.md

Ferramentas e comandos relevantes para o alvo Linux Ubuntu/Kubuntu 26.

## Ferramentas necessarias

- `apt` (pacotes do sistema)
- `flatpak` + Flathub
- Mesa Vulkan (`mesa-vulkan-drivers`, `vulkan-tools`, `libvulkan1`)
- Lutris
- Steam Devices (`steam-devices`)
- Flatpaks: Ryujinx, RetroArch, ES-DE

## Comandos uteis

```bash
# Setup / uninstall do ambiente de emulacao
bash core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh
bash core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh --uninstall

# Verificar Vulkan
vulkaninfo | head

# Listar Flatpaks
flatpak list
```

## Dependencias do sistema

Instaladas pelo script de setup (modo install):

- `mesa-vulkan-drivers`
- `vulkan-tools`
- `libvulkan1`
- `lutris`
- `steam-devices`
- `flatpak`

Flatpaks:

- `org.ryujinx.Ryujinx`
- `org.libretro.RetroArch`
- `org.es_de.frontend`

## Uso recomendado

1. Rodar o script de setup.
2. Colocar ROMs em `~/Games/ROMs/...` (nao versionar no Git).
3. Configurar Blur via Lutris apontando para `~/Games/PC/Blur` com DXVK/VKD3D.

## Observacoes especificas de Linux

- Suporte a GPU Intel Arc e tipicamente nativo no kernel moderno.
- Preferir Flatpak para isolamento e atualizacao dos emuladores.
- O modo `--uninstall` remove Flatpaks instalados pelo script e diretorios vazios criados por ele; nao reverte `apt upgrade`.
