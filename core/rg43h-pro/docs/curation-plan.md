# Plano de curadoria — RG43H PRO

## Problema SNES no SD original

O cartao tinha `snes/gamelist.xml` (**1.324** entradas) e `sfc/gamelist.xml` (**3.371** entradas), mas **zero ficheiros ROM** e **zero imagens** em `snes/`, `snesh/`, `sfc/`. O EmuELEC **oculta sistemas sem ROMs** — daí o SNES nao aparecer.

No PC temos **7.173** ROMs SNES (~3,9 GB) pos-mesclagem. A curadoria corrige isto.

---

## Principio geral

**Nao** copiar listas genericas da web cegamente. O fluxo e:

1. **Manifesto** — lista curada de titulos canonicos por sistema (YAML versionado no repo).
2. **Match** — cruzar manifesto com `resources/roms/android/<sistema>/` (nomes No-Intro; prioridade USA ja aplicada).
3. **Staging** — copiar so ROMs matched para `core/rg43h-pro/staging/` (layout EmuELEC).
4. **Metadados** — filtrar `gamelist.xml` + `images/` do SD original; preencher lacunas (ex.: SNES) com media ES-DE ou scrape novo.

---

## Tiers por peso do sistema

| Tier | Sistemas | Criterio | Quantidade alvo |
|---|---|---|---|
| **A — favorito / 8-16-bit leve** | **SNES**, MD, NES, GB, GBC, GBA, PCE, SMS, GG | Ficheiros pequenos; SNES generoso por preferencia do operador | SNES **~120** · MD **~80** · NES **~60** · handhelds **~40–60** cada · PCE **~30** |
| **B — medio** | Neo Geo, N64, MAME, FBNeo, CPS | Jogos maiores ou sets arcade; so classics | Neo Geo **~25** · N64 **~25** · arcade **~50–80** total |
| **C — pesado** | PSX, PSP, Dreamcast | ISO/CHD grandes; melhores dos melhores | PSX **~35** · PSP **~18** · DC **~10** |

**Total estimado:** ~500–650 jogos · **~25–40 GB** (cabe folgado em 128 GB com BIOS, media e margem).

Tier A nao e "top 10" — e biblioteca rica mas curada. Tier C e onde entram listas tipo "essential/top 100" filtradas.

---

## Fontes para os manifestos

Combinacao (nao uma so):

- Listas **essential** da comunidade (RetroRGB, r/emulation, FAQ EmuELEC).
- Top 100 IGN/Eurogamer/Metacritic — **filtrados** para titulos com ROM USA/Europe no espelho PC.
- Exclusivos JP so quando nao ha USA **e** o jogo e consensual (ex.: Terranigma, Seiken Densetsu 3 fan trad).
- **Operador** pode marcar favoritos extras numa lista `operator-picks.yaml`.

Cada entrada do manifesto:

```yaml
- title: "Super Mario World"
  base: "Super Mario World"      # match parcial No-Intro
  region_prefer: ["USA", "World"]
  note: "pack-in quality"
```

---

## Metadados e thumbnails

| Fonte | Conteudo | SNES |
|---|---|---|
| SD original (`core/rg43h-pro/sd-original/`) | `gamelist.xml` + `images/` por sistema | XML sim, imagens **nao** |
| ES-DE Razr (`resources/es-de/downloaded_media/snes/`) | boxart/screenshot scrape | **1.643** ficheiros (~1,5 GB) |
| Skraper (PC, frontend Recalbox) | `gamelist.xml` + `media/` / `images/` no staging | **fonte de verdade** para `<name>` e capas em **todos** os sistemas |
| Scrape novo no RG43H | fallback | se faltar match; RGBox costuma bloquear |

Script `apply_esde_media_rg43h.py` e/ou Skraper alimentam media + `<name>` no EmuELEC.

### Metadados Skraper (todos os sistemas)

- `curate_rg43h_roms.py` **nao** sobrescreve nem reescreve `<name>` num `gamelist.xml` ja presente no staging (SNES, MD, NES, PSX, Neo Geo, …).
- Pasta `media/` / imagens do Skraper permanece intacta.
- Sem Skraper: fallback = filtrar gamelist do `sd-original/` (e, so em arcade, preencher `<name>` a partir do `base` do manifesto).

### Arcade / Neo Geo (obrigatorio — ficheiros)

- Ficheiros `.zip` = **set MAME/FBNeo** (`fatfury3.zip`, `mslug.zip`). **Nunca renomear** para o titulo comercial.
- Titulo no ecran = `<name>` no `gamelist.xml` gerado pelo **Skraper**.
- Pastas afectadas pela regra de nao renomear ZIP: `neogeo/`, `mame/`, `cps1/`, `cps2/`, `cps3/`.

Localizacao de produto: staging e docs em **`core/rg43h-pro/`** (nao em `resources/`). `resources/` fica para ROMs/BIOS brutos.

---

## Extracao SD original (sem formatar)

Copiar para `core/rg43h-pro/sd-original/`:

- `gamelist.xml` de cada pasta de sistema
- `images/` e `videos/` onde existirem
- `bezels/` (4 ficheiros)

**Nao** copiar ROMs do SD (curadoria vem do PC). SD fisico fica intacto como backup.

---

## Pipeline (scripts)

```text
1. curate_rg43h_roms.py      match + franchise packs → staging     [ROMs]
2. Skraper (Recalbox)        gamelist.xml + media no staging       [metadados]
3. pull_rg43h_saves.py       so se for formatar o SD               [opcional]
4. deploy_rg43h_sd.ps1 -SkipFormat   staging → SD                  [copia]
```

Nao reexecutar curate depois do Skraper (apaga metadados). Formatar SD so com pull de saves antes.

---

## Proximo passo imediato

1. ~~Gerar manifestos Tier A/B/C~~ (2026-08-30).
2. ~~Implementar `curate_rg43h_roms.py`~~ (2026-08-31).
3. ~~Deploy SD 128 GB FAT32 EEROMS~~ (2026-08-31).
4. ~~**Operador:** smoke test SNES no RG43H~~ (confirmado 2026-08-31 — SNES OK).
5. **Operador:** capas via `apply_esde_media_rg43h.py` (RGBox sem scraper); sincronizar ES-DE media offline no Drive se faltarem letras F–Z; smoke test outros sistemas.
6. Fase 2 restante: sets CPS2 no espelho PC se arcade for prioridade.
