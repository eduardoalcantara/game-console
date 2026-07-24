# spec_root.md

## 1. Proposito

Padronizar e operar a configuracao de emulacao e jogos para:

- Android Poco X3 NFC (sistemas legados ate PS1, N64 e PSP);
- PC Windows 11 (emulacao moderna e jogo PC Blur);
- PC Linux Ubuntu/Kubuntu 26 (Flatpak, Lutris/Proton).

Este arquivo e a autoridade arquitetural maxima do repositorio game-console.

## 2. Visao geral

O repositorio e documental e operacional. A raiz concentra governanca Cursor; o conteudo especifico do dominio vive em `/core`. Scripts de instalacao devem ser previsiveis, reversiveis e equivalentes em intencao entre plataformas quando houver pares.

## 3. Principios fundacionais

1. Repositorio nasce documentado.
2. A raiz e a fonte de orientacao operacional.
3. O agente precisa de contexto explicito (regras, fluxo, status, timeline).
4. Formato universal de raiz; conteudo adaptavel ao dominio.
5. Tudo especifico do projeto vive sob `/core` quando nao contrariar padrao da tecnologia.

## 4. Escopo

- Documentacao de setup por alvo (Android, Windows 11, Linux Ubuntu 26).
- Script de bootstrap Linux de emulacao sob `core/pc-modern-emulation/linux-ubuntu-26/scripts/`.
- Governanca de scripts, fluxo do agente, status e timeline vivos.
- Referencias e relatorios de entrega/validacao.

## 5. Fora de escopo

- Emuladores de Switch ou PS2 no Poco X3 NFC.
- Versionamento de ROMs, ISOs, firmware proprietario ou `prod.keys`.
- Execucao automatica remota nos dispositivos fisicos sem confirmacao do operador.
- Criacao de categorias futuras em `./scripts/` sem script real correspondente.

## 6. Arquitetura de alto nivel

```text
raiz (governanca)
  ├── flow, rules, status, timeline, setup, tools-*, .cursorrules
  └── core/ (dominio)
        ├── android-poco-x3-nfc/
        └── pc-modern-emulation/
              ├── windows-11/
              └── linux-ubuntu-26/
```

Contratos:

- Specs formais em `specs/` relacionam-se a este `spec_root.md`.
- Scripts seguem `rules_scripts.md` (cabecalho, limpeza de tela, `REPO_ROOT`, input 0/1, `--uninstall` quando instalacao).
- Mudancas relevantes atualizam `status.md` e `timeline.md`.

## 7. Regras permanentes

- Nao inventar requisitos fora das specs e deste arquivo.
- Nao extrapolar escopo de hardware Android.
- Nao versionar segredos, dumps ilegais ou chaves proprietarias.
- Scripts de instalacao oferecem desinstalacao reversa documentada.
- Input de escolha do usuario e sempre lista numerada (0=nao, 1=sim).

## 8. Criterios de sucesso

O repositorio esta pronto quando o Cursor consegue responder sem ambiguidade:

- o que o projeto e;
- quais sao as regras;
- como operar e validar;
- como documentar progresso;
- onde ficam referencias e o nucleo em `/core`;
- como o agente deve se comportar.

## 9. Conclusao normativa

Qualquer entrega neste repositorio deve respeitar esta autoridade, o fluxo em `flow.md` e as regras em `rules.md` / `rules_scripts.md` / `.cursorrules`.
