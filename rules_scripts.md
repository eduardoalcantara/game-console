# rules_scripts.md

## 1. Proposito

Este documento define as regras obrigatorias para criacao, organizacao, manutencao e execucao de scripts no repositorio game-console.

O objetivo e garantir previsibilidade operacional, reduzir erro humano, facilitar execucao a partir de qualquer subpasta localizavel e manter consistencia comportamental entre Linux e Windows.

## 2. Escopo

Estas regras se aplicam a todo script versionado dentro de `./scripts` e a scripts de dominio sob `./core/**/scripts`, incluindo scripts de:

- setup;
- clonagem de referencias;
- manipulacao de repositorio;
- compilacao;
- testes;
- validacao;
- tooling e automacao operacional.

Arquivos documentais em `./scripts` (como notas) nao sao scripts executaveis e ficam na raiz de `./scripts` quando existirem.

## 3. Limpeza inicial da tela

Todo script deve comecar limpando a tela antes de qualquer saida principal.

### Regras

- Em Bash, usar `clear`.
- Em PowerShell, usar `Clear-Host`.
- A limpeza deve ocorrer no inicio do fluxo principal do script.
- Excecoes so sao permitidas quando houver justificativa explicita e documentada no proprio script.

## 4. Cabecalho operacional

Todo script deve exibir um cabecalho imediatamente apos a limpeza da tela e antes de qualquer log, validacao, prompt ou execucao principal.

### Conteudo obrigatorio

- informar que o script pertence ao projeto **game-console**;
- informar qual e a funcao do script (nome curto + descricao objetiva).

### Regras

- O cabecalho deve aparecer no inicio da execucao principal.
- Deve ser curto, legivel e consistente entre Linux e Windows.
- Nao deve ser decorativo em excesso (sem banners elaborados).
- Deve melhorar a UX operacional sem gerar ruido desnecessario.
- Ordem fixa do fluxo inicial: limpar tela → cabecalho → resto da execucao.

### Padrao esperado

```text
game-console
Script: <nome curto do script>
Funcao: <o que o script faz>
----------------------------------------
```

## 5. Organizacao por categoria macro

Todo script na raiz `./scripts` deve ficar em uma subpasta que represente sua categoria macro.

### Categorias previstas

- `setup` — preparacao de ambiente e referencias
- `repo-manipulation` — futura
- `compilation` — futura
- `tests` — futura
- `validation` — futura
- `tooling` — futura

### Regras

- Nao criar scripts soltos diretamente em `./scripts`, exceto arquivos documentais.
- A categoria deve refletir a responsabilidade principal do script.
- Nomes de categoria em ingles, curtos, minusculos e objetivos.
- Se houver versao por sistema operacional, ela deve ficar abaixo da categoria: `categoria/linux` e `categoria/windows`.
- A organizacao deve ser previsivel e equivalente entre Linux e Windows.
- Nao criar pastas de categoria futuras ate existir script real para elas.
- Scripts especificos de um alvo de dominio podem viver sob `core/<alvo>/scripts/` sem exigir categoria macro da raiz; ainda assim devem cumprir limpeza, cabecalho, raiz, input e `--uninstall` quando aplicavel.

### Estrutura canonica (quando houver scripts na raiz)

```text
./scripts/
  setup/
    linux/
      exemplo.sh
    windows/
      exemplo.ps1
```

## 6. Descoberta do caminho do repositorio

Todo script deve verificar de onde esta sendo executado e localizar a raiz do repositorio antes de operar em arquivos do projeto.

### Regra central

Os scripts devem assumir que o nome da pasta raiz do repositorio e:

`game-console`

### Requisitos obrigatorios

- O script deve detectar o diretorio atual de execucao e/ou o diretorio do proprio script.
- O script deve localizar a raiz `game-console`, mesmo quando executado a partir de subpastas.
- O script deve definir explicitamente uma variavel de caminho para a raiz do repositorio.
- Todos os caminhos internos usados pelo script devem derivar dessa variavel.
- O script nao deve depender implicitamente de "estar no diretorio certo".

### Convencao de variavel

- Bash: `REPO_ROOT`
- PowerShell: `$RepoRoot`

