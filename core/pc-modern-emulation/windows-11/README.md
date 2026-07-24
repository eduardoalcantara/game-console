# PC — Windows 11 (emulacao moderna e PC games)

## Drivers e dependencias iniciais

1. Baixe o **Intel Arc Graphics Windows DCH Driver** no site oficial da Intel. Realize a instalacao limpa para garantir suporte atualizado a API Vulkan 1.3.
2. Instale o pacote **Visual C++ Redistributable (All-in-One)** e o **DirectX End-User Runtimes**.

## Emuladores (download e configuracao)

### Ryujinx

1. Baixe o **Ryujinx** (binario portatil do site oficial).
2. Extraia em `C:\Emuladores\Ryujinx`.
3. Adicione o arquivo `prod.keys` mais recente na pasta `System` (acessivel via File > Open Ryujinx Folder).
4. Instale o Firmware original correspondente as chaves.
5. Em `Options > Settings > Graphics`, defina o Backend como `Vulkan` e a placa de video primaria como a Intel Arc. Resolucao: 2x (1440p).

Nao versionar `prod.keys` nem firmware neste repositorio.

### ES-DE

1. Baixe o **ES-DE (EmulationStation Desktop Edition)**.
2. Configure o arquivo `es_systems.xml` para apontar para o executavel do Ryujinx.

## Configuracao do jogo Blur (PC abandonware)

1. Adquira a imagem ISO original do Blur (PC).
2. Instale o jogo em `C:\Games\Blur`.
3. Baixe o patch da comunidade **"Blur Project"** (ou mods multiplayer documentados no PCGamingWiki) para restaurar a funcionalidade de rede local/online e suporte nativo a resolucoes ultrawide e controles modernos.
4. Substitua o executavel original pelo executavel do patch na pasta raiz do jogo.
5. Adicione o atalho do Blur manualmente no ES-DE ou no Steam como "Jogo Nao-Steam" para aproveitar o Steam Input para gerenciar os controles.

## Notas

- Passos manuais; sem script PowerShell neste bootstrap.
- Ver tambem `tools-windows.md` e `setup.md`.
- Fonte de dominio: `specs/spec-domain-emulation.md`.
