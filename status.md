# status.md

## Data da ultima atualizacao

2026-07-24

## Resumo do estado atual

Bootstrap do repositorio game-console concluido: raiz documental padrao criada, conteudo de dominio sob `/core`, script Linux de emulacao versionado. Execucao real nos hosts (Android, Windows 11, Ubuntu 26) ainda nao realizada.

## Tarefas concluidas

- Inicializacao Git na raiz.
- Estrutura de pastas padrao (`docs/`, `ideas/`, `specs/`, `references/`, `scripts/`, `reports/`, `prompts/`, `resources/`, `core/`).
- Arquivos de governanca na raiz.
- Specs de entrada movidas para `specs/`.
- READMEs de dominio Android, Windows 11 e Linux Ubuntu 26.
- Script `setup_linux_emulation.sh` com suporte a `--uninstall`.

## Tarefas pendentes

- Executar e validar o setup Linux em host Ubuntu/Kubuntu 26.
- Aplicar manualmente os guias Android e Windows 11 nos dispositivos.
- Adicionar scripts de raiz em `./scripts/<categoria>/` quando houver necessidade real.

## Riscos

- Spec de dominio original pedia script "exato"; a governanca de scripts exigiu adaptacao (`--uninstall`, cabecalho, `REPO_ROOT`).
- Pacotes Flatpak e nomes de apps podem mudar no Flathub.
- Ubuntu 26 pode nao estar disponivel no host do operador; versoes proximas exigem validacao local.

## Proximos passos

1. Rodar o script Linux em ambiente controlado e registrar resultado em `reports/`.
2. Completar configuracao manual Android/Windows conforme READMEs em `core/`.
3. Atualizar `timeline.md` a cada entrega.

## Mudancas recentes

- Bootstrap inicial conforme `specs/spec-root-repo-build-complete.md` e `specs/spec-domain-emulation.md`.
