# timeline.md

Historico em ordem cronologica decrescente.

---

## 2026-07-25 — Raiz unica `game-console/` no aparelho

**Evento:** Reorganizacao no Razr: `ES-DE`, `ROMs` e `Games` movidos para `/storage/emulated/0/game-console/`.

**Resultado:** Conteudo preservado (ex.: snes = 790 arquivos). Docs (`setup-adb.md`, `rom-layout.md`, etapa Razr, checklist, tools) atualizados para a nova raiz.

**Arquivos afetados:** `setup-adb.md`, `rom-layout.md`, `stage-razr-50-ultra-test.md`, `checklist.md`, `tools-android.md`, `status.md`, `timeline.md`.

---

## 2026-07-25 — Etapa Razr (Mario/Zelda/MK) + first-run ES-DE

**Evento:** Documentacao da bancada temporaria no Razr 50 Ultra e esclarecimento das pastas do ES-DE.

**Resultado:** Novo `stage-razr-50-ultra-test.md` (N64/GC/Wii para Mario, Zelda e Mario Kart; Switch fora por legalidade/desempenho). Secao 7.1 em `setup-adb.md`. Pasta `/storage/emulated/0/ES-DE` criada no Razr via ADB (Application data); ROMs ja em `/storage/emulated/0/ROMs`.

**Arquivos afetados:** `stage-razr-50-ultra-test.md`, `setup-adb.md`, `README.md` (hub Android), `status.md`, `timeline.md`.

---

## 2026-07-25 — Instalacao Android no Razr 50 Ultra (Poco bloqueado)

**Evento:** Execucao real do `setup-adb.md`. Poco X3 NFC reconhecido por ADB, mas MIUI 14 barrou os installs (RetroArch `VERIFICATION_FAILURE`; ES-DE `USER_RESTRICTED`; "Instalar via USB" exige conta Mi + verificacao por SIM). Migrado para Motorola Razr 50 Ultra (`ZY22JXF44B`, Android 16, arm64-v8a).

**Resultado (Razr):** RetroArch (`com.retroarch.aarch64`), ES-DE (`org.es_de.frontend`) e DuckStation (`com.github.stenzek.duckstation`) instalados. DuckStation vinha como bundle **APKM** (APKMirror) — extraido `base.apk` + `split_config.arm64_v8a.apk` e instalado via `adb install-multiple`. BIOS `SCPH1001.BIN` e ROMs de 10 sistemas enviadas; contagem recursiva local == device (1.976 arquivos). Config na GUI ainda pendente.

**Arquivos afetados:** `checklist.md`, `status.md`, `timeline.md` (aparelho e binarios fora do Git).

---

## 2026-07-25 — Platform-tools local (Windows + Linux)

**Evento:** Operador colocou `platform-tools-latest-windows.zip` e `platform-tools-latest-linux.zip` em `resources/android/`.

**Resultado:** Ambos `Pkg.Revision=37.0.0`. Hashes registrados no inventario; ZIPs fora do Git (`*.zip`). Instrucoes de extracao/PATH em `tools-android.md`.

**Arquivos afetados:** `resources-inventory.md`, `tools-android.md`, `resources/android/README.md`, `checklist.md`, `status.md`, `timeline.md` (ZIPs locais nao versionados).

---

## 2026-07-25 — Temas ES-DE versionados + BIOS PS1 local

**Evento:** Operador pediu versionar `resources/es-de/themes/` no remoto e registrou BIOS PS1.

**Resultado:** Removidos os 11 diretorios `.git` aninhados; regra de ignore dos temas retirada do `.gitignore`. BIOS `resources/android/bios/SCPH1001.BIN` (512 KB, SHA-256 `71AF94D1...`) registrada no inventario e **nao** commitada (`*.bin` continua ignorado).

**Arquivos afetados:** `resources/es-de/themes/**`, `.gitignore`, `resources/es-de/themes/README.md`, `resources-inventory.md`, `checklist.md`, `status.md`, `timeline.md`.

---

## 2026-07-25 — RetroArch layout paisagem (GUI + ADB)

**Evento:** Documentacao do layout jogo-no-centro / overlays laterais no Android.

**Resultado:** Em `setup-adb.md`, secao 8: calibracao obrigatoria na GUI; ADB apenas para `pull`/`push` do `retroarch.cfg` (e overrides). Checklist e `resources/android/config/` atualizados. Sem validacao em aparelho nesta entrega (so documentacao).

**Arquivos afetados:** `setup-adb.md`, `checklist.md`, `core/android-poco-x3-nfc/README.md`, `resources/android/README.md`, `resources/android/config/README.md`, `resources/android/config/poco-x3-nfc/.gitkeep`, `status.md`, `timeline.md`.

---

## 2026-07-24 — ES-DE Android arquivado pelo operador

**Evento:** Operador colocou `ES-DE_3.4.1-58.apk` (~79 MB) em `resources/android/apk/`.

