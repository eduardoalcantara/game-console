# spec-root-repo-build.md

## Objetivo

Este documento define a fundação universal para criação de qualquer novo repositório no Cursor.

Ele serve para projetos de software, hardware, configuração de sistema operacional, automação, impressão 3D, documentação técnica, pesquisa, ferramentas, bibliotecas, protótipos ou qualquer combinação desses domínios.

A meta é padronizar a raiz do repositório com estrutura, governança, contexto operacional e orientação suficiente para que o Cursor consiga trabalhar com consistência desde o primeiro momento.

---

## 1. Princípios centrais

### 1.1 Repositório nasce documentado
Todo projeto deve começar com uma estrutura mínima de contexto, não com arquivos soltos sem governança.

### 1.2 A raiz é a fonte de orientação
Os arquivos da raiz não são enfeites; cada um tem função operacional específica.

### 1.3 O agente precisa de contexto explícito
O Cursor deve encontrar no repositório as regras, o fluxo, o estado, o histórico e a orientação de trabalho.

### 1.4 O formato é universal, o conteúdo é adaptável
A espinha dorsal se mantém; o interior das pastas muda conforme o domínio do projeto.

### 1.5 Existe uma pasta `/core`
Todo projeto deve conter uma pasta `/core`, que concentra as pastas, arquivos e artefatos específicos do projeto.

### Regra obrigatória
Tudo que for específico do projeto deve viver sob `/core` sempre que isso não contrariar o padrão da tecnologia ou do domínio.

---

## 2. Estrutura raiz padrão

Todo novo repositório deve possuir, sempre que aplicável, os seguintes itens na raiz:

- `.gitignore`
- `readme.md`
- `spec_root.md`
- `flow.md`
- `rules.md`
- `status.md`
- `timeline.md`
- `setup.md`
- `tools-linux.md`
- `tools-windows.md`
- `.cursorrules`
- `spec_template.md`
- `rules_scripts.md`
- `docs/`
- `ideas/`
- `specs/`
- `references/`
- `scripts/`
- `reports/`
- `prompts/`
- `resources/`
- `core/`

### Regra
Pastas opcionais podem não existir em todos os projetos, mas a intenção estrutural deve permanecer clara.

---

## 3. Função dos arquivos da raiz

### 3.1 `.gitignore`
Define o que não deve entrar no versionamento.

### 3.2 `readme.md`
Explica o projeto para humanos: propósito, visão, escopo e uso inicial.

### 3.3 `spec_root.md`
É a autoridade arquitetural máxima do repositório.

### 3.4 `flow.md`
Define o fluxo operacional do agente: o que ler, em que ordem agir e como validar.

### 3.5 `rules.md`
Centraliza regras permanentes de governança, escopo, arquitetura e qualidade.

### 3.6 `status.md`
Registra o estado atual do projeto como snapshot mutável.

### 3.7 `timeline.md`
Registra o histórico do projeto em ordem cronológica decrescente, como log evolutivo.

### 3.8 `setup.md`
Documenta preparação do ambiente, instalação, bootstrap e caminhos de suporte.

### 3.9 `tools-linux.md`
Lista ferramentas, pacotes e comandos relevantes para Linux.

### 3.10 `tools-windows.md`
Lista ferramentas, pacotes e comandos relevantes para Windows.

### 3.11 `.cursorrules`
Define comportamento, honestidade, limites e formato de resposta do agente no repositório.

### 3.12 `spec_template.md`
Fornece o molde para novas specs do projeto.

### 3.13 `rules_scripts.md`
Define a governança de criação e execução de scripts, incluindo organização, input, cabeçalho, autodetecção da raiz, UX operacional e desinstalação reversa.

### 3.14 `docs/`
Armazena documentação técnica, operacional, normativa e de produto.

### 3.15 `ideas/`
Armazena hipóteses, rascunhos, propostas e ideias ainda não formalizadas.

### 3.16 `specs/`
Armazena especificações formais do projeto, com sub-pastas `to-do/` e `done/`

