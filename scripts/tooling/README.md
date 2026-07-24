# scripts/tooling

Scripts de apoio operacional (Python / multiplataforma).

## dedupe_roms.py

Elimina ROMs duplicadas (No-Intro / Redump) por prioridade de regiao e revisao.

### Regras

1. Agrupa pelo nome base (ignora tags `()` / `[]`).
2. Regiao: USA (e combinacoes com USA) > Japan > Europe.
3. Na regiao vencedora, mantem a maior revisao (`Rev N`, `v1.1`, ...).
4. Nunca apaga arquivos com tags de customizacao (`PT-BR`, `Hack`, `Mod`, `Undub`, `Translated`, `T-En`, `Tr` em forma de tag).
5. Se sobrar uma unica versao USA, remove o sufixo ` (USA)` do nome.
6. Ignora saves/companions (`.srm`, `.sav`, patches, imagens, etc.).

### Uso

Dry-run (padrao — nao apaga nada):

```bash
python scripts/tooling/dedupe_roms.py
python scripts/tooling/dedupe_roms.py --root resources/roms/android/snes
```

Aplicar de verdade (pede confirmacao `0`/`1`):

```bash
python scripts/tooling/dedupe_roms.py --execute
```

Sem prompt (ainda assim so com `--execute`):

```bash
python scripts/tooling/dedupe_roms.py --execute --yes
```

Default de `--root`: `<REPO_ROOT>/resources/roms/android` (faixa Android). A faixa `resources/roms/pc-only/` nao e o alvo deste script.

### Observacoes

- Agrupar por tags removidas faz edicoes especiais (`Competition Edition`, etc.) competirem com a ROM padrao do mesmo titulo.
- Empate de revisao: mantem o arquivo maior; se empatar de novo, o nome lexicograficamente menor.
- Stdlib apenas (sem pip).