### Regra de falha

Se a raiz do repositorio nao puder ser localizada com seguranca, o script deve abortar imediatamente com mensagem clara de erro (sem continuar com caminhos frageis).

## 7. Parametros minimos e input interativo

Os scripts devem funcionar com a menor quantidade possivel de parametros obrigatorios.

### Regras

- Sempre preferir defaults seguros quando a decisao puder ser inferida com seguranca.
- Quando um parametro obrigatorio nao for informado, o script deve solicitar esse valor via input interativo ao usuario.
- O script deve validar a entrada antes de continuar.
- O script deve exibir mensagens objetivas, claras e curtas ao pedir input.
- O script nao deve falhar silenciosamente por ausencia de parametro obrigatorio.
- Parametros opcionais podem manter default documentado sem prompt.

### Regra adicional de escolha do usuario

Sempre que o usuario precisar tomar uma escolha, o script deve exibir uma lista numerada de opcoes e aguardar que ele digite o numero correspondente.

### Convencao obrigatoria de selecao

- `0` significa sempre `nao`, `false` ou `no`.
- `1` significa sempre `sim`, `true` ou `yes`.
- Pressionar `Enter` sem digitar nada deve selecionar a opcao default documentada.
- O script deve validar a opcao escolhida antes de seguir.
- Se a entrada for invalida, o script deve repetir a solicitacao de forma clara.

## 8. Uso de caminhos internos

Todo acesso a arquivos e diretorios do repositorio deve usar caminhos construidos a partir da variavel da raiz do repo.

### Regras

- Proibido hardcode de caminhos relativos frageis como `../../..` ao longo do script inteiro.
- E permitido caminhar a arvore de diretorios apenas para descobrir `REPO_ROOT` / `$RepoRoot`.
- Apos isso, todo uso deve derivar da variavel raiz.
- Scripts devem funcionar independentemente do diretorio corrente do usuario, desde que a raiz `game-console` seja localizavel.

## 9. Mensagens e UX operacional

Os scripts devem ter comportamento previsivel e amigavel.

### Regras

- Informar claramente o que sera feito antes de executar acoes relevantes.
- Informar erros com contexto suficiente.
- Evitar output ruidoso desnecessario.
- Sempre que possivel, imprimir ao final:
  - acao concluida;
  - diretorio raiz detectado;
  - arquivos ou areas afetadas.

## 10. Equivalencia comportamental entre Linux e Windows

Quando um script tiver versoes para Linux e Windows:

- ambos devem seguir a mesma intencao operacional;
- diferencas de sintaxe nao devem gerar diferencas de comportamento desnecessarias;
- nomes, inputs e mensagens devem ser mantidos o mais equivalentes possivel;
- a estrutura de pastas `categoria/linux` e `categoria/windows` deve permanecer simetrica.

## 11. Scripts de instalacao e desinstalacao

Todo script de instalacao deve oferecer um modo de desinstalacao reversa, preferencialmente por `--uninstall` ou equivalente documentado.

### Regras

- O modo de desinstalacao deve desfazer exclusivamente as alteracoes realizadas pelo script.
- O modo de desinstalacao deve preservar conteudo que nao foi criado por ele.
- O modo de desinstalacao deve falhar de forma segura se nao puder reverter algo integralmente.
- Se o script instalar, configurar, registrar ou copiar algo, precisa existir caminho documentado para desfazer isso.
- A reversao deve ser previsivel, explicita e segura.

## 12. Atualizacao documental

Sempre que uma nova convencao estrutural de scripts for adotada ou alterada:

- avaliar impacto em `setup.md`;
- avaliar impacto em `tools-linux.md` e `tools-windows.md`;
- atualizar `status.md`;
- registrar a mudanca em `timeline.md`.

## 13. Regra final

Nenhum script novo deve ser adicionado ao repositorio se:

- estiver fora de uma categoria macro adequada (quando sob `./scripts`);
- depender de execucao manual a partir de um diretorio especifico sem autodeteccao da raiz;
- exigir parametros obrigatorios sem fallback interativo;
- omitir limpeza de tela ou cabecalho operacional no inicio;
- contrariar estas regras sem justificativa explicita.
