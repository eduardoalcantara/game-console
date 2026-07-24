# timeline.md

Historico em ordem cronologica decrescente.

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