**Resultado:** SHA-256 `4B8C06F1CF505945EDD77F9B8FA523E8F580A13EAEF1A02F0092390F3739B387` registrado no inventario; nome original do canal oficial preservado; `setup-adb.md` passa a citar o arquivo real. Versao lida do nome do arquivo (nao conferida via `aapt`). URL de redownload anotada: `https://packages.es-de.org/android/b829bd05/ES-DE_3.4.1-58.apk` (path com token; builds futuras mudam o segmento).

**Correcao associada:** `.gitignore` nao cobria `.7z`; `retroarch-aarch64-1.22.2.7z` (152 MB) e `ES-DE_3.4.1-58.7z` (33 MB) apareciam como untracked e quebrariam o push (limite de 100 MB). Adicionados `*.7z`, `*.rar`, `*.gz`, `*.bz2`, `*.xz`, `*.zst` e instaladores desktop (`*.AppImage`, `*.exe`, `*.msi`, `*.dmg`, `*.deb`, `*.rpm`).

**Arquivos afetados:** `resources-inventory.md`, `setup-adb.md`, `resources/android/README.md`, `.gitignore`, `status.md`, `timeline.md`.

---

## 2026-07-24 — Espelho local temas ES-DE (GitLab)

**Evento:** Shallow clone dos 11 projetos do grupo [es-de/themes](https://gitlab.com/es-de/themes) para `resources/es-de/themes/`.

**Resultado:** Modern, Slate, themes-list, packs de assets e exemplos (~530 MB). Conteudo em `.gitignore`; so `README.md` versionavel. Temas de terceiros da lista curada (maioria no GitHub) nao clonados.

**Arquivos afetados:** `resources/es-de/themes/**` (local), `resources/es-de/themes/README.md`, `.gitignore`, `status.md`, `timeline.md`.

---

## 2026-07-24 — Inventario APKs (manual vs automatizavel)

**Evento:** Reescrita de `resources-inventory.md`; download de RetroArch AArch64 1.22.2.

**Resultado:**

- RetroArch em `resources/android/apk/retroarch-aarch64-1.22.2.apk` (SHA-256 `7BD5D208DFE93CC8E2EA6C04608948CE1A045980F160A58CA2D0993AA20AD213`).
- DuckStation: URLs oficiais de APK retornam 404; reclassificado como Manual (Play Store) ate haver APK publico de novo.
- ES-DE e BIOS continuam Manual (operador).

**Arquivos afetados:** `resources-inventory.md`, `resources/android/README.md`, `setup-adb.md`, `resources/android/apk/retroarch-aarch64-1.22.2.apk` (local), `status.md`, `timeline.md`.

---

## 2026-07-24 — Expandir mapa de sistemas ES-DE

**Evento:** Criacao de pastas canônicas ausentes e documentacao do mapa Android vs PC-only.

**Android (novas vazias):** n64, psp, nds, dreamcast, saturn, gamegear, sg-1000, sega32x, segacd, virtualboy, ngp, ngpc, wonderswancolor, fds, neogeocd, atari7800, atari5200, colecovision, intellivision, msx, msx2, amiga, c64, scummvm.

**PC-only (novas vazias):** gc, wiiu, ps3, xbox, xbox360 (alem de dos/wii/ps2/switch).

**Arquivos afetados:** `resources/roms/**` (local), `rom-layout.md`, `roms-structure.md`, `status.md`, `timeline.md`.

**Fontes:** ES-DE ANDROID.md (Supported game systems); desempenho 732G (N64/PSP/Dreamcast/Saturn confortaveis; GC/Wii/PS2/Switch fora da faixa Android deste repo).

---

## 2026-07-24 — Split resources/roms (android vs pc-only)

**Evento:** Reorganizacao da biblioteca local em duas faixas.

**Impacto:** `adb push` e dedupe passam a usar so `resources/roms/android/`. Consoles modernos e DOS ficam em `resources/roms/pc-only/` (wii, ps2, switch vazios; `dos` = antiga pasta `pc`).

**Arquivos afetados:**

- `resources/roms/android/`, `resources/roms/pc-only/` (conteudo local)
- `resources/roms-structure.md`
- `core/android-poco-x3-nfc/docs/rom-layout.md`
- `core/android-poco-x3-nfc/docs/setup-adb.md`
- `core/android-poco-x3-nfc/docs/checklist.md`
- `resources/android/README.md`
- `scripts/tooling/dedupe_roms.py`, `scripts/tooling/README.md`
- `status.md`, `timeline.md`

---

## 2026-07-24 — Execucao dedupe_roms (producao)

**Evento:** Aplicacao real de `scripts/tooling/dedupe_roms.py --execute --yes` em `resources/roms/`.

**Impacto:** Biblioteca deduplicada e com sufixo ` (USA)` removido nas unicas versoes restantes.

**Resultado:** Apagados 40 | Renomeados 1919 | Erros 0. Segundo dry-run: 0 acoes pendentes. Total atual ~2824 arquivos / 2,63 GB (inclui saves/companions ignorados pelo dedupe).

**Arquivos afetados:**

- `resources/roms/` (conteudo local)
- `reports/2026-07-24-dedupe-roms-execute.md`
- `reports/_dedupe_roms_execute_raw.txt`
- `status.md`, `timeline.md`

---

## 2026-07-24 — Dry-run dedupe_roms (relatorio)

**Evento:** Execucao em dry-run de `scripts/tooling/dedupe_roms.py` sobre `resources/roms/`.

**Impacto:** Relatorio de auditoria gerado; biblioteca nao alterada.

**Resultado:** 2839 arquivos considerados; 40 delecoes e 1919 renomeacoes (strip ` (USA)`) planejadas; 0 protegidos; 0 alteracoes aplicadas.

**Arquivos afetados:**

- `reports/2026-07-24-dedupe-roms-dryrun.md`
- `reports/_dedupe_roms_dryrun_raw.txt`
- `status.md`, `timeline.md`

---

## 2026-07-24 — Script dedupe_roms

**Evento:** Criacao de `scripts/tooling/dedupe_roms.py` para eliminar duplicatas No-Intro/Redump (USA > Japan > Europe, maior Rev, protecao a hacks/traducoes, strip de ` (USA)` na unica versao restante).

**Impacto:** Operador pode auditar com dry-run antes de apagar. Default aponta para `resources/roms/`.

**Arquivos afetados:**

- `scripts/tooling/dedupe_roms.py`
- `scripts/tooling/README.md`
- `status.md`, `timeline.md`

**Observacoes:** Dry-run em `resources/roms/snes` validado apos correcao que excluía `.srm` do confronto com ROMs reais.

---

## 2026-07-24 — Espelho local da biblioteca de ROMs

**Evento:** Copia da biblioteca de `G:\Meu Drive\Recursos\Jogos\roms` para `resources/roms/`, ja renomeada para o canon ES-DE.

**Impacto:** O `adb push` passa a usar caminhos curtos dentro do repositorio, sem depender do mapeamento manual de nomes. Nenhuma ROM versionada (regra `roms/` do `.gitignore` confirmada com `git check-ignore`).

**Numeros:** 2864 arquivos / 2,67 GB. Contagem por pasta conferida contra a origem, sem divergencia. `desktop.ini` e `Thumbs.db` excluidos.

**Achados:** `2600`, `LYNX`, `WSWAN` e `PS1` estao vazias na origem. A extensao `.md` em `megadrive` e ROM de Mega Drive, nao Markdown.

**Arquivos afetados:**

- `resources/roms/` (conteudo local, nao versionado)
- `core/android-poco-x3-nfc/docs/rom-layout.md`
- `core/android-poco-x3-nfc/docs/setup-adb.md`
- `core/android-poco-x3-nfc/docs/checklist.md`
- `resources/android/README.md`
- `status.md`, `timeline.md`

---

## 2026-07-24 — Android passo 1 (docs + recursos)

**Evento:** Pacote documental do ambiente Android com ADB primario, ES-DE pago e inventario da biblioteca de ROMs.

**Impacto:** Operador tem mapa claro do que baixar, onde colocar e como instalar no celular e depois no tablet. Frontend Android alinhado a ES-DE (nao Daijisho). Pasta `PC` da biblioteca ignorada neste passo.

**Arquivos afetados:**

- `core/android-poco-x3-nfc/README.md`
- `core/android-poco-x3-nfc/docs/resources-inventory.md`
- `core/android-poco-x3-nfc/docs/rom-layout.md`
- `core/android-poco-x3-nfc/docs/setup-adb.md`
- `core/android-poco-x3-nfc/docs/setup-play-store.md`
- `core/android-poco-x3-nfc/docs/checklist.md`
- `resources/android/README.md`
- `resources/android/apk/.gitkeep`
- `resources/android/bios/.gitkeep`
- `tools-android.md`
- `.gitignore`
- `setup.md`
- `status.md`
- `timeline.md`
- `reports/2026-07-24-android-docs-passo1.md`

**Observacoes:** Instalacao real nos aparelhos nao executada nesta entrega.

---

## 2026-07-24 — Bootstrap do repositorio

**Evento:** Criacao da fundacao documental e do dominio de emulacao.

**Impacto:** Repositorio passa a ter governanca Cursor operacional e guias por alvo (Android, Windows 11, Linux Ubuntu 26).

**Arquivos afetados:**

- Raiz: `.gitignore`, `readme.md`, `spec_root.md`, `flow.md`, `rules.md`, `status.md`, `timeline.md`, `setup.md`, `tools-linux.md`, `tools-windows.md`, `.cursorrules`, `spec_template.md`, `rules_scripts.md`
- `specs/`: specs de entrada movidas
- `core/android-poco-x3-nfc/README.md`
- `core/pc-modern-emulation/windows-11/README.md`
- `core/pc-modern-emulation/linux-ubuntu-26/README.md`
- `core/pc-modern-emulation/linux-ubuntu-26/scripts/setup_linux_emulation.sh`
- `reports/2026-07-24-bootstrap-entrega.md`

**Observacoes:** Script Linux adaptado a `rules_scripts.md` (nao copia literal da spec de dominio). URL do Flathub corrigida.
