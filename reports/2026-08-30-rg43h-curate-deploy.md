# Relatorio — Curadoria RG43H + deploy SD 128 GB

**Data:** 2026-08-30 / 2026-08-31  
**Alvo:** RG43H PRO (EmuELEC / RGBox) — particao `EEROMS` FAT32  
**Cartao:** `H:` — 128 GB (SD novo; original 50 GB guardado noutro sitio)

---

## Resumo executivo

Pipeline concluido: manifestos YAML → staging curado → formatacao FAT32 → copia para `H:\` (rotulo **EEROMS**).

| Metrica | Valor |
|---|---|
| ROMs matched | **466** |
| Entradas missing | **291** (maioria arcade/CPS — nomes MAME vs manifesto) |
| Tamanho staging | **7,46 GB** ROMs + BIOS/media |
| Ficheiros no SD | **3375** (~7,88 GB total com BIOS) |
| FAT32 | OK — nenhum ficheiro > 4 GB |
| Filesystem SD | **FAT32**, rotulo **EEROMS**, clusters 64 KB (`fat32format -c128`) |

---

## Scripts criados

| Script | Funcao |
|---|---|
| `scripts/tooling/curate_rg43h_roms.py` | Match 16 manifestos → `resources/rg43h/staging/` + relatorio |
| `scripts/tooling/windows/deploy_rg43h_sd.ps1` | Pre-checks, FAT32 (>32 GB via `fat32format`), robocopy, validacao |

### Uso

```bash
python scripts/tooling/curate_rg43h_roms.py              # dry-run
python scripts/tooling/curate_rg43h_roms.py --execute --yes
```

```powershell
.\scripts\tooling\windows\deploy_rg43h_sd.ps1 -DriveLetter H -Yes
# Volumes >32 GB: winget install Ridgecrop.fat32format
```

---

## ROMs por pasta SD (matched)

| Pasta | ROMs |
|---|---|
| snes | 115 |
| megadrive | 62 |
| gba | 46 |
| nes | 45 |
| gb | 33 |
| gbc | 33 |
| mastersystem | 32 |
| n64 | 27 |
| pcengine | 25 |
| psx | 35 |
| psp | 5 |
| neogeo | 2 |
| msx | 2 |
| mame | 2 |
| cps1 | 1 |
| dreamcast | 1 |

**Ausentes no output:** gamegear, fbneo, cps2, cps3 — entradas arcade sem match no espelho PC (sets MAME usam nomes curtos, ex. `sf2.zip` vs `Street Fighter II`).

---

## Favoritos operador (SNES) — OK

- **Metal Warriors** → `Metal Warriors.smc`
- **Rock n' Roll Racing** → `Rock n' Roll Racing.smc`
- **Parodius** (`include_all_regions: true`) → 5 ficheiros (JP + EU)

---

## Validacao pos-deploy (`H:\`)

| Check | Resultado |
|---|---|
| Filesystem | FAT32 |
| Rotulo | EEROMS |
| `.firstDownload` | presente |
| `bios/` | 2880 ficheiros |
| `snes/` | 115 ROMs |
| `megadrive/` | 62 ROMs |
| `neogeo/` | 4 ficheiros |
| Total ficheiros | 3375 |

---

## Lacunas conhecidas (v1)

1. **SNES sem `gamelist.xml` no SD** — sd-original tinha XML (1324 entradas) mas paths nao casam com nomes No-Intro copiados; ROMs suficientes para sistema aparecer no EmuELEC. Fase 2: gerar gamelist a partir de ES-DE ou paths corrigidos.
2. **SNES sem thumbnails** — esperado v1 (sd-original sem imagens SNES).
3. **Arcade ~90% missing** — requer alias MAME no manifesto ou sets FBNeo adicionais no espelho PC.
4. **Copia Google Drive** — primeira execucao falhou com `shutil.copy2` (OSError 22); corrigido com copia chunked + retry.

---

## Proximo passo (operador)

1. Inserir SD no RG43H; confirmar **SNES** aparece no menu.
2. Smoke test: 2 jogos/sistema (prioridade SNES, MD, NES).
3. Se arcade necessario: ajustar `arcade.yaml` com nomes de set MAME/FBNeo reais.

---

## Referencias

- Plano: curadoria RG43H + deploy SD 128 GB (aprovado 2026-08-30)
- Analise SD original: `reports/2026-08-30-rg43h-sd-analysis.md`
- Manifestos: `resources/rg43h/manifests/*.yaml`
- Staging (gitignored): `resources/rg43h/staging/`
- Logs: `reports/curate_rg43h_execute.log`, `reports/deploy_rg43h_sd.log`
