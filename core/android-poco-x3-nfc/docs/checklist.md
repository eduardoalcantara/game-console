# Checklist — Android (celular depois tablet)

Nao marcar host como configurado sem execucao real no aparelho. Itens abaixo sao aceite operacional.

Inventario de APKs: `resources-inventory.md`. Layout: `rom-layout.md`. ADB: `setup-adb.md`.

## A. Preparacao de recursos (PC)

- [ ] platform-tools (`adb`) — ZIPs em `resources/android/` (rev. 37.0.0); extrair + PATH (`tools-android.md`)
- [ ] ES-DE APK em `resources/android/apk/` + hash registrado
- [ ] RetroArch AArch64 APK em `resources/android/apk/` + hash registrado (ja baixado: `retroarch-aarch64-1.22.2.apk`)
- [ ] DuckStation instalado (Play Store no aparelho **ou** APK local se disponivel)
- [ ] BIOS PS1 em `resources/android/bios/` (dump proprio) — presente: `SCPH1001.BIN` (hash no inventario; fora do Git)
- [ ] BIOS Neo Geo em `resources/android/bios/` (se `NEOGEO` for usada)

## B. Celular — Poco X3 NFC

Modelo esperado: Poco X3 NFC (Snapdragon 732G / Adreno 618).

> **Desvio 2026-07-25:** o Poco X3 NFC bloqueou a instalacao via ADB (MIUI 14 exige "Instalar via USB" com conta Mi + verificacao por SIM, indisponivel no aparelho). A instalacao foi feita no **Motorola Razr 50 Ultra** (`ZY22JXF44B`, `arcfox`, Android 16, `arm64-v8a`). O restante deste bloco foi executado nele. Poco fica pendente ate resolver a restricao MIUI.

- [x] Depuracao USB autorizada (`adb devices` = device) — Razr `ZY22JXF44B`
- [x] ABI confirmada (`arm64-v8a`) — Razr
- [x] Pastas sob `/storage/emulated/0/game-console/` (`ES-DE`, `ROMs/<sistema>/`, `Games/BIOS`) — Razr (desde 2026-08-04: so `megadrive` + `snes` no aparelho)
- [x] RetroArch instalado (`com.retroarch.aarch64`) — Razr
- [x] DuckStation instalado (`com.github.stenzek.duckstation`, via `install-multiple` do bundle APKM) — Razr
- [x] ES-DE instalado (`org.es_de.frontend`, build paga) — Razr
- [x] Package ids anotados (ver acima)
- [x] BIOS enviada (`game-console/Games/BIOS/SCPH1001.BIN`, 512 KB) — Razr
- [x] ROMs enviadas a partir de `resources/roms/android/` — Razr (contagem recursiva conferida = 1.976 arquivos, 10 sistemas; raiz reorganizada para `game-console/` em 2026-07-25)
- [ ] ES-DE first-run + diretorio de ROMs confirmado
- [ ] Scrapers / artes (opcional nesta fase, se desejado)
- [ ] RetroArch: video Vulkan
- [ ] RetroArch: cores instalados (Stella, Handy, Beetle Cygne, Gambatte/SameBoy, mGBA, Mesen/Nestopia, Snes9x, Genesis Plus GX, Beetle PCE, FBNeo/MAME conforme uso)
- [ ] RetroArch: layout paisagem calibrado na GUI (overlay + video no centro; `setup-adb.md` secao 8)
- [ ] RetroArch: cfg arquivado em `resources/android/config/poco-x3-nfc/` (path real do aparelho anotado abaixo se divergir)
- [ ] DuckStation: 2x (720p), GPU Vulkan, BIOS apontada
- [ ] Players ES-DE: RetroArch para sistemas RetroArch; DuckStation para `psx`

### Smoke test por sistema (celular)

Um titulo por pasta; marcar so apos teste real. Sistemas sem ROM na biblioteca atual ficam bloqueados.

- [ ] gb
- [ ] gbc
- [ ] gba
- [ ] nes
- [ ] snes
- [ ] mastersystem
- [ ] megadrive
- [ ] pcengine
- [ ] neogeo (requer BIOS)
- [ ] mame (anotar set / core usado)
- [ ] ~~atari2600~~ — sem ROMs na biblioteca
- [ ] ~~atarilynx~~ — sem ROMs na biblioteca
- [ ] ~~wonderswan~~ — sem ROMs na biblioteca
- [ ] ~~psx~~ — sem ROMs na biblioteca (DuckStation sem conteudo)

Notas do celular (desvios, fallback OpenGL, falhas):

```text
2026-07-25 — Instalacao migrada do Poco X3 NFC para Motorola Razr 50 Ultra.
  Poco (M2007J20CG / surya, Android 12, MIUI 14 V14.0.2.0): adb devices=device,
  mas installs falharam: RetroArch INSTALL_FAILED_VERIFICATION_FAILURE;
  ES-DE INSTALL_FAILED_USER_RESTRICTED; toggle "Instalar via USB" exige SIM/verificacao Mi.
  DuckStation: arquivo era bundle APKM (APKMirror), nao APK unico -> extraido base.apk +
  split_config.arm64_v8a.apk e instalado com adb install-multiple.
  Razr 50 Ultra (arcfox / ZY22JXF44B, Android 16): 3 installs OK, BIOS+ROMs enviadas,
  contagem recursiva local==device para os 10 sistemas.
  2026-07-25 — Pastas reorganizadas sob /storage/emulated/0/game-console/{ES-DE,ROMs,Games}.
  2026-08-04 — Limpeza no Razr: ROMs + downloaded_media + gamelists removidos de todos
  os sistemas exceto megadrive e snes (~2 GB ROMs + ~3,1 GB media no aparelho).
  Espelho local no PC intacto. Operador reportou tela preta em Neo Geo e MAME/arcade
  antes da remocao; Neo Geo: neogeo.zip com CRC incompativel com FBNeo (ja diagnosticado);
  MAME: falha observada (core/BIOS/romset) — sem fix neste ciclo.
```

## C. Tablet

Modelo: _(preencher quando conhecido)_

Serial ADB: _(preencher)_

- [ ] Mesmo fluxo ADB das secoes B (install + pastas + push)
- [ ] Mesmos APKs do inventario
- [ ] RetroArch: cfg do Poco usado so como base; viewport/escala revalidados na GUI do tablet
- [ ] RetroArch: cfg do tablet arquivado em `resources/android/config/<modelo>/`
- [ ] Smoke test dos sistemas usados no tablet
- [ ] Desvios vs celular registrados abaixo

Notas do tablet:

```text
(data / modelo / observacoes)
```

## D. Fora desta checklist

- Pasta `PC` da biblioteca
- N64 / PSP / PPSSPP
- Windows 11 / Linux Ubuntu 26
- Scripts ADB automatizados

## Encerramento

Apos validacao real: atualizar `status.md`, `timeline.md` e, se formal, `reports/`.
