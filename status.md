# status.md

## Data da ultima atualizacao

2026-08-31

## Resumo do estado atual

Pacote documental Android (passo 1) concluido. Espelho local de scrape ES-DE em `resources/es-de/` (~10,8 GB; fora do Git). **Biblioteca ROMs mesclada (2026-08-30):** `new-roms` + biblioteca externa movidos para `resources/roms/` (~40k ROMs android, ~675 pc-only, BIOS em `resources/roms/bios/`); prioridade USA aplicada (26k descartados JP/EU). **Razr (2026-08-04):** no aparelho restam so ROMs + media ES-DE de **megadrive** e **snes**; demais sistemas removidos do celular (repo PC intacto). Apps (RetroArch, ES-DE, Eden, DuckStation) mantidos. Neo Geo: BIOS `new-roms` com CRC FBNeo correto (`94416D67`); smoke test pendente. Switch ROMs tirados do aparelho; Neon Apex push **adiado** ate nova decisao. Poco X3 NFC bloqueado pelo MIUI. **RG43H PRO (2026-08-31):** 526 ROMs no SD; SNES OK no aparelho; scrape in-device **indisponivel** (RGBox). Capas via `apply_esde_media_rg43h.py`: **126/458** no staging (media ES-DE parcialmente sincronizada no Drive). Cartao H: desmontado no ultimo deploy de midia — reinserir e `--deploy`. Guia: `resources/rg43h/docs/operator-guide.md`.

## Tarefas pendentes

- **RG43H:** sincronizar `resources/es-de/downloaded_media/` offline no Google Drive; reexecutar `apply_esde_media_rg43h.py --execute --yes --deploy H:\`; smoke test outros sistemas.
- Smoke test PC (RetroArch/DuckStation): 2 jogos por sistema (complementar).
- Verificar pasta externa `Recursos/Jogos/roms/ROMs/` (6 arquivos nao mapeados).
- Limpar placeholders vazios em `resources/new-roms/` (opcional).
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
- Set MAME / Neo Geo no Razr: operador reportou tela preta antes da limpeza; BIOS mesclada tem CRC FBNeo correto — revalidar em emulador antes de reenviar.
- Assinatura Play Store vs APK oficial do RetroArch exige desinstalacao previa.
- `psx`, `n64`, `psp` etc. agora populados no espelho PC; smoke test ainda nao executado.
- O espelho `resources/roms/` e `resources/es-de/downloaded_media/` ocupam espaco no Google Drive.

## Proximos passos

1. Operador: Google Drive → `downloaded_media` disponivel offline → `apply_esde_media_rg43h.py --execute --yes --deploy H:\`.
2. Operador RG43H: smoke test 2 jogos/sistema (MD, NES, Neo Geo, …).
3. Operador: rescan/reabrir ES-DE no Razr (so Mega Drive + SNES).
4. Poco X3 NFC: resolver "Instalar via USB" e repetir faixa Android padrao.

## Mudancas recentes

- **RG43H capas ES-DE:** `apply_esde_media_rg43h.py` — 126/458 capas no staging; SNES 14/115 (Drive parcial A–E). Relatorio: `reports/2026-08-31-rg43h-esde-media.md`.
- **RG43H guia operador:** `resources/rg43h/docs/operator-guide.md` (saves/savestates + scrape/capas); SNES confirmado no aparelho; scrape in-device bloqueado no RGBox.
- **RG43H curadoria v2 (rom_set):** suporte `rom_set` em manifestos Neo Geo/arcade; re-curadoria 526 matched (+60); Neo Geo 45/45; redeploy SD `H:` (3447 ficheiros, ~8,9 GB).
- **RG43H curadoria + deploy SD 128 GB:** `curate_rg43h_roms.py` + `deploy_rg43h_sd.ps1`; staging EmuELEC FAT32 EEROMS. Relatorio: `reports/2026-08-30-rg43h-curate-deploy.md`.
- Mesclagem ROMs: `merge_roms.py` moveu `new-roms` + biblioteca externa → `resources/roms/` (60k movidos, 26k JP/EU descartados); dedupe pos-merge (5.469 renomeados). Relatorio: `reports/2026-08-30-merge-roms.md`.
- Limpeza Razr: so `megadrive` + `snes` no aparelho; demais ROMs/media/gamelists removidos (PC intacto).
- Pull ES-DE: `downloaded_media/` (~10,8 GB) + `gamelists/` do Razr → `resources/es-de/` (gitignore).
- Tutorial `eden-install-updates.md` (Install to NAND a partir de `ROMs/switch/updates/`).
- Switch: pasta `updates/`, nomes limpos, UPD movidos; convencao em `rom-layout.md`.
- Neo Geo: diagnostico FBNeo — BIOS local com CRC errado; operador reportou tela preta Neo Geo/MAME.
