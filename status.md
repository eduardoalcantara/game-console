# status.md

## Data da ultima atualizacao

2026-07-25

## Resumo do estado atual

Pacote documental Android (passo 1) concluido. Biblioteca de ROMs dividida em `resources/roms/android/` e `resources/roms/pc-only/`. Temas oficiais ES-DE (grupo GitLab) versionados em `resources/es-de/themes/` (~530 MB). BIOS PS1 `SCPH1001.BIN` arquivada localmente (fora do Git). **Instalacao Android executada no Motorola Razr 50 Ultra** (RetroArch + DuckStation + ES-DE instalados, BIOS e ROMs enviadas e conferidas). Poco X3 NFC bloqueado pelo MIUI (Instalar via USB exige verificacao Mi/SIM). Falta configuracao na GUI (first-run ES-DE, cores, layout, smoke test).

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

- Poco X3 NFC (MIUI 14) bloqueia install via ADB sem "Instalar via USB" (conta Mi + verificacao por SIM). Aparelho primario documentado nao esta operacional para ADB no momento.
- Razr 50 Ultra (SD 8s Gen 3) e muito mais forte que o Poco: a faixa de sistemas de `rules.md` (ate PS1/N64/PSP) foi definida para o Poco; se o Razr virar alvo oficial, revisar escopo antes de expandir.
- ES-DE Android e pago e nao redistribuivel; o APK esta local e coberto por `.gitignore` (nunca commitar).
- Package ids do ES-DE podem variar por canal (Patreon vs Galaxy Store).
- DuckStation Android sem suporte ativo; regressoes futuras de OS sao risco.
- Set MAME da biblioteca pode ser pesado/incompativel com o core escolhido no aparelho.
- Assinatura Play Store vs APK oficial do RetroArch exige desinstalacao previa.
- Pastas `atari2600`, `atarilynx`, `wonderswan` e `psx` estao vazias na biblioteca: sem ROMs de PS1, o DuckStation nao tem o que rodar.
- O espelho `resources/roms/` duplica ~2,6 GB dentro do Google Drive; se o espaco sincronizado for critico, remover a pasta apos enviar aos aparelhos.

## Proximos passos

1. No Razr: first-run do ES-DE — Application data = `game-console/ES-DE`; ROMs = `game-console/ROMs`.
2. Instalar cores no RetroArch, apontar BIOS em `game-console/Games/BIOS`, calibrar layout paisagem e smoke test (checklist).
3. Quando houver dumps: executar `docs/stage-razr-50-ultra-test.md` (Mario / Zelda / Mario Kart em N64·GC·Wii).
4. Poco X3 NFC: resolver "Instalar via USB" (conta Mi + SIM) e repetir a faixa Android padrao (mesma raiz `game-console/`).

## Mudancas recentes

- Etapa extra documentada: `stage-razr-50-ultra-test.md` (Mario / Zelda / Mario Kart no Razr via N64·GC·Wii; Switch fora).
- First-run ES-DE documentado em `setup-adb.md` 7.1; pasta `/storage/emulated/0/ES-DE` criada no Razr.
- Instalacao Android realizada no Razr 50 Ultra via ADB: RetroArch, DuckStation (APKM split) e ES-DE; BIOS + ROMs (10 sistemas, 1.976 arquivos) conferidas por contagem recursiva.
- Poco X3 NFC bloqueado por restricao de install do MIUI 14 (documentado na checklist).
- Platform-tools 37.0.0 arquivado localmente (`platform-tools-latest-{windows,linux}.zip`; hashes no inventario; fora do Git).
- Temas ES-DE: removidos `.git` aninhados; conteudo passa a ser versionado no repo (~530 MB).
- BIOS PS1 `SCPH1001.BIN` registrada no inventario (SHA-256; arquivo local, nao commitado).
- Documentado layout paisagem RetroArch (GUI + ADB pull/push do cfg) em `setup-adb.md` secao 8; pasta `resources/android/config/`.
- ES-DE Android `3.4.1-58` arquivado com SHA-256 e URL de redownload (`packages.es-de.org/.../b829bd05/...`) no inventario.
- `.gitignore` ampliado para `.7z`/`.rar`/instaladores desktop (`.AppImage`, `.exe`, …): evita commit acidental de binarios acima do limite do GitHub.
- Temas ES-DE oficiais (GitLab) clonados em `resources/es-de/themes/` (~530 MB).
- Inventario Android com colunas Manual/Automatizavel; RetroArch 1.22.2 baixado; DuckStation APK oficial 404 (fica Manual/Play Store).
- Mapa ES-DE expandido e split android/pc-only.
