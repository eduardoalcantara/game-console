# Diretrizes de Inicialização e Estruturação do Repositório (Setup de Emulação e Jogos)

Inicie um novo repositório Git no diretório atual. Crie a estrutura de diretórios e arquivos exatamente como especificado abaixo. Salve todos os arquivos gerados com a codificação "UTF-8 sem BOM" e não utilize emojis em nomes de arquivos ou dentro de scripts.

## 1. Estrutura de Diretórios
Crie a seguinte hierarquia de pastas na ./core do projeto:
/android-poco-x3-nfc/
/android-poco-x3-nfc/docs/
/pc-modern-emulation/
/pc-modern-emulation/windows-11/
/pc-modern-emulation/windows-11/docs/
/pc-modern-emulation/linux-ubuntu-26/
/pc-modern-emulation/linux-ubuntu-26/scripts/

---

## 2. Projeto 1: Android PocoFone X3 NFC (Jogos Legados)

Crie o arquivo `/android-poco-x3-nfc/README.md` e insira as seguintes instruções de configuração:

### Escopo do Hardware
O Poco X3 NFC utiliza o chipset Snapdragon 732G. Limite a configuração a sistemas de 8-bit até PlayStation 1, Nintendo 64 e PSP. Não tente configurar emuladores de Switch ou PS2 neste dispositivo.

### Softwares e Emuladores (Download e Configuração)
1. Instale o Frontend **Daijishō** (Disponível na Google Play Store).
2. Baixe o **RetroArch (AArch64)** via site oficial (build noturna) ou Play Store.
   - Configure os seguintes Cores (Núcleos): `Snes9x` (SNES), `Genesis Plus GX` (Mega Drive), `Mupen64Plus-Next` (N64).
   - Defina a API de vídeo para `Vulkan` em `Configurações > Vídeo`.
3. Instale o **DuckStation** (Play Store) para PS1.
   - Configure a resolução interna para 2x (720p).
   - Defina o renderizador da GPU para `Vulkan`.
4. Instale o **PPSSPP** (Play Store) para PSP.
   - Configure o pulo de quadros (Frameskip) para 0 e ative o buffer de gráficos.

### Integração
No Daijishō, aponte os caminhos das pastas de ROMs e selecione os emuladores instalados acima como os "Players" padrão para cada plataforma. Sincronize a biblioteca para baixar as artes automaticamente.

---

## 3. Projeto 2: PC (Emulação Moderna e PC Games)

### 3.1. Subdivisão Windows 11

Crie o arquivo `/pc-modern-emulation/windows-11/README.md` e documente as seguintes diretrizes:

#### Drivers e Dependências Iniciais
1. Baixe o **Intel Arc Graphics Windows DCH Driver** no site oficial da Intel. Realize a instalação limpa para garantir suporte atualizado à API Vulkan 1.3.
2. Instale o pacote **Visual C++ Redistributable (All-in-One)** e o **DirectX End-User Runtimes**.

#### Emuladores (Download e Configuração)
1. Baixe o **Ryujinx** (binário portátil do site oficial).
   - Extraia em `C:\Emuladores\Ryujinx`.
   - Adicione o arquivo `prod.keys` mais recente na pasta `System` (acessível via File > Open Ryujinx Folder).
   - Instale o Firmware original correspondente às chaves.
   - Em `Options > Settings > Graphics`, defina o Backend como `Vulkan` e a placa de vídeo primária como a Intel Arc. Resolução: 2x (1440p).
2. Baixe o **ES-DE (EmulationStation Desktop Edition)**.
   - Configure o arquivo `es_systems.xml` para apontar para o executável do Ryujinx.

#### Configuração do Jogo "Blur" (PC Abandonware)
1. Adquira a imagem ISO original do Blur (PC).
2. Instale o jogo em `C:\Games\Blur`.
3. Baixe o patch da comunidade **"Blur Project"** (ou amentes mods multiplayer disponíveis no PCGamingWiki) para restaurar a funcionalidade de rede local/online e suporte nativo a resoluções ultrawide e controles modernos.
4. Substitua o executável original pelo executável do patch na pasta raiz do jogo.
5. Adicione o atalho do Blur manualmente no ES-DE ou no Steam como "Jogo Não-Steam" para aproveitar o Steam Input para gerenciar os controles.

---

### 3.2. Subdivisão Linux (Ubuntu 26 / Kubuntu 26)

Crie o arquivo `/pc-modern-emulation/linux-ubuntu-26/README.md` documentando que o ambiente utilizará Flatpaks para isolamento e facilidade de atualização dos emuladores, e Lutris/Proton para os jogos de PC. O suporte à GPU Intel Arc é nativo no kernel.

Crie o script Bash `/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh` contendo exatamente o código abaixo. Este script atuará como automatizador do ambiente:

```bash
#!/bin/bash
# setup_linux_emulation.sh
# Finalidade: Configurar dependências de emulação e jogos de PC no Ubuntu/Kubuntu 26

set -e

echo "Iniciando a configuração do ambiente de emulação (Linux 2026)..."

# 1. Atualizar repositórios e instalar drivers essenciais (Mesa Vulkan para Intel)
sudo apt update && sudo apt upgrade -y
sudo apt install -y mesa-vulkan-drivers vulkan-tools libvulkan1 lutris steam-devices

# 2. Configurar Flatpak e repositório Flathub
sudo apt install -y flatpak
sudo flatpak remote-add --if-not-exists flathub [https://flathub.org/repo/flathub.flatpakrepo](https://flathub.org/repo/flathub.flatpakrepo)

# 3. Instalar Emuladores e Frontends via Flatpak
echo "Instalando Ryujinx, RetroArch e ES-DE..."
flatpak install -y flathub org.ryujinx.Ryujinx
flatpak install -y flathub org.libretro.RetroArch
flatpak install -y flathub org.es_de.frontend

# 4. Configurar estrutura de diretórios para ROMs e Jogos
mkdir -p ~/Games/ROMs/{switch,ps1,snes,n64}
mkdir -p ~/Games/PC/Blur

echo "Configuração base concluída."
echo "Para o jogo Blur:"
echo "1. Abra o Lutris."
echo "2. Clique no ícone '+' e selecione 'Add locally installed game'."
echo "3. Defina o 'Runner' como 'Wine' e aponte para o executável modificado do Blur na pasta ~/Games/PC/Blur."
echo "4. Em 'Runner options', ative o DXVK e o VKD3D para traduzir DirectX para Vulkan."
