# resources/rg43h

Espelho local para migracao RG43H PRO (EmuELEC / RGBox).

| Pasta | Conteudo | Git |
|---|---|---|
| `sd-original/` | Metadados extraidos do SD de fabrico (gamelist.xml, images/) | ignorado |
| `manifests/` | Listas curadas por sistema (YAML) | versionado |
| `staging/` | ROMs + media filtrados prontos para SD 128 GB | ignorado |
| `docs/` | Plano de curadoria, guia do operador (saves + scrape/capas) | versionado |

Scripts:
- `scripts/tooling/extract_rg43h_metadata.py`
- `scripts/tooling/curate_rg43h_roms.py`
- `scripts/tooling/apply_esde_media_rg43h.py` — capas ES-DE → staging/SD
- `scripts/tooling/windows/deploy_rg43h_sd.ps1`

Guia no aparelho: [`docs/operator-guide.md`](docs/operator-guide.md).

SD fisico original (50 GB): **nao formatar** — backup de referencia. SD novo 128 GB = cartao de uso.
