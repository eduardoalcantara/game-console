# Android — Poco X3 NFC (jogos legados)

## Escopo do hardware

O Poco X3 NFC utiliza o chipset Snapdragon 732G. Limite a configuracao a sistemas de 8-bit ate PlayStation 1, Nintendo 64 e PSP. Nao tente configurar emuladores de Switch ou PS2 neste dispositivo.

## Softwares e emuladores (download e configuracao)

### 1. Frontend Daijisho

Instale o frontend **Daijisho** (disponivel na Google Play Store).

### 2. RetroArch (AArch64)

Baixe o **RetroArch (AArch64)** via site oficial (build noturna) ou Play Store.

- Configure os seguintes cores (nucleos): `Snes9x` (SNES), `Genesis Plus GX` (Mega Drive), `Mupen64Plus-Next` (N64).
- Defina a API de video para `Vulkan` em `Configuracoes > Video`.

### 3. DuckStation (PS1)

Instale o **DuckStation** (Play Store) para PS1.

- Configure a resolucao interna para 2x (720p).
- Defina o renderizador da GPU para `Vulkan`.

### 4. PPSSPP (PSP)

Instale o **PPSSPP** (Play Store) para PSP.

- Configure o pulo de quadros (Frameskip) para 0.
- Ative o buffer de graficos.

## Integracao

No Daijisho, aponte os caminhos das pastas de ROMs e selecione os emuladores instalados acima como os "Players" padrao para cada plataforma. Sincronize a biblioteca para baixar as artes automaticamente.

## Notas

- Nao versionar ROMs neste repositorio.
- Documentacao complementar pode ser adicionada em `docs/`.
- Autoridade do projeto: `spec_root.md`. Fonte de dominio: `specs/spec-domain-emulation.md`.
