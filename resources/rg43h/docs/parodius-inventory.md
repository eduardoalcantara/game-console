# Inventario Parodius — espelho PC vs RG43H

Verificacao em 2026-08-30. Objetivo: serie completa no SD 128 GB; nada deixado em `new-roms`.

## Presentes em `resources/roms/android/` (OK)

| Ficheiro | Sistema | Regiao | Manifesto |
|---|---|---|---|
| `Jikkyou Oshaberi Parodius (Japan).sfc` | SNES | JP | `snes.yaml` |
| `Gokujou Parodius (Japan).zip` | SNES | JP | `snes.yaml` |
| `Parodius Da! - Shinwa kara Owarai e (Japan).zip` | SNES | JP | `snes.yaml` |
| `Parodius (Europe).smc` | SNES | EU | `snes.yaml` |
| `Parodius Non-Sense Fantasy (E).smc` | SNES | EU | `snes.yaml` |
| `Parodius Da! - Shinwa kara Owarai e (Japan).zip` | PC Engine | JP | `pcengine.yaml` |
| `Parodius (Europe).zip` | GB | EU | `gb.yaml` |
| `Parodius Da! (Japan).zip` | GB | JP | `gb.yaml` |
| `Parodius (Europe).nes` | NES | EU | `nes.yaml` |
| `Sexy Parodius.chd` | PSX | — | `psx.yaml` |

**Total ROMs Parodius no espelho:** 10 ficheiros (~13 MB).

## Nada pendente em `new-roms`

Pesquisa recursiva: **0** ficheiros Parodius fora de `resources/roms/`. Nao e necessario mover nada de `new-roms` → `roms`.

## Ausentes no espelho (nao recuperaveis por move)

| Titulo | Plataforma tipica | Nota |
|---|---|---|
| *Parodius* (1988, original) | PC Engine / MSX | PCE: so `Parodius Da!` no espelho e no SD `H:\roms\pcengine\` |
| *Parodius Star Ocean* | Game Boy | **Nao encontrado** em PC, SD, `new-roms` nem `Recursos\Jogos` |
| *Parodius* (arcade) / *Parodius Da!* (arcade) | MAME/FBNeo | Nao encontrado; `sd-original/mame/images/parodius.png` e so metadata |
| *Parodius* (Japan) | MSX | **Recuperado do SD** `H:\roms\msx1\` → `resources/roms/android/msx/` (2026-08-30) |

Estes exigiriam **nova aquisicao/dump** se o operador quiser 100% da serie; MSX foi excecao (estava no SD original, nao no espelho PC).

## Favoritos operador (confirmados no espelho SNES)

| Titulo | Ficheiro |
|---|---|
| Metal Warriors | `Metal Warriors.smc` |
| Rock n' Roll Racing | `Rock n' Roll Racing.smc` (+ variantes EU `.zip`) |

## Flag `include_all_regions`

Entradas Parodius nos manifestos usam `include_all_regions: true` para o script de curadoria incluir **JP + EU + USA** (nao aplicar filtro USA-only nestes titulos).

## Proximo passo

`curate_rg43h_roms.py` deve copiar todos os matches Parodius + Metal Warriors + Rock N' Roll Racing para `staging/`.
