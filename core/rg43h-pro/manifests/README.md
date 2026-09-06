# Manifestos de curadoria — RG43H

Listas YAML versionadas. Cada ficheiro define titulos-alvo para match contra `resources/roms/android/`.

## Campos

| Campo | Descricao |
|---|---|
| `system` | Pasta no espelho PC (`resources/roms/android/<system>/`) |
| `sd_folder` | Pasta no SD EmuELEC (EEROMS) |
| `tier` | A = 8/16-bit generoso · B = medio · C = pesado |
| `target_count` | Meta aproximada (pode exceder ligeiramente) |
| `games[].base` | Substring para match No-Intro (case-insensitive) |
| `games[].region_prefer` | Opcional; override de regiao |
| `games[].sd_folder` | Opcional; so em `arcade.yaml` (cps1/2/3, mame, fbneo) |
| `games[].note` | Notas para o operador / script de match |
| `games[].include_all_regions` | Opcional; `true` = incluir JP/EU/USA (ex.: serie Parodius) |

## Franchise packs (Mario / Sonic / Mega Man / corrida)

Ficheiro `_franchise_packs.yaml` (prefixo `_` = nao e manifesto de sistema).

`curate_rg43h_roms.py` aplica estes packs a **todos** os sistemas: copia ROMs cujo nome casa com os regex (preferencia USA via `plan_group`), alem das listas `games:` de cada YAML.

## Favoritos operador

Registados em manifestos com `note: "favorito operador"`:

- **Metal Warriors** (`snes.yaml`)
- **Rock n' Roll Racing** (`snes.yaml` + variantes EU)

## Serie Parodius

Cobertura multi-sistema — ver `docs/parodius-inventory.md`:

- SNES (5 ROMs), GB (2), NES (1), PC Engine (1), PSX (1)

## Ficheiros

| Manifesto | Tier | Meta | Entradas |
|---|---|---:|---:|
| `_franchise_packs.yaml` | — | packs | mario, sonic, megaman, racing |
| `snes.yaml` | A | 120 | 120 |
| `megadrive.yaml` | A | 80 | ~80 |
| `nes.yaml` | A | 60 | ~60 |
| `gba.yaml` | A | 50 | ~50 |
| `gb.yaml` | A | 45 | ~45 |
| `gbc.yaml` | A | 45 | ~45 |
| `pcengine.yaml` | A | 30 | ~30 |
| `mastersystem.yaml` | A | 30 | ~30 |
| `gamegear.yaml` | A | 30 | ~30 |
| `neogeo.yaml` | B | 25 | ~45 |
| `n64.yaml` | B | 25 | ~35 |
| `arcade.yaml` | B | 60 | ~60 |
| `psx.yaml` | C | 35 | ~55 |
| `psp.yaml` | C | 18 | ~35 |
| `dreamcast.yaml` | C | 10 | ~30 |

**Total aproximado:** ~800 entradas manifesto → ~550–700 jogos apos dedupe/match (depende do espelho PC).

## Uso (futuro)

```bash
python scripts/tooling/curate_rg43h_roms.py --manifest core/rg43h-pro/manifests/snes.yaml
python scripts/tooling/curate_rg43h_roms.py --all
```

Plano completo: `docs/curation-plan.md`.
