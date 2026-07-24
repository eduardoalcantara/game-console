# Relatorio — dry-run dedupe_roms

**Data:** 2026-07-24
**Script:** `scripts/tooling/dedupe_roms.py`
**Modo:** DRY-RUN (nenhum arquivo foi apagado ou renomeado)
**Biblioteca:** `resources/roms/`

## Resumo

| Metrica | Valor |
|---|---|
| Arquivos considerados | 2839 |
| Protegidos (hack/traducao/mod) | 0 |
| Delecoes planejadas | 40 |
| Renomeacoes planejadas (strip ` (USA)`) | 1919 |
| Alteracoes aplicadas | 0 |

## Delecoes por sistema

| Sistema | Qtd |
|---|---|
| `nes` | 15 |
| `snes` | 15 |
| `megadrive` | 7 |
| `mastersystem` | 3 |

## Delecoes por motivo

| Motivo | Qtd |
|---|---|
| revisao inferior ou empate (mesma regiao) | 21 |
| Europe apagada (existe USA) | 19 |

## Renomeacoes por sistema (remover sufixo USA)

| Sistema | Qtd |
|---|---|
| `nes` | 723 |
| `snes` | 721 |
| `megadrive` | 429 |
| `mastersystem` | 23 |
| `gba` | 10 |
| `gbc` | 7 |
| `gb` | 3 |
| `pcengine` | 3 |

## Lista completa de delecoes

Arquivos que **seriam apagados** se `--execute` fosse usado:

- `mastersystem\A\Alex Kidd in Miracle World (USA, Europe).sms`
  - motivo: revisao base inferior ou empate (mantida: Alex Kidd in Miracle World (USA, Europe) (v1.1).sms / v1.1)
- `mastersystem\P-Q-R\Phantasy Star (USA, Europe) (v1.2).sms`
  - motivo: revisao v1.2 inferior ou empate (mantida: Phantasy Star (USA, Europe) (v1.3).sms / v1.3)
- `mastersystem\T-U-V-W-X-Y-Z\Zillion (Europe) (v1.2).sms`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `megadrive\C\Contra - Hard Corps (USA, Korea).md`
  - motivo: revisao base inferior ou empate (mantida: Contra - Hard Corps (USA).md / base)
- `megadrive\E-F\ESWAT - City Under Siege (USA, Europe).md`
  - motivo: revisao base inferior ou empate (mantida: ESWAT - City Under Siege (USA).md / base)
