# Checklist — Android (celular depois tablet)

Nao marcar host como configurado sem execucao real no aparelho. Itens abaixo sao aceite operacional.

Inventario de APKs: `resources-inventory.md`. Layout: `rom-layout.md`. ADB: `setup-adb.md`.

## A. Preparacao de recursos (PC)

- [ ] platform-tools (`adb`) instalado
- [ ] ES-DE APK em `resources/android/apk/` + hash registrado
- [ ] RetroArch AArch64 APK em `resources/android/apk/` + hash registrado (ja baixado: `retroarch-aarch64-1.22.2.apk`)
- [ ] DuckStation instalado (Play Store no aparelho **ou** APK local se disponivel)
- [ ] BIOS PS1 em `resources/android/bios/` (dump proprio)
- [ ] BIOS Neo Geo em `resources/android/bios/` (se `NEOGEO` for usada)

## B. Celular — Poco X3 NFC

Modelo esperado: Poco X3 NFC (Snapdragon 732G / Adreno 618).

- [ ] Depuracao USB autorizada (`adb devices` = device)
- [ ] ABI confirmada (`arm64-v8a`)
- [ ] Pastas `/storage/emulated/0/ROMs/<sistema>/` criadas
- [ ] RetroArch instalado (APK oficial)
- [ ] DuckStation instalado
- [ ] ES-DE instalado (build paga oficial)
- [ ] Package ids anotados (se divergirem da referencia)
- [ ] BIOS enviada
- [ ] ROMs enviadas a partir de `resources/roms/android/` (nunca `pc-only/`; pular pastas vazias)
- [ ] ES-DE first-run + diretorio de ROMs confirmado
- [ ] Scrapers / artes (opcional nesta fase, se desejado)
- [ ] RetroArch: video Vulkan
- [ ] RetroArch: cores instalados (Stella, Handy, Beetle Cygne, Gambatte/SameBoy, mGBA, Mesen/Nestopia, Snes9x, Genesis Plus GX, Beetle PCE, FBNeo/MAME conforme uso)
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
(data / observacoes)
```

## C. Tablet

Modelo: _(preencher quando conhecido)_

Serial ADB: _(preencher)_

- [ ] Mesmo fluxo ADB das secoes B (install + pastas + push)
- [ ] Mesmos APKs do inventario
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
