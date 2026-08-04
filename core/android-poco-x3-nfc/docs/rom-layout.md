# Layout de ROMs

## Fonte no PC do operador

Biblioteca de origem (nao versionar no Git):

`G:\Meu Drive\Recursos\Jogos\roms`

## Espelho local no repositorio (duas faixas)

```text
resources/roms/
  android/          # consoles adequados ao Poco X3 NFC / tablet Android
  pc-only/          # consoles/jogos so para emulacao desktop (PC)
```

Toda a arvore `resources/roms/` e ignorada pelo Git (regra `roms/` / `ROMs/` em `.gitignore`). Binarios ficam locais.

Nomes de pasta = canon ES-DE (minusculo). Referencia: tabela *Supported game systems* do [ANDROID.md](https://gitlab.com/es-de/emulationstation-de/-/blob/master/ANDROID.md) do ES-DE.

Destino no aparelho Android (raiz unica deste projeto):

```text
/storage/emulated/0/game-console/
  ES-DE/                 # Application data do frontend
  ROMs/<sistema>/        # jogos
  Games/BIOS/            # BIOS
```

Caminho tipico de ROMs: `/storage/emulated/0/game-console/ROMs/<sistema>/`

---

## Faixa Android — `resources/roms/android/<sistema>/`

Consoles no teto confortavel do Snapdragon 732G (ate Dreamcast/Saturn/N64/PSP/NDS e legados). **Nao** inclui GC/Wii/PS2/Switch.

### Com conteudo hoje (espelho da biblioteca do operador)

| Origem | Sistema | Pasta ES-DE | Emulador / core previsto | Estado |
|---|---|---|---|---|
| `2600` | Atari 2600 | `atari2600` | RetroArch (Stella) | vazia |
| `LYNX` | Atari Lynx | `atarilynx` | RetroArch (Handy) | vazia |
| `WSWAN` | WonderSwan | `wonderswan` | RetroArch (Beetle Cygne) | vazia |
| `GB` | Game Boy | `gb` | RetroArch (Gambatte / SameBoy) | presente |
| `GBC` | Game Boy Color | `gbc` | RetroArch (Gambatte / SameBoy) | presente |
| `GBA` | Game Boy Advance | `gba` | RetroArch (mGBA) | presente |
| `NES` | NES | `nes` | RetroArch (Mesen / Nestopia) | presente |
| `SNES` | Super Nintendo | `snes` | RetroArch (Snes9x) | presente |
| `SMS` | Master System | `mastersystem` | RetroArch (Genesis Plus GX) | presente |
| `SMD` | Mega Drive / Genesis | `megadrive` | RetroArch (Genesis Plus GX) | presente |
| `PCE` | PC Engine | `pcengine` | RetroArch (Beetle PCE) | presente |
| `NEOGEO` | Neo Geo AES/MVS | `neogeo` | RetroArch (FinalBurn Neo) + BIOS | presente |
| `MAME` | Arcade | `mame` | RetroArch (MAME / FBNeo) | presente |
| `PS1` | PlayStation 1 | `psx` | DuckStation | vazia |

Atencao: em `megadrive` a extensao `.md` e ROM de Mega Drive, nao Markdown.

### Pastas reservadas (criadas; sem ROMs ainda)

| Pasta ES-DE | Sistema | Emulador / core previsto | BIOS? |
|---|---|---|---|
| `n64` | Nintendo 64 | Mupen64Plus-Next / M64Plus FZ | Nao |
| `psp` | PlayStation Portable | PPSSPP | Nao |
| `nds` | Nintendo DS | melonDS / DraStic | Nao |
| `dreamcast` | Sega Dreamcast | Flycast / Redream | Nao (na maioria dos setups) |
| `saturn` | Sega Saturn | YabaSanshiro / Beetle Saturn | Sim |
| `gamegear` | Sega Game Gear | Genesis Plus GX | Nao |
| `sg-1000` | Sega SG-1000 | Genesis Plus GX | Nao |
| `sega32x` | Mega Drive 32X | PicoDrive | Nao |
| `segacd` | Sega CD / Mega CD | Genesis Plus GX | Sim |
| `virtualboy` | Nintendo Virtual Boy | Beetle VB | Nao |
| `ngp` | Neo Geo Pocket | Beetle NeoPop | Nao |
| `ngpc` | Neo Geo Pocket Color | Beetle NeoPop | Nao |
| `wonderswancolor` | WonderSwan Color | Beetle Cygne | Nao |
| `fds` | Famicom Disk System | Mesen / Nestopia | Sim |
| `neogeocd` | Neo Geo CD | NeoCD | Sim |
| `atari7800` | Atari 7800 | ProSystem | Sim |
| `atari5200` | Atari 5200 | a5200 | Sim |
| `colecovision` | ColecoVision | blueMSX | Sim |
| `intellivision` | Intellivision | FreeIntv | Sim |
| `msx` | MSX | blueMSX | Sim |
| `msx2` | MSX2 | blueMSX | Sim |
| `amiga` | Commodore Amiga | PUAE | Sim |
| `c64` | Commodore 64 | VICE | Nao |
| `scummvm` | ScummVM | ScummVM | Nao |

---

## Faixa PC-only — `resources/roms/pc-only/<sistema>/`

Fora do envio Android. No Poco X3 NFC esses alvos sao fragis ou inadequados; no PC usam emuladores desktop.

| Pasta ES-DE | Sistema | Emulador desktop tipico | Estado |
|---|---|---|---|
| `dos/` | DOS / PC antigo (origem `PC`) | DOSBox / RetroArch | presente |
| `gc/` | Nintendo GameCube | Dolphin | vazia |
| `wii/` | Nintendo Wii | Dolphin | vazia |
| `wiiu/` | Nintendo Wii U | Cemu | vazia |
| `ps2/` | PlayStation 2 | PCSX2 | vazia |
| `ps3/` | PlayStation 3 | RPCS3 | vazia |
| `xbox/` | Xbox original | xemu | vazia |
| `xbox360/` | Xbox 360 | Xenia (Windows) | vazia |
| `switch/` | Nintendo Switch | Ryujinx / Eden (bancada Razr) | presente (local; fora do Git) |

### Switch — base vs updates

Espelho operacional (fora do Git; nao faz parte da faixa Android do Poco):

```text
resources/roms/switch/            # jogos base (.nsp / .xci) — visiveis no ES-DE
resources/roms/switch/updates/    # UPD / DLC — NAO lancar como jogo
```

No aparelho (Razr / raiz `game-console/`):

```text
/storage/emulated/0/game-console/ROMs/switch/
/storage/emulated/0/game-console/ROMs/switch/updates/
```

- Nomes limpos (ex.: `Mario Kart 8 Deluxe.nsp`); tags `[UPD]` / Title ID / `[vN]` sao opcionais e so para organizacao humana.
- O Eden identifica base/update pelo conteudo interno do NSP.
- Updates: instalar no Eden (Install Files / Install to NAND), nao abrir pelo carrossel do ES-DE. Tutorial: `eden-install-updates.md`.
- No push ADB: bases → `ROMs/switch/`; updates → `ROMs/switch/updates/`.

GC/Wii/PS2 podem rodar de forma parcial em Android high-end com tuning; neste repositorio permanecem em `pc-only/` por decisao de escopo do Poco X3 NFC.

---

## Arvore Android no aparelho (espelho das pastas da faixa)

```text
/storage/emulated/0/game-console/
  ES-DE/
  Games/BIOS/
  ROMs/
    amiga/ atari2600/ atari5200/ atari7800/ atarilynx/
    c64/ colecovision/ dreamcast/ fds/ gamegear/
    gb/ gba/ gbc/ intellivision/ mame/ mastersystem/
    megadrive/ msx/ msx2/ n64/ nds/ neogeo/ neogeocd/
    nes/ ngp/ ngpc/ pcengine/ psp/ psx/ saturn/ scummvm/
    sega32x/ segacd/ sg-1000/ snes/ virtualboy/
    wonderswan/ wonderswancolor/
```

No `adb push`, enviar so pastas **com ROMs**; pastas vazias podem existir no aparelho se o ES-DE gerar a estrutura, mas nao precisam ser copiadas do PC.

---

## Regras

- ROMs e BIOS nunca entram no Git.
- Envio ADB usa **somente** `resources/roms/android/`.
- Sem Switch/PS2/Wii/GC/PS3/Xbox na faixa Android deste projeto.
- `desktop.ini` / `Thumbs.db` nao fazem parte da biblioteca util.

## Relacionados

- Inventario de APKs: `resources-inventory.md`
- Instalacao ADB: `setup-adb.md`
- Checklist: `checklist.md`
- Estrutura resumida: `resources/roms-structure.md`
