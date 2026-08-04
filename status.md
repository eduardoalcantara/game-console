# status.md

## Data da ultima atualizacao

2026-08-04

## Resumo do estado atual

Pacote documental Android (passo 1) concluido. Espelho local de scrape ES-DE em `resources/es-de/` (~10,8 GB; fora do Git). **Razr (2026-08-04):** no aparelho restam so ROMs + media ES-DE de **megadrive** e **snes**; demais sistemas removidos do celular (repo PC intacto). Apps (RetroArch, ES-DE, Eden, DuckStation) mantidos. Neo Geo/MAME: tela preta reportada pelo operador (BIOS CRC FBNeo ja diagnosticada; MAME sem fix neste ciclo). Switch ROMs tirados do aparelho; Neon Apex push **adiado** ate nova decisao. Poco X3 NFC bloqueado pelo MIUI.

## Tarefas pendentes

- Operador: rescan/reabrir ES-DE no Razr (carrossel so MD + SNES).
- ADB (quando decidir): reenviar Switch / outros sistemas a partir do espelho local (incl. Neon Apex).
- Operador: obter `neogeo.zip` com CRCs FBNeo; diagnosticar MAME (core/set) antes de reenviar arcade.
- Operador: first-run ES-DE / cores RetroArch / layout / smoke test legado (checklist).
- Executar `setup-adb.md` no Poco X3 NFC e validar checklist (celular).
- Repetir no tablet (modelo ainda nao registrado).
- Executar e validar setup Linux em host Ubuntu/Kubuntu 26.
- Aplicar guia Windows 11 no host.

## Riscos

- Poco X3 NFC (MIUI 14) bloqueia install via ADB sem "Instalar via USB" (conta Mi + verificacao por SIM). Aparelho primario documentado nao esta operacional para ADB no momento.
- Razr 50 Ultra (SD 8s Gen 3) e muito mais forte que o Poco: a faixa de sistemas de `rules.md` (ate PS1/N64/PSP) foi definida para o Poco; se o Razr virar alvo oficial, revisar escopo antes de expandir.
- ES-DE Android e pago e nao redistribuivel; o APK esta local e coberto por `.gitignore` (nunca commitar).
- Package ids do ES-DE podem variar por canal (Patreon vs Galaxy Store).
- DuckStation Android sem suporte ativo; regressoes futuras de OS sao risco.
- Set MAME / Neo Geo no Razr: operador reportou tela preta; `neogeo.zip` local com CRC errado para FBNeo; arcade nao reenviar ate corrigir BIOS/core.
- Assinatura Play Store vs APK oficial do RetroArch exige desinstalacao previa.
- Pastas `atari2600`, `atarilynx`, `wonderswan` e `psx` estao vazias na biblioteca: sem ROMs de PS1, o DuckStation nao tem o que rodar.
- O espelho `resources/roms/` e `resources/es-de/downloaded_media/` ocupam espaco no Google Drive.

## Proximos passos

1. Operador: rescan/reabrir ES-DE no Razr (so Mega Drive + SNES).
2. Quando quiser Switch de novo: push a partir do espelho local (incl. Neon Apex) + Install to NAND dos UPD.
3. Antes de reenviar Neo Geo/MAME: BIOS FBNeo correta + diagnostico de core/set.
4. First-run ES-DE legado / cores RetroArch / layout (checklist) nos sistemas que voltarem.
5. Poco X3 NFC: resolver "Instalar via USB" e repetir faixa Android padrao.

## Mudancas recentes

- Limpeza Razr: so `megadrive` + `snes` no aparelho; demais ROMs/media/gamelists removidos (PC intacto).
- Pull ES-DE: `downloaded_media/` (~10,8 GB) + `gamelists/` do Razr → `resources/es-de/` (gitignore).
- Tutorial `eden-install-updates.md` (Install to NAND a partir de `ROMs/switch/updates/`).
- Switch: pasta `updates/`, nomes limpos, UPD movidos; convencao em `rom-layout.md`.
- Neo Geo: diagnostico FBNeo — BIOS local com CRC errado; operador reportou tela preta Neo Geo/MAME.