### 3.17 `references/`
Armazena referências locais, engenharia reversa, exemplos e materiais de estudo.

### 3.18 `scripts/`
Armazena scripts de automação, bootstrap, validação e apoio operacional.

### 3.19 `reports/`
Armazena relatórios de implementação, auditoria, validação e entrega.

### 3.20 `prompts/`
Armazena prompts reutilizáveis, colas e instruções mestre.

### 3.21 `resources/`
Armazena downloads, binários, imagens, apps auxiliares e materiais de apoio.

### 3.22 `core/`
Armazena o conteúdo específico do projeto, incluindo pastas de domínio, arquivos-fonte, ativos, modelos, componentes e artefatos operacionais próprios do repositório.

---

## 4. Estrutura correta de cada arquivo

### 4.1 `.gitignore`
- Ignorar artefatos temporários.
- Ignorar saídas de build, caches, logs e arquivos locais.
- Ignorar segredos, credenciais e arquivos específicos do ambiente.
- Não ignorar arquivos de governança do projeto.

### 4.2 `readme.md`
- Nome do projeto.
- Resumo do que ele faz.
- Público e objetivo.
- Estrutura de alto nível.
- Como iniciar.
- Documentação relacionada.
- Estado atual.

### 4.3 `spec_root.md`
- Propósito do projeto.
- Visão geral.
- Princípios fundacionais.
- Escopo.
- Fora de escopo.
- Arquitetura de alto nível.
- Contratos centrais.
- Regras permanentes.
- Critérios de sucesso.
- Conclusão normativa.

### 4.4 `flow.md`
- Ordem de leitura obrigatória.
- Fluxo de execução do agente.
- Ordem de decisões.
- Gate de confirmação.
- Checklist de execução.
- Passos de validação.
- Passos de encerramento.

### 4.5 `rules.md`
- Hierarquia normativa.
- Regras gerais permanentes.
- Regras de escopo.
- Regras de qualidade.
- Regras de documentação.
- Regras de validação.
- Regras de bloqueio.
- Regras de atualização.

### 4.6 `status.md`
- Data da última atualização.
- Resumo do estado atual.
- Tarefas concluídas.
- Tarefas pendentes.
- Riscos.
- Próximos passos.
- Mudanças recentes.

### 4.7 `timeline.md`
- Histórico cronológico reverso.
- Entrada por evento/entrega.
- Impacto.
- Arquivos afetados.
- Data.
- Observações relevantes.

### 4.8 `setup.md`
- Pré-requisitos.
- Instalação.
- Bootstrap.
- Variáveis de ambiente.
- Verificações.
- Execução inicial.
- Solução de problemas.

### 4.9 `tools-linux.md`
- Ferramentas necessárias.
- Comandos úteis.
- Dependências do sistema.
- Uso recomendado.
- Observações específicas de Linux.

### 4.10 `tools-windows.md`
- Ferramentas necessárias.
- Comandos úteis.
- Dependências do sistema.
- Uso recomendado.
- Observações específicas de Windows.

### 4.11 `.cursorrules`
- Perfil do agente.
- Comportamento esperado.
- Honestidade e bloqueio.
- Regras de resposta.
- Regras de validação.
- Regras de escopo.
- Regras de atualização documental.
- Regras de dados mínimos por resposta.
- Regras de scripts e input.

### 4.12 `spec_template.md`
- Título.
- Objetivo.
- Dependências.
- Escopo.
- Fora de escopo.
- Requisitos.
- Resultado esperado.
- Critérios de aceite.
- Impacto.
- Arquivos afetados.
- Validações.
- Riscos.
- Próxima spec.

### 4.13 `rules_scripts.md`
- Propósito.
- Escopo.
- Limpeza inicial da tela.
- Cabeçalho operacional.
- Organização por categoria macro.
- Descoberta da raiz do repositório.
- Parâmetros mínimos e input interativo.
- Uso de caminhos internos.
- Mensagens e UX operacional.
- Equivalência comportamental entre Linux e Windows.
- Scripts de instalação e desinstalação.
- Atualização documental.
- Regra final.

