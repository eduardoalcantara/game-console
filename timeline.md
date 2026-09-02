# timeline.md

Historico em ordem cronologica decrescente.

---

## 2026-09-02 — RG43H: Correção de BIOS, NeoGeo, PSX e Rock N Roll Racing

**Evento:** Diagnóstico e correção de falhas de execução no RG43H Pro:
1. **Neo Geo:** `neogeo.zip` FBNeo completo (1.95MB, 38 chips de ROM e Uni-BIOS 4.0) sincronizado para `bios/` e `neogeo/` (antes havia uma versão antiga de 1.48MB com 26 chips sem a Uni-BIOS 4.0 exigida pelo core).
2. **BIOS aplanadas:** arquivos de BIOS essenciais (PS1 `scph1001.bin`, `scph5500.bin`, `scph5501.bin`, `scph7001.bin`, etc.) foram copiados diretamente para a raiz de `bios/`, permitindo que os cores do RetroArch/EmuELEC encontrem os arquivos sem falhar por subpastas.
3. **PSX:** arquivos 7z compactados que estavam com extensão `.zip` (Tekken 3, Metal Gear Solid, Gran Turismo) foram descompactados em `.bin`/`.cue` nativos e foi gerado o arquivo `Crash Bandicoot.cue` para o `.bin` raw.
4. **SNES:** removidas as variantes europeias com defeito de Rock N Roll Racing (`Rock 'N' Roll Racing (Europe).zip` e `Rock & Roll Racing (Europe) (Beta).zip`), mantendo apenas a ROM USA limpa (`Rock n' Roll Racing.smc`).
5. **Redeploy SD:** `deploy_rg43h_sd.ps1 -SkipFormat -Yes` executado com sucesso para o cartão `H:`, totalizando 8.602 ficheiros (15.01 GB).

