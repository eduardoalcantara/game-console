# Etapa extra — bancada de teste Razr 50 Ultra

Etapa **separada** e **temporaria**. Nao substitui o alvo primario (Poco X3 NFC).

Objetivo: enquanto o Poco estiver bloqueado pelo MIUI (Instalar via USB / SIM), usar o Motorola Razr 50 Ultra (`ZY22JXF44B`, Snapdragon 8s Gen 3, Android 16) para validar Mario / Zelda / Mario Kart em plataformas **mais leves que Switch**.

Escopo permanente do repo continua em `rom-layout.md` e `rules.md` (teto do 732G). Esta etapa **nao** move `pc-only/` para `android/` no repositorio.

## Status

| Item | Estado |
|---|---|
| Base ADB no Razr (APKs + ROMs legadas) | Feito 2026-07-25 |
| Jogos Mario / Zelda / Mario Kart desta etapa | **Pendente** — operador ainda precisa obter dumps legais |
| Execucao desta etapa | **Aguardando** jogos |

## Por que nao Switch aqui

Emular Switch (Eden/Citron/etc.) no Razr e **parcial** (Adreno 735 + termica de dobravel). Alem disso, exige `prod.keys`, firmware e dump do console proprio. Sem Switch fisico, nao ha caminho legal — e o projeto nao documenta obtencao de chaves/firmware.

Alternativa documentada: N64 / GameCube / Wii (e BOTW de Wii U no **PC**, fora desta etapa Android).

## Catalogo alvo (quando houver dumps)

Pastas ES-DE canônicas. Dump apenas de midia que o operador possui.

### Mario

| Jogo | Pasta | Emulador Android | Faixa no repo |
|---|---|---|---|
| Super Mario 64 | `n64` | Mupen64Plus-Next / M64Plus FZ | `resources/roms/android/n64/` |
| Super Mario Sunshine | `gc` | Dolphin | `resources/roms/pc-only/gc/` (envio **so** nesta etapa de teste) |
| Super Mario Galaxy / Galaxy 2 | `wii` | Dolphin | `resources/roms/pc-only/wii/` (envio so nesta etapa) |

### Zelda

| Jogo | Pasta | Emulador Android | Faixa no repo |
|---|---|---|---|
| Ocarina of Time / Majora's Mask | `n64` | Mupen64Plus-Next | `android/n64/` |
| The Wind Waker / Twilight Princess | `gc` | Dolphin | `pc-only/gc/` (envio so nesta etapa) |
| Skyward Sword | `wii` | Dolphin | `pc-only/wii/` (envio so nesta etapa) |

BOTW (Wii U) permanece fora desta etapa Android: preferir Cemu no PC (`pc-only/wiiu/` quando houver dump).

### Mario Kart

| Jogo | Pasta | Emulador Android | Faixa no repo |
|---|---|---|---|
| Mario Kart 64 | `n64` | Mupen64Plus-Next | `android/n64/` |
| Mario Kart: Double Dash!! | `gc` | Dolphin | `pc-only/gc/` (envio so nesta etapa) |
| Mario Kart Wii | `wii` | Dolphin | `pc-only/wii/` (envio so nesta etapa) |

## Pre-requisitos (quando for executar)

1. Dumps legais colocados nas pastas locais acima (sem versionar no Git).
2. No Razr: Dolphin + emulador N64 (standalone ou core RetroArch) instalados.
3. Players no ES-DE: `n64` → N64; `gc`/`wii` → Dolphin.
4. Nao tratar sucesso no Razr como aceite do Poco.

## Procedimento (futuro)

1. `adb -s ZY22JXF44B` (ou o serial atual).
2. Criar pastas no aparelho se necessario:

```bash
adb shell mkdir -p /storage/emulated/0/game-console/ROMs/n64
adb shell mkdir -p /storage/emulated/0/game-console/ROMs/gc
adb shell mkdir -p /storage/emulated/0/game-console/ROMs/wii
```

3. Push apenas dos jogos desta etapa (exemplos):

```bash
adb push resources/roms/android/n64/. /storage/emulated/0/game-console/ROMs/n64/
adb push resources/roms/pc-only/gc/. /storage/emulated/0/game-console/ROMs/gc/
adb push resources/roms/pc-only/wii/. /storage/emulated/0/game-console/ROMs/wii/
```

4. Rescan no ES-DE; smoke test: 1 Mario + 1 Zelda + 1 Mario Kart.
5. Registrar resultados na checklist (notas do Razr).
6. Quando o Poco tiver SIM/Mi Account: **nao** enviar `gc`/`wii` ao Poco; repetir so a faixa Android padrao.

## Relacionados

- `setup-adb.md` — base ADB
- `rom-layout.md` — mapa permanente android vs pc-only
- `checklist.md` — aceite e notas do desvio Poco → Razr
- Hub: `../README.md`