- `megadrive\M\Michael Jackson's Moonwalker (World).md`
  - motivo: revisao base inferior ou empate (mantida: Michael Jackson's Moonwalker (World) (Rev A).md / Rev A)
- `megadrive\S\Sonic The Hedgehog 2 (World).md`
  - motivo: revisao base inferior ou empate (mantida: Sonic the Hedgehog 2 (World) (Rev A).md / Rev A)
- `megadrive\S\Street Fighter II' - Special Champion Edition (Europe).md`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `megadrive\T\Thunder Force II (USA, Europe).md`
  - motivo: revisao base inferior ou empate (mantida: Thunder Force II (USA).md / base)
- `megadrive\W-X-Y-Z\World of Illusion Starring Mickey Mouse and Donald Duck (USA, Korea).md`
  - motivo: revisao base inferior ou empate (mantida: World of Illusion Starring Mickey Mouse and Donald Duck (USA).md / base)
- `nes\B\Batman - The Video Game (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\B\Bionic Commando (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\B\Blaster Master (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\B\Bubble Bobble (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\C\Castlevania III - Dracula's Curse (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\D\DuckTales (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\I-J-K\Indiana Jones and the Last Crusade (USA) (UBI Soft).nes`
  - motivo: revisao base inferior ou empate (mantida: Indiana Jones and the Last Crusade (USA) (Taito).nes / base)
- `nes\I-J-K\Kid Icarus (Europe) (Rev A).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\I-J-K\Kirby's Adventure (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\L\Legend of Zelda, The (Europe) (Rev A).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\M\Mega Man 2 (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\M\Metroid (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\M\Mike Tyson's Punch-Out!! (Europe) (Rev A).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `nes\P\Pac-Man (USA) (Tengen).nes`
  - motivo: revisao base inferior ou empate (mantida: Pac-Man (USA) (Namco).nes / base)
- `nes\S\Super Mario Bros. 3 (Europe).nes`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `snes\D-E\Donkey Kong Country (USA) (Competition Edition).smc`
  - motivo: revisao base inferior ou empate (mantida: Donkey Kong Country (USA) (Rev 2).smc / Rev 2)
- `snes\D-E\Donkey Kong Country 2 - Diddy's Kong Quest (Europe) (En,Fr) (Rev 1).sfc`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `snes\F\F-Zero (USA).smc`
  - motivo: revisao base inferior ou empate (mantida: F-Zero (USA).sfc / base)
- `snes\I-J\International Superstar Soccer (Europe).smc`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `snes\K-L\Killer Instinct (USA).sfc`
  - motivo: revisao base inferior ou empate (mantida: Killer Instinct (USA) (Rev 1).smc / Rev 1)
- `snes\M\Mega Man X (E).smc`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `snes\S\Star Fox (USA) (Super Weekend Competition).smc`
  - motivo: revisao base inferior ou empate (mantida: Star Fox (USA) (Rev 2).smc / Rev 2)
- `snes\S\Street Fighter II Turbo (USA).smc`
  - motivo: revisao base inferior ou empate (mantida: Street Fighter II Turbo (USA).sfc / base)
- `snes\S\Super Castlevania IV (USA).smc`
  - motivo: revisao base inferior ou empate (mantida: Super Castlevania IV (USA).sfc / base)
- `snes\S\Super Mario World (USA).sfc`
  - motivo: revisao base inferior ou empate (mantida: Super Mario World (U) [!].smc / base)
- `snes\S\Super Mario World (USA).smc`
  - motivo: revisao base inferior ou empate (mantida: Super Mario World (U) [!].smc / base)
- `snes\S\Super Mario World 2 - Yoshi's Island (USA).sfc`
  - motivo: revisao base inferior ou empate (mantida: Super Mario World 2 - Yoshi's Island (USA) (Rev 1).smc / Rev 1)
- `snes\S\Super Metroid (Europe) (En,Fr,De).sfc`
  - motivo: regiao Europe inferior a USA (grupo tem versao USA)
- `snes\S\Super Street Fighter II (USA).smc`
  - motivo: revisao base inferior ou empate (mantida: Super Street Fighter II (USA).sfc / base)
- `snes\T\Teenage Mutant Ninja Turtles IV - Turtles in Time (USA).smc`
  - motivo: revisao base inferior ou empate (mantida: Teenage Mutant Ninja Turtles IV - Turtles in Time (USA).sfc / base)

## Amostra de renomeacoes

Mostrando as primeiras 40 (lista completa no artefato bruto).

- `gb\Gradius - The Interstellar Assault (USA).gb` → `gb\Gradius - The Interstellar Assault.gb`
- `gb\Mega Man V (USA) (SGB Enhanced).gb` → `gb\Mega Man V (SGB Enhanced).gb`
- `gb\Operation C (USA).gb` → `gb\Operation C.gb`
- `gba\Astro Boy - Omega Factor (USA) (En,Ja,Fr,De,Es,It).gba` → `gba\Astro Boy - Omega Factor (En,Ja,Fr,De,Es,It).gba`
- `gba\Car Battler Joe (USA).gba` → `gba\Car Battler Joe.gba`
- `gba\Castlevania - Aria of Sorrow (USA).gba` → `gba\Castlevania - Aria of Sorrow.gba`
- `gba\Dragon Ball Z - Taiketsu (USA).gba` → `gba\Dragon Ball Z - Taiketsu.gba`
- `gba\Drill Dozer (USA).gba` → `gba\Drill Dozer.gba`
- `gba\Kirby & the Amazing Mirror (USA).gba` → `gba\Kirby & the Amazing Mirror.gba`
- `gba\Legend of Zelda, The - The Minish Cap (USA).gba` → `gba\Legend of Zelda, The - The Minish Cap.gba`
- `gba\Street Fighter Alpha 3 (USA).gba` → `gba\Street Fighter Alpha 3.gba`
- `gba\Super Mario Advance 4 - Super Mario Bros. 3 (USA).gba` → `gba\Super Mario Advance 4 - Super Mario Bros. 3.gba`
- `gba\WarioWare, Inc. - Mega Microgame$! (USA).gba` → `gba\WarioWare, Inc. - Mega Microgame$!.gba`
- `gbc\Harvest Moon GB (USA) (SGB Enhanced).gbc` → `gbc\Harvest Moon GB (SGB Enhanced).gbc`
- `gbc\Legend of Zelda, The - Oracle of Seasons (USA).gbc` → `gbc\Legend of Zelda, The - Oracle of Seasons.gbc`
- `gbc\Mario Golf (USA).gbc` → `gbc\Mario Golf.gbc`
- `gbc\Mario Tennis (USA).gbc` → `gbc\Mario Tennis.gbc`
- `gbc\Metal Gear Solid (USA).gbc` → `gbc\Metal Gear Solid.gbc`
- `gbc\Rayman (USA) (En,Fr,De,Es,It,Nl).gbc` → `gbc\Rayman (En,Fr,De,Es,It,Nl).gbc`
- `gbc\Shantae (USA).gbc` → `gbc\Shantae.gbc`
- `mastersystem\A\Aerial Assault (USA).sms` → `mastersystem\A\Aerial Assault.sms`
- `mastersystem\A\Alf (USA).sms` → `mastersystem\A\Alf.sms`
- `mastersystem\B-C\Captain Silver (USA).sms` → `mastersystem\B-C\Captain Silver.sms`
- `mastersystem\B-C\Castle of Illusion Starring Mickey Mouse (USA).sms` → `mastersystem\B-C\Castle of Illusion Starring Mickey Mouse.sms`
- `mastersystem\F-G\F-16 Fighting Falcon (USA).sms` → `mastersystem\F-G\F-16 Fighting Falcon.sms`
- `mastersystem\F-G\Galaxy Force (USA).sms` → `mastersystem\F-G\Galaxy Force.sms`
- `mastersystem\H-I-J-K\Hang-On & Astro Warrior (USA).sms` → `mastersystem\H-I-J-K\Hang-On & Astro Warrior.sms`
- `mastersystem\H-I-J-K\Hang-On & Safari Hunt (USA).sms` → `mastersystem\H-I-J-K\Hang-On & Safari Hunt.sms`
- `mastersystem\H-I-J-K\James 'Buster' Douglas Knockout Boxing (USA).sms` → `mastersystem\H-I-J-K\James 'Buster' Douglas Knockout Boxing.sms`
- `mastersystem\H-I-J-K\King's Quest - Quest for the Crown (USA).sms` → `mastersystem\H-I-J-K\King's Quest - Quest for the Crown.sms`
- `mastersystem\L-M-N-O\Marksman Shooting & Trap Shooting (USA).sms` → `mastersystem\L-M-N-O\Marksman Shooting & Trap Shooting.sms`
- `mastersystem\L-M-N-O\Monopoly (USA).sms` → `mastersystem\L-M-N-O\Monopoly.sms`
- `mastersystem\L-M-N-O\Montezuma's Revenge Featuring Panama Joe (USA).sms` → `mastersystem\L-M-N-O\Montezuma's Revenge Featuring Panama Joe.sms`
- `mastersystem\P-Q-R\Paperboy (USA).sms` → `mastersystem\P-Q-R\Paperboy.sms`
- `mastersystem\P-Q-R\Rambo - First Blood Part II (USA).sms` → `mastersystem\P-Q-R\Rambo - First Blood Part II.sms`
- `mastersystem\P-Q-R\Reggie Jackson Baseball (USA).sms` → `mastersystem\P-Q-R\Reggie Jackson Baseball.sms`
- `mastersystem\S\Slap Shot (USA) (v1.1).sms` → `mastersystem\S\Slap Shot (v1.1).sms`
- `mastersystem\S\Sports Pad Football (USA).sms` → `mastersystem\S\Sports Pad Football.sms`
- `mastersystem\S\Super Monaco GP (USA).sms` → `mastersystem\S\Super Monaco GP.sms`
- `mastersystem\T-U-V-W-X-Y-Z\Walter Payton Football (USA).sms` → `mastersystem\T-U-V-W-X-Y-Z\Walter Payton Football.sms`

... e mais 1879 renomeacoes.

## Observacoes

- Dry-run apenas: biblioteca intacta.
- Saves/companions (`.srm`, `.sav`, etc.) foram ignorados pelo script.
- Edicoes especiais entre parenteses (ex.: `Competition Edition`) competem com a ROM padrao do mesmo titulo, porque o agrupamento remove tags `()` / `[]`.
- Nenhum arquivo protegido (PT-BR/Hack/Mod/...) foi detectado nesta passagem.
- Artefato bruto do console: `reports/_dedupe_roms_dryrun_raw.txt` (auxiliar; pode ser removido apos auditoria).

## Proximo passo

1. Auditar a lista de delecoes acima.
2. Se estiver de acordo: `python scripts/tooling/dedupe_roms.py --execute`
3. Atualizar `status.md` / `timeline.md` apos execucao real.