### 4.14 `docs/`
- Documentação técnica.
- Guias de uso.
- Decisões arquiteturais.
- Referências de implementação.
- Mudanças normativas.

### 4.15 `ideas/`
- Ideias soltas.
- Hipóteses.
- Propostas.
- Rascunhos.
- Explorações ainda não aprovadas.

### 4.16 `specs/`
- Specs formais.
- Cada spec com escopo e critério de aceite.
- Relacionamento explícito com `spec_root.md`.
- Ordem por domínio ou grupo.

### 4.17 `references/`
- Links, estudos, comparativos.
- Material de engenharia reversa.
- Arquivos de apoio e análise.
- Conteúdo consultivo, não normativo.

### 4.18 `scripts/`
- Scripts de setup.
- Scripts de validação.
- Scripts de automação.
- Scripts de manutenção.
- Estrutura por categoria e por sistema operacional.

### 4.19 `reports/`
- Relatórios de implementação.
- Relatórios de validação.
- Relatórios de auditoria.
- Relatórios de entrega.
- Evidências e impacto.

### 4.20 `prompts/`
- Prompts reutilizáveis.
- Colas de bootstrap.
- Prompts de revisão.
- Prompts de grupo e de fluxo.

### 4.21 `resources/`
- Downloads.
- Binários.
- Imagens.
- Apps auxiliares.
- Materiais de apoio.

### 4.22 `core/`
- Código ou conteúdo central do projeto.
- Subpastas específicas do domínio.
- Modelos, schemas, componentes, ativos e dados centrais.
- Tudo que é específico do projeto e não da governança do repositório.

---

## 5. Regras de `.cursorrules`

A `.cursorrules` deve deixar claro, no mínimo, os seguintes pontos:

### 5.1 Comportamento do agente
- Ser objetivo.
- Ser consistente.
- Ser disciplinado com o repositório.
- Não inventar requisitos.
- Não extrapolar escopo.

### 5.2 Honestidade
- Dizer quando não sabe.
- Distinguir fato de suposição.
- Não afirmar validação que não ocorreu.
- Não fingir que entendeu algo que não está documentado.

### 5.3 Dados que a resposta deve mostrar
Toda resposta relevante deve privilegiar:
- o que foi alterado;
- o que foi validado;
- o que ficou pendente;
- quais arquivos foram impactados;
- qual o próximo passo;
- quais documentos justificam a ação.

### 5.4 Leitura obrigatória
Antes de agir, o agente deve ler os documentos-raiz relevantes.

### 5.5 Regras de bloqueio
Se faltar contexto, houver contradição ou escopo indefinido, o agente deve pausar e pedir esclarecimento.

### 5.6 Regras de documentação
Mudanças relevantes devem refletir em documentação, status e timeline.

### 5.7 Regras de scripts de instalação
Todo script de instalação deve suportar, quando aplicável, um parâmetro `--uninstall` que execute a remoção reversa do que o script instalou, preservando o comportamento esperado e evitando efeitos colaterais não documentados.

### 5.8 Regras de input interativo
Sempre que o usuário precisar tomar uma escolha, o script deve exibir uma lista numerada de opções e aguardar que ele digite o número correspondente.

### 5.9 Convenção de escolha
- `0` significa sempre `não`, `false` ou `no`.
- `1` significa sempre `sim`, `true` ou `yes`.
- Pressionar `Enter` sem digitar nada deve selecionar a opção default documentada.
- A entrada deve ser validada antes de continuar.
- Entrada inválida deve gerar novo prompt claro.

---

## 6. Regras de `flow.md`

O `flow.md` deve orientar a sequência de trabalho no repositório.

