# Android — celular e tablet (ES-DE + ADB)

Documentacao e preparacao de recursos para emulacao legada em aparelhos Android.

Ordem de implantacao:

1. **Celular primario** — Poco X3 NFC (Snapdragon 732G) — bloqueado por MIUI ate haver SIM / "Instalar via USB"
2. **Bancada de teste temporaria** — Motorola Razr 50 Ultra — ver [docs/stage-razr-50-ultra-test.md](docs/stage-razr-50-ultra-test.md) (Mario / Zelda / Mario Kart em N64·GC·Wii; **sem** Switch)
3. **Tablet** — mesmo fluxo ADB/APK e mesma arvore de ROMs (modelo a registrar na checklist)

## Escopo de hardware

Limite pratico no Poco X3 NFC: sistemas da biblioteca documentada (8-bit ate PS1 / arcade leve). Nao configurar Switch ou PS2 nestes aparelhos.

Biblioteca atual do operador: ver `docs/rom-layout.md`. Pasta `PC` da origem fica fora deste passo. N64 e PSP nao constam na biblioteca atual.

## Caminho primario: ADB + APKs oficiais

Play Store e apenas fallback restrito. Motivos principais:

- RetroArch na loja e limitado (Core Downloader restrito; doc Libretro nao recomenda).
- ES-DE Android e pago e **nao** esta na Play Store.
- DuckStation Android sem suporte ativo do autor; arquivar APK oficial.

## Stack

| Papel | Software | Obtencao |
|---|---|---|
| Frontend | ES-DE (pago, canal oficial) | `es-de.org` / Patreon / Galaxy Store / AppGallery |
| Multi-sistema | RetroArch AArch64 | APK em `retroarch.com` |
| PS1 | DuckStation | APK em `duckstation.org/android/` |

Daijisho e PPSSPP nao entram no caminho primario desta entrega.

## Ordem recomendada de leitura

1. [docs/resources-inventory.md](docs/resources-inventory.md) — o que baixar e onde colocar em `resources/android/`
2. [docs/rom-layout.md](docs/rom-layout.md) — mapeamento da biblioteca → pastas ES-DE
3. [docs/setup-adb.md](docs/setup-adb.md) — instalacao primaria (inclui secao 8: layout paisagem RetroArch via GUI + replicacao ADB do cfg)
4. [docs/checklist.md](docs/checklist.md) — aceite celular / tablet
5. [docs/stage-razr-50-ultra-test.md](docs/stage-razr-50-ultra-test.md) — etapa extra temporaria (Mario / Zelda / Mario Kart no Razr)
6. [docs/eden-install-updates.md](docs/eden-install-updates.md) — instalar NSP de update no Eden (Razr; pasta `ROMs/switch/updates/`)
7. [docs/setup-play-store.md](docs/setup-play-store.md) — fallback (opcional)

Contrato da pasta de binarios locais: [resources/android/README.md](../../../resources/android/README.md) (APKs, BIOS, `config/` para `retroarch.cfg`).

Ferramentas ADB na raiz do repo: [tools-android.md](../../../tools-android.md).

## Fora de escopo (este passo)

- Configuracao ao vivo ja marcada como concluida sem evidencia
- Scripts ADB automatizados (fase seguinte)
- Pasta `PC` da biblioteca
- Alvos Windows 11 e Linux Ubuntu 26
- Versionar ROMs, BIOS ou APKs

## Autoridade

- `spec_root.md`
- Spec de dominio historica: `specs/done/spec-domain-emulation.md` (frontend antigo: Daijisho; **decisao atual do operador: ES-DE**)
