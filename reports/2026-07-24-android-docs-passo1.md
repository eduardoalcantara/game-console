# Relatorio — Android passo 1 (docs + recursos)

**Data:** 2026-07-24  
**Justificativa:** pedido do operador (ADB primario, ES-DE pago, inventario de ROMs, celular depois tablet); alinhado a `spec_root.md` e a decisoes que atualizam o frontend Android relativo a `specs/done/spec-domain-emulation.md`.

## Objetivo

Montar apenas a documentacao e a estrutura de recursos para instalar o ambiente Android no celular (Poco X3 NFC) e depois no tablet — sem scripts ADB e sem execucao ao vivo nesta entrega.

## Decisoes aplicadas

- Frontend: **ES-DE pago** (canal oficial via `es-de.org`); Daijisho fora do caminho primario.
- Instalacao: **ADB/APK primario**; Play Store = fallback restrito.
- Emuladores obrigatorios: RetroArch AArch64 (APK oficial) + DuckStation.
- Biblioteca: pastas em `G:\Meu Drive\Recursos\Jogos\roms` mapeadas para canon ES-DE; pasta **`PC` ignorada**.
- PPSSPP / N64 fora (ausentes na biblioteca).

## Fontes verificadas (pesquisa previa)

- Libretro: Play Store do RetroArch marcada como nao recomendada; APK do site e a versao completa.
- DuckStation: suporte Android encerrado; APK oficial em `duckstation.org/android/`.
- ES-DE: Android pago; fora da Play Store; nao redistribuir APK.

## O que foi alterado

- Docs sob `core/android-poco-x3-nfc/docs/`
- Hub `core/android-poco-x3-nfc/README.md`
- `resources/android/` (README + apk/bios)
- `tools-android.md`
- `.gitignore` (extensoes APK)
- `setup.md`, `status.md`, `timeline.md`

## O que foi validado

- Consistencia documental estatica (estrutura, links relativos, mapeamento ROM → ES-DE).
- `.gitignore` cobre `*.apk` e variantes.

## O que nao foi validado

- Download real dos APKs pelo operador.
- Conexao ADB / instalacao no Poco ou tablet.
- Smoke test de jogos.
- Package id definitivo do ES-DE no canal que o operador usar.

## Pendencias

1. Preencher tabela de hashes no inventario apos baixar APKs.
2. Executar setup ADB no celular e checklist.
3. Informar modelo do tablet e repetir o fluxo.

## Criterio de aceite do plano

| Criterio | Estado |
|---|---|
| Operador sabe o que baixar e onde colocar | Atendido em `resources-inventory.md` |
| Cada pasta da biblioteca (exceto PC) mapeada | Atendido em `rom-layout.md` |
| Guia ADB para celular e tablet | Atendido em `setup-adb.md` |
| Nenhum APK/ROM/BIOS versionado | Atendido via `.gitignore` + contrato |
| Windows/Linux so com apontadores minimos | Atendido (`setup.md` / status / timeline) |
