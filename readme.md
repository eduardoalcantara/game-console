# game-console

Repositorio de documentacao e automacao para configuracao de emulacao e jogos em tres alvos: Android (Poco X3 NFC), Windows 11 e Ubuntu/Kubuntu 26.

## Publico e objetivo

Operadores e o agente Cursor usam este repositorio para montar, validar e manter ambientes de emulacao legada (Android) e moderna (PC), com governanca documental explicita e scripts reversiveis.

## Escopo

- Frontend e emuladores no Poco X3 NFC (ate PS1, N64 e PSP).
- Emulacao moderna e jogos PC no Windows 11 (Ryujinx, ES-DE, Blur).
- Bootstrap de emulacao no Linux Ubuntu 26 via Flatpak, Lutris e Proton.

## Estrutura de alto nivel

```text
.
├── core/                 # Conteudo especifico do dominio
│   ├── android-poco-x3-nfc/
│   └── pc-modern-emulation/
│       ├── windows-11/
│       └── linux-ubuntu-26/
├── specs/                # Especificacoes formais e fontes
├── docs/                 # Documentacao tecnica
├── scripts/              # Scripts de automacao na raiz (quando existirem)
├── reports/              # Relatorios de entrega e validacao
├── status.md             # Estado atual
├── timeline.md           # Historico
├── flow.md               # Fluxo operacional do agente
├── rules.md              # Regras permanentes
└── spec_root.md          # Autoridade arquitetural
```

## Como iniciar

1. Ler `spec_root.md`, `rules.md`, `.cursorrules` e `flow.md`.
2. Consultar `status.md` e `timeline.md`.
3. Seguir o guia do alvo desejado em `core/`.
4. No Linux, executar o script documentado em `core/pc-modern-emulation/linux-ubuntu-26/`.

Detalhes de ambiente: `setup.md`, `tools-linux.md`, `tools-windows.md`.

## Documentacao relacionada

| Documento | Funcao |
|---|---|
| `spec_root.md` | Autoridade arquitetural |
| `flow.md` | Ordem de leitura e execucao |
| `rules.md` | Governanca permanente |
| `rules_scripts.md` | Regras de scripts |
| `specs/spec-domain-emulation.md` | Spec de dominio (fonte) |
| `specs/spec-root-repo-build-complete.md` | Spec de bootstrap da raiz |

## Estado atual

Ver `status.md`. Bootstrap documental concluido; execucao real nos hosts permanece pendente.
