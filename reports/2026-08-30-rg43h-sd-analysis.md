# Analise SD original — AISLPC RG43H PRO (2026-08-30)

## Hardware do cartao atual

| Campo | Valor |
|---|---|
| Unidade | `H:` |
| Rotulo | **EEROMS** |
| Sistema de ficheiros | FAT32 |
| Capacidade | ~48,7 GB (cartao **50 GB** classe generica) |
| Controlador | NORELSYS 1081CS0 (leitor/cartao USB generico) |
| Particoes visiveis | **1** (MBR, FAT32, offset 4 MB) |
| Espaco usado | ~36,9 GB |
| Espaco livre | ~11,8 GB |

**Nota:** So aparece a particao de ROMs. O EmuELEC 4.7 + RGBox provavelmente reside no **storage interno** do aparelho; este SD e essencialmente a biblioteca `EEROMS`.

---

## Estrutura (particao EEROMS)

```text
H:\
  .firstDownload          # flag EmuELEC (vazio)
  bios/                   # BIOS todos os cores (~379 MB, 430 ficheiros)
  <sistema>/              # uma pasta por sistema, na raiz
  savestates/             # saves de estado
  screenshots/            # capturas
  BGM/                    # musica de fundo
  bezels/                 # molduras de ecrã
  splash/                 # splash screens
  ports/                  # ports nativos
  ports_scripts/
  downloads/
  .update/
  applyCenter/
  mplayer/
```

### Pastas de ROMs com conteudo real (~37 GB)

| Pasta SD | ROMs | Tamanho | Notas |
|---|---:|---:|---|
| psp | 26 | 14,6 GB | ISOs grandes |
| psx | 26 | 6,4 GB | CHD/BIN |
| neogeo | 301 | 4,9 GB | ROMs + `neogeo.zip` |
| dreamcast | 11 | 3,8 GB | |
| mame | 2.962 | 2,9 GB | |
| fbneo | 2.132 | 2,7 GB | |
| megadrive | 1.835 | 920 MB | |
| cps2 | 75 | 519 MB | |
| cps1/cps3 | 75 | 283 MB | |
| pcengine | 336 | 75 MB | |
| gba | 959 | 70 MB | |
| famicom | 1.128 | 65 MB | NES (No-Intro) |
| gamegear | 489 | 55 MB | |
| gbc/gb | 944 | 56 MB | |
| nes | 97 | 6 MB | subset NES |
| outros | — | <30 MB | atari, ngp, sega32x, sg-1000 |

**~77 pastas** existem mas estao **vazias** (placeholders EmuELEC/RGBox).

### Quirks de nomenclatura RGBox

O RGBox usa pastas paralelas que o ES-Android nao usa:

| SD (RGBox) | Equivalente ES-DE / PC | Conteudo neste SD |
|---|---|---|
| `famicom` + `nes` | `nes` | Famicom = bulk NES |
| `snes` / `snesh` / `sfc` | `snes` | SNES quase vazio aqui |
| `megadrive` / `genesis` / `genh` | `megadrive` | MD principal |
| `tg16` | `pcengine` | |
| `mame` + `fbneo` + `cps1/2/3` | `mame` / arcade | Separados no SD |
| `atarilynx` | `atarilynx` | |

### BIOS

- Localizacao canonica: **`bios/`** na raiz da particao EEROMS
- Ficheiros soltos + subpastas por core (`fbneo/`, `mame2010/`, `Mupen64plus/`, etc.)
- `neogeo.zip` em `bios/` — CRC `sm1.sm1` = **94416D67** (FBNeo OK)

---

## Comparacao com espelho PC (`resources/roms/android/`)

Biblioteca mesclada no PC para os mesmos sistemas: **~54,6 GB** (+ BIOS ~421 MB).

