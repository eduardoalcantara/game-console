# Relatorio — mesclagem ROMs (2026-08-30)

## Objetivo

Mover (nao copiar) conteudo de `resources/new-roms/` e biblioteca externa para `resources/roms/`, priorizando versao USA e descartando Japan/Europe quando existir alternativa USA (exceto titulo exclusivo ou `(USA, Europe)`).

## Script

`scripts/tooling/merge_roms.py` (novo) — reutiliza regras de regiao de `dedupe_roms.py`.

## Fontes

| Fonte | Destino |
|---|---|
| `resources/new-roms/roms/` | `resources/roms/android/` ou `pc-only/` |
| `resources/new-roms/BIOS/` | `resources/roms/bios/` |
| `G:\Meu Drive\Recursos\Jogos\roms\` | mapeamento ES-DE (SMD→megadrive, etc.) |

## Resultado merge (`--execute --yes`)

| Metrica | Valor |
|---|---|
| Movidos | 60.029 |
| Descartados (JP/EU inferiores) | 26.432 |
| Substituiram existente | 19.067 |
| Placeholders ignorados | 163 |
| Erros | 0 |
| Duracao | ~62 min |

## Pos-merge (espelho local)

| Pasta | Arquivos | Tamanho |
|---|---|---|
| `resources/roms/android/` | ~40.446 | ~62,5 GB |
| `resources/roms/pc-only/` | ~675 | ~38,5 GB |
| `resources/roms/bios/` | 2.880 | ~421 MB |
| `resources/roms/switch/` | 25 | ~102 GB (inalterado + amostras) |
| `resources/new-roms/` | ~160 | ~0 (so placeholders) |

### Sistemas-chave (android)

| Sistema | ROMs |
|---|---|
| snes | 7.173 |
| gba | 2.133 |
| nes | 1.593 |
| gb | 1.321 |
| gbc | 1.179 |
| neogeo | 959 |
| megadrive | 822 |
| psx | 707 |
| psp | 503 |
| n64 | 260 |

## Dedupe pos-merge

`dedupe_roms.py --root resources/roms/android --execute --yes`:

- 1 apagado (duplicata residual)
- 5.469 renomeados (remocao de sufixo `(USA)` quando unica versao)

## Pendencias

- Pasta externa `Recursos/Jogos/roms/ROMs/` (6 arquivos) nao mapeada — verificar conteudo manualmente.
- `resources/new-roms/`: placeholders vazios podem ser removidos pelo operador.
- Smoke test PC (2 jogos/sistema) antes de copiar para SD RG43H.
- Neo Geo BIOS em `new-roms` tem CRC FBNeo correto (`sm1.sm1` = `94416D67`); validar em emulador.

## Validacao

Inventario por contagem de arquivos no PC apos execucao. Nenhum jogo foi lancado em emulador neste ciclo.
