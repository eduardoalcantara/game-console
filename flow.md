# flow.md

Fluxo operacional obrigatorio do agente no repositorio game-console.

## 1. Ordem de leitura obrigatoria

1. Ler `spec_root.md`.
2. Ler `rules.md`.
3. Ler `.cursorrules`.
4. Ler `rules_scripts.md` quando a tarefa envolver scripts.
5. Ler `status.md` e `timeline.md` para contexto atual.
6. Ler `specs/` e `docs/` relevantes ao tema.
7. Ler o README do alvo em `core/` quando a tarefa for de dominio.

## 2. Fluxo de execucao

1. Planejar a entrega com base no escopo confirmado.
2. Implementar ou documentar somente o escopo confirmado.
3. Validar o que foi feito.
4. Atualizar `status.md`.
5. Atualizar `timeline.md`.
6. Produzir relatorio de entrega em `reports/` quando a tarefa for entrega formal.
7. Registrar proximos passos.

## 3. Ordem de decisoes

1. A tarefa cabe no escopo de `spec_root.md`?
2. Ha contradicao entre specs, status ou regras?
3. Ha necessidade de script? Se sim, aplicar `rules_scripts.md`.
4. O conteudo e de dominio? Se sim, colocar sob `/core`.

## 4. Gate de confirmacao

Se faltar contexto, houver contradicao ou escopo indefinido: pausar e pedir esclarecimento. Nao inventar requisitos.

## 5. Checklist de execucao

- [ ] Leitura obrigatoria concluida
- [ ] Escopo confirmado
- [ ] Arquivos corretos sob `/core` ou raiz conforme tipo
- [ ] Scripts com limpeza, cabecalho, raiz detectada e `--uninstall` se instalacao
- [ ] Sem emojis em nomes/scripts; UTF-8 sem BOM

## 6. Passos de validacao

- Conferir estrutura e nomes canonicos.
- Conferir consistencia entre `spec_root.md`, `rules.md`, `.cursorrules`, `flow.md` e `rules_scripts.md`.
- Conferir que docs de dominio batem com `specs/spec-domain-emulation.md`.
- Nao afirmar validacao que nao ocorreu.

## 7. Passos de encerramento

- Atualizar `status.md` e `timeline.md`.
- Listar: o que foi alterado, validado, pendente, arquivos impactados, proximo passo, docs que justificam a acao.

## Regras

- Nao pular leitura obrigatoria.
- Nao comecar implementacao sem contexto.
- Nao misturar grupos ou temas sem autorizacao.
- Encerrar cada tarefa com validacao e atualizacao documental.