**Arquivos afetados:** `resources/rg43h/manifests/snes.yaml`, `scripts/tooling/curate_rg43h_roms.py`, `scripts/tooling/fix_rg43h_staging.py`, `resources/rg43h/staging/`, SD `H:\`, `status.md`, `timeline.md`.

---

## 2026-09-01 — Deploy Staging RG43H para SD 128 GB (H:)

**Evento:** Envio completo do staging atualizado (ROMs, BIOS, gamelist.xml, imagens e videos) para o cartao SD 128 GB (`H:`).

**Resultado:** `deploy_rg43h_sd.ps1 -SkipFormat -Yes` executado com sucesso. Sincronizados 6.887 ficheiros (14.06 GB). Validacao confirmou presenca de `bios/` (2.893), `snes/` (902), `megadrive/` (538), `neogeo/` (347), favoritos SNES e flag `.firstDownload`.

**Arquivos afetados:** SD `H:\*`, `status.md`, `timeline.md`.

---

## 2026-08-31 — Skraper → staging RG43H

**Evento:** Operador executou Skraper apontando para `resources/rg43h/staging/`.

**Resultado:** `gamelist.xml` + `images/` (e `videos/` em Neo Geo/PSX) actualizados no staging. Cobertura estimada ~**172/458** ROMs com capa (Neo Geo 43/45; NES 44/45; SNES continua 14/115). Deploy SD pendente.

**Arquivos afetados:** `resources/rg43h/staging/**/gamelist.xml`, `images/`, `videos/`, `status.md`, `timeline.md`.

---

## 2026-08-31 — Capas ES-DE → staging RG43H

**Evento:** Implementar copia de capas do ES-DE PC para layout EmuELEC (RGBox sem scraper).

**Resultado:** Script `apply_esde_media_rg43h.py` (dry-run/execute/uninstall/deploy). Staging: 126/458 ROMs com capa; NES quase completo (44/45); SNES 14/115 por sincronizacao parcial do Google Drive (pastas A–E). H: nao montado — deploy SD pendente. Relatorio `reports/2026-08-31-rg43h-esde-media.md`.

**Arquivos afetados:** `scripts/tooling/apply_esde_media_rg43h.py`, `resources/rg43h/staging/**/images/`, `gamelist.xml`, `media-report.*`, docs RG43H, `status.md`, `timeline.md`.

---

## 2026-08-31 — RG43H: SNES OK + guia saves/scrape

**Evento:** Operador confirmou SNES no RG43H Pro; documentar saves e scrape de capas no launcher.

**Resultado:** Criado `resources/rg43h/docs/operator-guide.md` (SRAM vs savestate SELECT+R1/L1; scrape EmulationStation via ScreenScraper + Update Game Lists). README e plano de curadoria actualizados.

**Arquivos afetados:** `resources/rg43h/docs/operator-guide.md`, `resources/rg43h/README.md`, `resources/rg43h/docs/curation-plan.md`, `status.md`, `timeline.md`.

---

## 2026-08-31 — RG43H curadoria v2 (rom_set Neo Geo / arcade)

**Evento:** Corrigir match MAME/FBNeo via campo `rom_set` nos manifestos; re-curadoria e redeploy SD.

**Resultado:** `curate_rg43h_roms.py` passa a priorizar `rom_set` (stem exacto do zip). `neogeo.yaml` 45/45 matched; `arcade.yaml` 20/70 (sets CPS2/CPS3/classics ausentes no espelho). Total **526** jogos matched (+60 vs v1). Redeploy `H:` FAT32 EEROMS sem reformatar (`-SkipFormat`), 3447 ficheiros (~8,9 GB). Neo Geo no SD: 45 ROMs + BIOS.

**Arquivos afetados:** `scripts/tooling/curate_rg43h_roms.py`, `resources/rg43h/manifests/neogeo.yaml`, `resources/rg43h/manifests/arcade.yaml`, staging, SD `H:\`, `status.md`, `timeline.md`.

---

## 2026-08-31 — Curadoria RG43H + deploy SD 128 GB

**Evento:** Gerar staging EmuELEC a partir de 16 manifestos YAML e copiar para cartao novo 128 GB.

**Resultado:** `curate_rg43h_roms.py` executado (`--execute --yes`): 466 matched, 291 missing, ~7,46 GB ROMs. Staging em `resources/rg43h/staging/` (gitignored). `deploy_rg43h_sd.ps1`: formatacao FAT32 via `fat32format -c128` (Windows nao suporta FAT32 nativo >32 GB), rotulo EEROMS, robocopy 3375 ficheiros para `H:\`. Favoritos SNES OK (Metal Warriors, Rock n' Roll Racing, Parodius). Arcade largely missing (nomes MAME). SNES sem gamelist.xml filtrado (paths sd-original incompativeis — ROMs presentes).

**Arquivos afetados:** `scripts/tooling/curate_rg43h_roms.py`, `scripts/tooling/windows/deploy_rg43h_sd.ps1`, `resources/rg43h/staging/`, SD `H:\`; `reports/2026-08-30-rg43h-curate-deploy.md`, `status.md`, `timeline.md`, `resources/rg43h/docs/curation-plan.md`.

---

## 2026-08-30 — Mesclagem biblioteca ROMs (new-roms + externa)

**Evento:** Mover ROMs de `resources/new-roms/` e `G:\Meu Drive\Recursos\Jogos\roms\` para espelho `resources/roms/` com prioridade USA.

**Resultado:** Script `scripts/tooling/merge_roms.py` criado e executado (~62 min). 60.029 movidos; 26.432 descartados (JP/EU inferiores); 19.067 substituicoes. Espelho final: ~40,4k ROMs em `android/` (~62,5 GB), ~675 em `pc-only/`, BIOS em `resources/roms/bios/`. Dedupe pos-merge: 1 apagado, 5.469 renomeados (remocao `(USA)`). `new-roms` esvaziado (so placeholders). Biblioteca externa esvaziada exceto pasta `ROMs/` (6 arquivos, nao mapeada).

**Arquivos afetados:** `resources/roms/**`, `resources/new-roms/**`, biblioteca externa; `scripts/tooling/merge_roms.py`, `reports/2026-08-30-merge-roms.md`, `status.md`, `timeline.md`.

---

## 2026-08-04 — Limpeza Razr: so Mega Drive + SNES

**Evento:** Remover do celular ROMs e media ES-DE de todos os sistemas exceto `megadrive` e `snes`.

**Resultado:** `ROMs/` no Razr = megadrive + snes (~2 GB). `downloaded_media/` e `gamelists/` no aparelho idem (~3,1 GB media). Repo PC intacto. Keys/firmware Eden em `game-console/switch/` preservados. Operador reportou tela preta em Neo Geo e MAME antes da remocao — documentado (CRC FBNeo ja conhecido; MAME sem fix neste ciclo). Push Neon Apex adiado.

**Arquivos afetados:** aparelho; `status.md`, `timeline.md`, `checklist.md`.

---

## 2026-08-04 — Pull capas/metadados ES-DE do Razr

**Evento:** Espelhar scrape do ES-DE no repo local.

**Resultado:** `adb pull` de `downloaded_media/` (12.821 arquivos, ~10,8 GB; sistemas: gb, gba, gbc, mame, mastersystem, megadrive, nes, pcengine, snes, switch) e `gamelists/` (11 XMLs) para `resources/es-de/`. Pastas adicionadas ao `.gitignore`. README em `resources/es-de/README.md`.

**Arquivos afetados:** `resources/es-de/downloaded_media/`, `resources/es-de/gamelists/` (fora do Git), `.gitignore`, `resources/es-de/README.md`, `status.md`, `timeline.md`.

---

## 2026-07-27 — Pendente: Neon Apex Beyond the Limit (Switch)

**Evento:** Novos dumps locais renomeados e enfileirados para push ADB.

**Resultado:** Base `resources/roms/switch/Neon Apex Beyond the Limit.xci` (~1,86 GB) e update `resources/roms/switch/updates/Neon Apex Beyond the Limit.nsp` (~246 MB). Razr desconectado — push para `game-console/ROMs/switch[/updates]/` registrado em `status.md` como pendente.

**Arquivos afetados:** `resources/roms/switch/**` (fora do Git), `status.md`, `timeline.md`.

---

## 2026-07-26 — Temas ES-DE enviados ao Razr

**Evento:** Push de `resources/es-de/themes/` (~530 MB) para `/storage/emulated/0/game-console/ES-DE/themes/`.

**Resultado:** Temas oficiais (modern, slate, carousel-icons, system-*, etc.) disponiveis no aparelho para selecionar no ES-DE. Capas de jogos (`downloaded_media`) continuam a depender de scrape ScreenScraper (conta do operador).

**Arquivos afetados:** aparelho; `timeline.md`.

---

## 2026-07-26 — Push biblioteca Switch completa no Razr

**Evento:** Renomear NSMBU Deluxe; conferir device (so Odyssey); push de bases pendentes + pasta `updates/`.

**Resultado:** 12 bases (~81 GB novos + Odyssey) e 4 updates (~17 GB) em `game-console/ROMs/switch[/updates]/`. Totais no aparelho: ~98 GB na pasta switch (inclui updates).

**Arquivos afetados:** aparelho (fora do Git); `timeline.md`, `status.md`.

---

## 2026-07-26 — Tutorial Eden: instalar update NSP

**Evento:** Documentar o fluxo de update (base em `ROMs/switch/`, UPD em `updates/`, Install to NAND no Eden).

**Resultado:** Novo `docs/eden-install-updates.md`; links no hub Android e em `rom-layout.md`.

**Arquivos afetados:** `eden-install-updates.md`, `README.md` (hub), `rom-layout.md`, `timeline.md`.

---

## 2026-07-26 — Remocao dos NCA soltos em resources/switch

**Evento:** Apos existir `firmware.zip`, apagar as 238 copias soltas `.nca` / `.cnmt.nca` em `resources/switch/`.

**Resultado:** Pasta local ficou com `firmware.zip`, `prod.keys` e `title.keys`. Git ainda marca as 238 exclusoes como unstaged (firmware fora indevidamente no historico — commit de remocao pendente se o operador pedir).

**Arquivos afetados:** `resources/switch/*.nca` (disco); status Git working tree.

---

## 2026-07-26 — Switch updates/ + diagnostico Neo Geo FBNeo

**Evento:** Reorganizacao dos dumps Switch e analise do erro FBNeo no Metal Slug.

**Resultado:** Criada `resources/roms/switch/updates/` (README local). Bases renomeadas sem Title ID; 3 UPD movidos (DOOM, Mario Kart 8 Deluxe, Wolfenstein II). Convencao documentada em `rom-layout.md`. Razr desconectado — push ADB pendente. `neogeo.zip` local tem `sm1.sm1` / `sfix.sfx` / `000-lo.lo`, mas CRCs diferem do exigido pelo FBNeo (ex.: sm1 `0x97cf998b` vs `0x94416d67`); precisa dump proprio compativel.

**Arquivos afetados:** `resources/roms/switch/**` (fora do Git), `rom-layout.md`, `resources-inventory.md`, `status.md`, `timeline.md`.

---

## 2026-07-25 — Smoke test Eden / Switch no Razr 50 Ultra

**Evento:** Instalacao e configuracao do Eden Android v0.2.1-standard no Razr (`ZY22JXF44B`) com keys, firmware e Super Mario Odyssey.

**Resultado:** Eden instalado (`dev.eden.eden_emulator`). Keys em `game-console/switch/keys/` e espelho na pasta do app. Firmware enviado como `game-console/switch/firmware/firmware.zip` (238 NCAs; Install Firmware via seletor de arquivo — pasta solta nao funciona). NSP Odyssey em `game-console/ROMs/switch/`. Operador confirmou instalacao de firmware OK. ES-DE 3.4.1-58 ja inclui sistema `switch` com player padrao Eden (Standalone). Proximo: dumps adicionais do operador.

**Arquivos afetados:** aparelho (fora do Git); `resources/switch/firmware.zip` local (gitignore); `status.md`, `timeline.md`.

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
