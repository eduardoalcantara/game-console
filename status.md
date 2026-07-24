# status.md

## Data da ultima atualizacao

2026-07-24

## Resumo do estado atual

Pacote documental Android (passo 1) concluido. Biblioteca de ROMs dividida em `resources/roms/android/` (envio aos aparelhos) e `resources/roms/pc-only/` (Wii/PS2/Switch/DOS). Faixa Android ja deduplicada. Instalacao real no celular/tablet ainda nao realizada.

## Tarefas concluidas

- Bootstrap Git e governanca da raiz.
- Script Linux de emulacao com `--uninstall`.
- Documentacao Android passo 1:
  - hub `core/android-poco-x3-nfc/README.md`
  - `docs/resources-inventory.md`, `rom-layout.md`, `setup-adb.md`, `setup-play-store.md`, `checklist.md`
  - `resources/android/` (contrato + pastas apk/bios)
  - `tools-android.md`
  - `.gitignore` com extensoes de APK
  - `setup.md` atualizado (secao Android)
- Espelho local da biblioteca de ROMs em `resources/roms/{android,pc-only}/` com nomes canonicos ES-DE.
- Script `scripts/tooling/dedupe_roms.py` (dry-run padrao) para deduplicar por regiao/revisao.

## Tarefas pendentes

- Operador: baixar/comprar APKs e preencher tabela de hashes no inventario.
- Executar `setup-adb.md` no Poco X3 NFC e validar checklist (celular).
- Repetir no tablet (modelo ainda nao registrado).
- Executar e validar setup Linux em host Ubuntu/Kubuntu 26.
- Aplicar guia Windows 11 no host.

## Riscos

- ES-DE Android e pago e nao redistribuivel; sem APK local o fluxo ADB para.
- Package ids do ES-DE podem variar por canal (Patreon vs Galaxy Store).
- DuckStation Android sem suporte ativo; regressoes futuras de OS sao risco.
- Set MAME da biblioteca pode ser pesado/incompativel com o core escolhido no aparelho.
- Assinatura Play Store vs APK oficial do RetroArch exige desinstalacao previa.
- Pastas `atari2600`, `atarilynx`, `wonderswan` e `psx` estao vazias na biblioteca: sem ROMs de PS1, o DuckStation nao tem o que rodar.
- O espelho `resources/roms/` duplica ~2,6 GB dentro do Google Drive; se o espaco sincronizado for critico, remover a pasta apos enviar aos aparelhos.

## Proximos passos

1. Arquivar ES-DE, RetroArch e DuckStation em `resources/android/apk/` e registrar hashes.
2. Instalar no celular via ADB e preencher a checklist.
3. Apos aceite no celular, repetir no tablet.

## Mudancas recentes

- Inventario Android com colunas Manual/Automatizavel; RetroArch 1.22.2 baixado; DuckStation APK oficial 404 (fica Manual/Play Store).
- Mapa ES-DE expandido e split android/pc-only.