| Sistema | SD atual | PC mesclado |
|---|---:|---:|
| psx | 6,4 GB | **23,2 GB** |
| psp | 14,6 GB | 7,5 GB |
| gba | 70 MB | **9,7 GB** |
| snes | ~1 MB | **4,0 GB** |
| nes | 65 MB | 231 MB |
| megadrive | 920 MB | 1,0 GB |
| n64 | ~0 | **3,1 GB** |
| neogeo | 4,9 GB | 3,9 GB |

O PC tem muito mais conteudo (especialmente PSX, GBA, SNES, N64). **Nao cabe inteiro** no SD de 50 GB nem seria adequado ao hardware (N64/PSP parcial, PSX ok, Switch fora).

---

## Recomendacao: 128 GB vs 512 GB

### Para o RG43H → **128 GB V30** e suficiente

Estimativa para biblioteca **curada** (USA, sistemas ate PS1/PSP/N64 parcial):

| Componente | Estimativa |
|---|---:|
| ROMs curadas (legado + PSX + PSP leve + MD/SNES/NES/Neo Geo) | 40–70 GB |
| BIOS | ~0,5 GB |
| savestates / screenshots / bezels | 1–5 GB |
| Margem de crescimento | 10–20 GB |
| **Total** | **~55–95 GB** |

Um **128 GB** V30 (util real ~119 GB) cobre confortavelmente uma biblioteca curada sem desperdicar o cartao de 512 GB.

### 512 GB — melhor para o MP3 player

- RG43H nao precisa de 512 GB; PS2/PS3/Wii/Switch nem rodam bem ou estao fora de escopo.
- Copiar o espelho PC inteiro (~62 GB android + ~38 GB pc-only irrelevante) ainda caberia em 128 GB.
- **512 GB** so faz sentido se quiseres biblioteca massiva de PSP/PSX CHD + Dreamcast + tudo no cartao sem curadoria — overkill para este aparelho.

**Sugestao:** 128 GB V30 para RG43H; reserva 512 GB para o MP3 player como planeado.

---

## Plano para criar o novo SD

1. **Manter SD original intacto** como referencia/backup ate validar o novo.
2. **Flash imagem RGBox/EmuELEC** para RG43H (se o fabricante fornecer imagem especifica) **ou** formatar FAT32, rotulo `EEROMS`, se o SO for so interno.
3. Copiar **`bios/`** primeiro (do SD original ou de `resources/roms/bios/`).
4. Copiar ROMs **curadas** do PC (`resources/roms/android/`) para pastas SD correspondentes (ver tabela de mapeamento acima).
5. **Nao copiar** `pc-only/` (PS2, PS3, Wii, Switch, etc.).
6. Smoke test no PC antes de copiar (2 jogos/sistema).
7. Copiar `savestates/` / `bezels/` do SD antigo se quiseres preservar progresso e UI.

### Mapeamento PC → SD (principais)

| PC (`resources/roms/android/`) | SD (`EEROMS/`) |
|---|---|
| `nes/` | `nes/` ou `famicom/` |
| `snes/` | `snes/` |
| `megadrive/` | `megadrive/` |
| `gb/` `gba/` `gbc/` | `gb/` `gba/` `gbc/` |
| `neogeo/` | `neogeo/` |
| `mame/` | `mame/` |
| `fbneo/` | `fbneo/` |
| `psx/` | `psx/` |
| `psp/` | `psp/` |
| `n64/` | `n64/` |
| `pcengine/` | `pcengine/` ou `tg16/` |
| `atarilynx/` | `atarilynx/` |
| `dreamcast/` | `dreamcast/` |
| BIOS | `bios/` |

---

## Validacao

Inventario por contagem e tamanho no Windows (`H:`). Nenhum teste no aparelho fisico neste ciclo.

## Proximo passo

1. Operador decide: **128 GB** para RG43H.
2. Definir lista curada de sistemas (ex.: sem PSP massivo se performance for fraca).
3. Smoke test PC → copia para novo SD → teste no RG43H.
