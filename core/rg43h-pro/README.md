# core/rg43h-pro

Espelho local para migracao RG43H PRO (EmuELEC / RGBox).

| Pasta | Conteudo | Git |
|---|---|---|
| `sd-original/` | Metadados extraidos do SD de fabrico (gamelist.xml, images/) | ignorado |
| `manifests/` | Listas curadas por sistema (YAML) | versionado |
| `staging/` | ROMs + media filtrados prontos para SD 128 GB | ignorado |
| `docs/` | Plano de curadoria, guia do operador (saves + scrape/capas) | versionado |

Scripts:
- `scripts/tooling/extract_rg43h_metadata.py`
- `scripts/tooling/curate_rg43h_roms.py` — copia ROMs + franchise packs; **nao** altera `gamelist.xml`/media do Skraper; **nao** renomeia sets arcade
- `scripts/tooling/pull_rg43h_saves.py` — verifica/backup saves do SD → `saves-backup/`
- `scripts/tooling/apply_esde_media_rg43h.py` — capas ES-DE → staging/SD
- `scripts/tooling/fix_rg43h_staging.py` — BIOS aplanadas + correccoes PSX
- `scripts/tooling/windows/deploy_rg43h_sd.ps1` — copia staging; pull saves antes de formatar

**Pipeline:** curate → Skraper → `deploy -SkipFormat`. **Metadados:** Skraper = fonte de verdade. **Arcade:** ZIP = set MAME. Ver `docs/operator-guide.md` §1.4 e §2.6.

Guia no aparelho: [`docs/operator-guide.md`](docs/operator-guide.md).

SD fisico original (50 GB): **nao formatar** — backup de referencia. SD novo 128 GB = cartao de uso.
