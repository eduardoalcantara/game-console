#!/bin/bash
# setup_linux_emulation.sh
# Finalidade: Configurar dependencias de emulacao e jogos de PC no Ubuntu/Kubuntu 26
# Desinstalacao: bash setup_linux_emulation.sh --uninstall

set -euo pipefail

FLATPAK_APPS=(
  "org.ryujinx.Ryujinx"
  "org.libretro.RetroArch"
  "org.es_de.frontend"
)

ROM_DIRS=(
  "$HOME/Games/ROMs/switch"
  "$HOME/Games/ROMs/ps1"
  "$HOME/Games/ROMs/snes"
  "$HOME/Games/ROMs/n64"
)
PC_BLUR_DIR="$HOME/Games/PC/Blur"

prompt_yes_no() {
  # $1 = pergunta, $2 = default (0 ou 1)
  local question="$1"
  local default="${2:-0}"
  local reply
  while true; do
    echo "$question"
    echo "  0 = nao"
    echo "  1 = sim"
    if [[ "$default" == "1" ]]; then
      echo "  Enter = default (sim)"
    else
      echo "  Enter = default (nao)"
    fi
    read -r reply || true
    if [[ -z "$reply" ]]; then
      reply="$default"
    fi
    case "$reply" in
      0|1) echo "$reply"; return 0 ;;
      *) echo "Entrada invalida. Digite 0, 1 ou Enter." ;;
    esac
  done
}

find_repo_root() {
  local start="$1"
  local dir
  dir="$(cd "$start" && pwd)"
  while true; do
    if [[ "$(basename "$dir")" == "game-console" ]]; then
      printf '%s\n' "$dir"
      return 0
    fi
    if [[ "$dir" == "/" ]]; then
      return 1
    fi
    dir="$(dirname "$dir")"
  done
}

print_header() {
  echo "game-console"
  echo "Script: setup_linux_emulation"
  echo "Funcao: Configurar emulacao e jogos PC no Ubuntu/Kubuntu 26"
  echo "----------------------------------------"
}

remove_empty_dir() {
  local path="$1"
  if [[ -d "$path" ]] && [[ -z "$(ls -A "$path" 2>/dev/null || true)" ]]; then
    rmdir "$path"
    echo "Removido diretorio vazio: $path"
  elif [[ -d "$path" ]]; then
    echo "Preservado (nao vazio): $path"
  fi
}

do_uninstall() {
  echo "Modo: desinstalacao reversa."
  echo "Serao removidos apenas Flatpaks deste script e diretorios vazios criados por ele."
  echo "Nao sera revertido apt upgrade nem pacotes apt compartilhados do sistema."
  echo

  local confirm
  confirm="$(prompt_yes_no "Confirmar desinstalacao?" 0)"
  if [[ "$confirm" != "1" ]]; then
    echo "Desinstalacao cancelada."
    exit 0
  fi

  local app
  for app in "${FLATPAK_APPS[@]}"; do
    if flatpak info "$app" >/dev/null 2>&1; then
      echo "Removendo Flatpak: $app"
      flatpak uninstall -y "$app" || {
        echo "ERRO: falha ao remover $app. Abortando para falha segura."
        exit 1
      }
    else
      echo "Flatpak ausente (ok): $app"
    fi
  done

  local d
  for d in "${ROM_DIRS[@]}" "$PC_BLUR_DIR"; do
    remove_empty_dir "$d"
  done
  remove_empty_dir "$HOME/Games/ROMs"
  remove_empty_dir "$HOME/Games/PC"
  remove_empty_dir "$HOME/Games"

  echo
  echo "Acao concluida: uninstall"
  echo "Diretorio raiz detectado: $REPO_ROOT"
  echo "Areas afetadas: Flatpaks listados; diretorios ~/Games/... se vazios"
}

do_install() {
  echo "Modo: instalacao."
  echo "Serao instalados pacotes apt, Flatpak/Flathub, emuladores Flatpak e pastas ~/Games."
  echo

  local confirm
  confirm="$(prompt_yes_no "Confirmar instalacao?" 1)"
  if [[ "$confirm" != "1" ]]; then
    echo "Instalacao cancelada."
    exit 0
  fi

  echo "Iniciando a configuracao do ambiente de emulacao (Linux 2026)..."

  # 1. Atualizar repositorios e instalar drivers essenciais (Mesa Vulkan para Intel)
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y mesa-vulkan-drivers vulkan-tools libvulkan1 lutris steam-devices

  # 2. Configurar Flatpak e repositorio Flathub
  sudo apt install -y flatpak
  sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

  # 3. Instalar Emuladores e Frontends via Flatpak
  echo "Instalando Ryujinx, RetroArch e ES-DE..."
  flatpak install -y flathub org.ryujinx.Ryujinx
  flatpak install -y flathub org.libretro.RetroArch
  flatpak install -y flathub org.es_de.frontend

  # 4. Configurar estrutura de diretorios para ROMs e Jogos
  mkdir -p "$HOME/Games/ROMs/switch" \
    "$HOME/Games/ROMs/ps1" \
    "$HOME/Games/ROMs/snes" \
    "$HOME/Games/ROMs/n64"
  mkdir -p "$HOME/Games/PC/Blur"

  echo "Configuracao base concluida."
  echo "Para o jogo Blur:"
  echo "1. Abra o Lutris."
  echo "2. Clique no icone '+' e selecione 'Add locally installed game'."
  echo "3. Defina o 'Runner' como 'Wine' e aponte para o executavel modificado do Blur na pasta ~/Games/PC/Blur."
  echo "4. Em 'Runner options', ative o DXVK e o VKD3D para traduzir DirectX para Vulkan."
  echo
  echo "Acao concluida: install"
  echo "Diretorio raiz detectado: $REPO_ROOT"
  echo "Areas afetadas: apt (vulkan/lutris/flatpak), Flatpaks, ~/Games/ROMs e ~/Games/PC/Blur"
}

main() {
  clear
  print_header

  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  if ! REPO_ROOT="$(find_repo_root "$script_dir")"; then
    if ! REPO_ROOT="$(find_repo_root "$(pwd)")"; then
      echo "ERRO: nao foi possivel localizar a raiz do repositorio (pasta game-console)."
      exit 1
    fi
  fi
  export REPO_ROOT

  echo "REPO_ROOT=$REPO_ROOT"
  echo

  local mode="install"
  if [[ "${1:-}" == "--uninstall" ]]; then
    mode="uninstall"
  elif [[ -n "${1:-}" ]]; then
    echo "Uso: $0 [--uninstall]"
    exit 1
  fi

  if [[ "$mode" == "uninstall" ]]; then
    do_uninstall
  else
    do_install
  fi
}

main "$@"
