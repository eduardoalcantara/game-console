# tools-windows.md

Ferramentas e comandos relevantes para o alvo Windows 11.

## Ferramentas necessarias

- Intel Arc Graphics Windows DCH Driver (site oficial Intel)
- Visual C++ Redistributable (All-in-One)
- DirectX End-User Runtimes
- Ryujinx (binario portatil)
- ES-DE (EmulationStation Desktop Edition)
- Steam (opcional, para Non-Steam + Steam Input) ou atalho no ES-DE

## Caminhos recomendados

| Item | Caminho |
|---|---|
| Ryujinx | `C:\Emuladores\Ryujinx` |
| Blur | `C:\Games\Blur` |

## Dependencias do sistema

- Driver Intel Arc com Vulkan 1.3 atualizado (instalacao limpa recomendada).
- Redistributables C++ e DirectX conforme pacotes acima.
- `prod.keys` e firmware original correspondentes (nao versionar neste repositorio).

## Uso recomendado

1. Instalar driver e redistributables.
2. Extrair Ryujinx, colocar chaves/firmware, backend Vulkan na Intel Arc, resolucao 2x (1440p).
3. Configurar ES-DE (`es_systems.xml`) apontando para o Ryujinx.
4. Instalar Blur + patch da comunidade; integrar ao ES-DE ou Steam.

## Observacoes especificas de Windows

- Passos sao manuais; nao ha script PowerShell de setup neste bootstrap.
- Nunca commitiar `prod.keys`, ISOs ou dumps.
- Detalhes operacionais: `core/pc-modern-emulation/windows-11/README.md`.
