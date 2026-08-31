# Estrutura de `resources/roms`

Espelho local de ROMs (ignorado pelo Git). Dividido em duas faixas:

```text
resources/roms/
  android/     # consoles confortaveis no Poco X3 NFC / tablet
  pc-only/     # GC, Wii, Wii U, PS2, PS3, Xbox, Switch, DOS, …
```

| Faixa | Uso |
|---|---|
| `android/` | Fonte do `adb push` e do ES-DE no celular/tablet |
| `pc-only/` | Emulacao desktop (Windows 11 / Linux); **nao** enviar ao Android |

### Android (pastas ES-DE)

Com conteudo hoje: `gb`, `gbc`, `gba`, `nes`, `snes`, `mastersystem`, `megadrive`, `pcengine`, `neogeo`, `mame` (+ vazias espelhadas da origem: `atari2600`, `atarilynx`, `wonderswan`, `psx`).

Reservadas (vazias): `n64`, `psp`, `nds`, `dreamcast`, `saturn`, `gamegear`, `sg-1000`, `sega32x`, `segacd`, `virtualboy`, `ngp`, `ngpc`, `wonderswancolor`, `fds`, `neogeocd`, `atari7800`, `atari5200`, `colecovision`, `intellivision`, `msx`, `msx2`, `amiga`, `c64`, `scummvm`.

### PC-only (pastas ES-DE)

`dos` (presente), `gc`, `wii`, `wiiu`, `ps2`, `ps3`, `xbox`, `xbox360`, `switch`.

Mapeamento completo e emuladores: `core/android-poco-x3-nfc/docs/rom-layout.md`.

Dedupe No-Intro (faixa Android):

```bash
python scripts/tooling/dedupe_roms.py --root resources/roms/android
```

Mesclagem de fontes externas (move, prioridade USA):

```bash
python scripts/tooling/merge_roms.py --execute --yes
```

Fontes: `resources/new-roms/`, biblioteca externa (`G:\Meu Drive\Recursos\Jogos\roms`), destino `resources/roms/`.
