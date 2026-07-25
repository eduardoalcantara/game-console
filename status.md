# status.md

## Data da ultima atualizacao

2026-07-25

## Resumo do estado atual

Pacote documental Android (passo 1) concluido. Biblioteca de ROMs dividida em `resources/roms/android/` e `resources/roms/pc-only/`. Temas oficiais ES-DE (grupo GitLab) passam a ser versionados em `resources/es-de/themes/` (~530 MB; sem `.git` aninhado). BIOS PS1 `SCPH1001.BIN` arquivada localmente (fora do Git). Instalacao real no celular/tablet ainda nao realizada.

## Tarefas concluidas

- Bootstrap Git e governanca da raiz.
- Script Linux de emulacao com `--uninstall`.
- Documentacao Android passo 1:
  - hub `core/android-poco-x3-nfc/README.md`
  - `docs/resources-inventory.md`, `rom-layout.md`, `setup-adb.md`, `setup-play-store.md`, `checklist.md`
  - `resources/android/` (contrato + pastas apk/bios)
  - `tools-android.md`
  - `.gitignore` com extensoes de APK
  - `setup.md` atualizado (secao Android)
- Espelho local da biblioteca de ROMs em `resources/roms/{android,pc-only}/` com nomes canonicos ES-DE.
- Script `scripts/tooling/dedupe_roms.py` (dry-run padrao) para deduplicar por regiao/revisao.
- Espelho local dos 11 repos do grupo [es-de/themes](https://gitlab.com/es-de/themes) em `resources/es-de/themes/` (shallow clone; gitignore).

## Tarefas pendentes

- Operador: DuckStation (ES-DE, RetroArch e BIOS PS1 ja arquivados; BIOS fora do Git).
- Executar `setup-adb.md` no Poco X3 NFC e validar checklist (celular).
- Repetir no tablet (modelo ainda nao registrado).
- Executar e validar setup Linux em host Ubuntu/Kubuntu 26.
- Aplicar guia Windows 11 no host.

## Riscos

- ES-DE Android e pago e nao redistribuivel; o APK esta local e coberto por `.gitignore` (nunca commitar).
- Package ids do ES-DE podem variar por canal (Patreon vs Galaxy Store).
- DuckStation Android sem suporte ativo; regressoes futuras de OS sao risco.
- Set MAME da biblioteca pode ser pesado/incompativel com o core escolhido no aparelho.
- Assinatura Play Store vs APK oficial do RetroArch exige desinstalacao previa.
- Pastas `atari2600`, `atarilynx`, `wonderswan` e `psx` estao vazias na biblioteca: sem ROMs de PS1, o DuckStation nao tem o que rodar.
- O espelho `resources/roms/` duplica ~2,6 GB dentro do Google Drive; se o espaco sincronizado for critico, remover a pasta apos enviar aos aparelhos.

## Proximos passos

1. Definir DuckStation (Play Store ou APK proprio).
2. Instalar ES-DE + RetroArch no celular via ADB; enviar BIOS `SCPH1001.BIN`; preencher a checklist.
3. Apos aceite no celular, repetir no tablet.

## Mudancas recentes

- Temas ES-DE: removidos `.git` aninhados; conteudo passa a ser versionado no repo (~530 MB).
- BIOS PS1 `SCPH1001.BIN` registrada no inventario (SHA-256; arquivo local, nao commitado).
- Documentado layout paisagem RetroArch (GUI + ADB pull/push do cfg) em `setup-adb.md` secao 8; pasta `resources/android/config/`.
- ES-DE Android `3.4.1-58` arquivado com SHA-256 e URL de redownload (`packages.es-de.org/.../b829bd05/...`) no inventario.
- `.gitignore` ampliado para `.7z`/`.rar`/instaladores desktop (`.AppImage`, `.exe`, …): evita commit acidental de binarios acima do limite do GitHub.
- Temas ES-DE oficiais (GitLab) clonados em `resources/es-de/themes/` (~530 MB).
- Inventario Android com colunas Manual/Automatizavel; RetroArch 1.22.2 baixado; DuckStation APK oficial 404 (fica Manual/Play Store).
- Mapa ES-DE expandido e split android/pc-only.