### Estrutura mínima
1. Ler `spec_root.md`.
2. Ler `rules.md`.
3. Ler `.cursorrules`.
4. Ler `rules_scripts.md` quando a tarefa envolver scripts.
5. Ler `status.md` e `timeline.md` para contexto atual.
6. Ler `specs/` e `docs/` relevantes.
7. Planejar a entrega.
8. Implementar ou documentar somente o escopo confirmado.
9. Validar o que foi feito.
10. Atualizar `status.md`.
11. Atualizar `timeline.md`.
12. Produzir relatório de entrega.
13. Registrar próximos passos.

### Regras
- Não pular leitura obrigatória.
- Não começar implementação sem contexto.
- Não misturar grupos ou temas sem autorização.
- Encerrar cada tarefa com validação e atualização documental.

---

## 7. Regras adicionais para scripts

Todo script de instalação deve oferecer um modo de desinstalação reversa, preferencialmente por `--uninstall` ou equivalente documentado.

### Regras
- O modo de desinstalação deve desfazer exclusivamente as alterações realizadas pelo script.
- O modo de desinstalação deve preservar conteúdo que não foi criado por ele.
- O modo de desinstalação deve falhar de forma segura se não puder reverter algo integralmente.
- Se o script instalar, configurar, registrar ou copiar algo, precisa existir caminho documentado para desfazer isso.
- A reversão deve ser previsível, explícita e segura.

### Regra de input do usuário
Sempre que o usuário precisar tomar uma escolha, o script deve exibir uma lista numerada de opções e aguardar que ele digite o número correspondente.

### Convenção obrigatória de seleção
- `0` significa sempre `não`, `false` ou `no`.
- `1` significa sempre `sim`, `true` ou `yes`.
- Pressionar `Enter` sem digitar nada deve selecionar a opção default documentada.
- O script deve validar a opção escolhida antes de seguir.
- Se a entrada for inválida, o script deve repetir a solicitação de forma clara.

---

## 8. Regras de adaptação por tipo de projeto

### 8.1 Software
Pode incluir `src/`, `tests/`, `build/`, `packages/`, `migrations/`, `api/` e similares dentro de `/core` ou de subestruturas apropriadas.

### 8.2 Hardware
Pode incluir `cad/`, `bom/`, `schematics/`, `firmware/`, `manufacturing/` dentro de `/core`.

### 8.3 Sistema operacional
Pode incluir `profiles/`, `policies/`, `scripts/`, `debs/`, `rpm/`, `services/` dentro de `/core`.

### 8.4 Impressão 3D
Pode incluir `models/`, `slicing/`, `profiles/`, `materials/`, `test-parts/` dentro de `/core`.

### 8.5 Projetos híbridos
Podem combinar estruturas, desde que a raiz documental permaneça consistente e `/core` concentre o conteúdo específico do projeto.

---

## 9. Regras para o Cursor ao criar o repositório

O Cursor deve:

- reconhecer a natureza do projeto;
- criar a raiz documental mínima;
- preencher os arquivos com wireframes adequados ao domínio;
- manter consistência entre `spec_root.md`, `rules.md`, `.cursorrules`, `flow.md` e `rules_scripts.md`;
- não confundir arquivo de visão com arquivo operacional;
- manter `status.md` e `timeline.md` vivos desde o início;
- colocar tudo que é específico do projeto sob `/core` sempre que aplicável.

---

## 10. Critério de completude

Um novo repositório está realmente pronto quando o Cursor consegue responder, sem ambiguidade:

- o que o projeto é;
- quais são as regras;
- como operar;
- como validar;
- como documentar progresso;
- onde ficam as referências;
- onde fica o núcleo específico do projeto;
- como o agente deve se comportar.

---

## 11. Resumo normativo

`spec-root-repo-build.md` deve ser a raiz universal para criação de qualquer novo repositório no Cursor, com estrutura documental completa, wireframes por arquivo, regras de comportamento do agente, honestidade operacional, suporte a scripts reversíveis, regra de input numerado, fluxo de trabalho explícito e centralização do conteúdo específico do projeto em `/core`.
