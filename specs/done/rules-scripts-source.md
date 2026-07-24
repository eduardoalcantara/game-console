# rules_scripts.md

## 1. Propósito

Este documento define as regras obrigatórias para criação, organização, manutenção e execução de scripts no repositório RustForge.

O objetivo é garantir previsibilidade operacional, reduzir erro humano, facilitar execução a partir de qualquer subpasta localizável e manter consistência comportamental entre Linux e Windows.

---

## 2. Escopo

Estas regras se aplicam a todo script versionado dentro de `./scripts`, incluindo scripts de:
- setup;
- clonagem de referências;
- manipulação de repositório;
- compilação;
- testes;
- validação;
- tooling e automação operacional.

Arquivos documentais em `./scripts` (como este) não são scripts executáveis e ficam na raiz de `./scripts`.

---

## 3. Limpeza inicial da tela

Todo script deve começar limpando a tela antes de qualquer saída principal.

### Regras
- Em Bash, usar `clear`.
- Em PowerShell, usar `Clear-Host`.
- A limpeza deve ocorrer no início do fluxo principal do script.
- Exceções só são permitidas quando houver justificativa explícita e documentada no próprio script.

---

## 4. Cabeçalho operacional

Todo script deve exibir um cabeçalho imediatamente após a limpeza da tela e antes de qualquer log, validação, prompt ou execução principal.

### Conteúdo obrigatório
- informar que o script pertence ao projeto **RustForge**;
- informar qual é a função do script (nome curto + descrição objetiva).

### Regras
- O cabeçalho deve aparecer no início da execução principal.
- Deve ser curto, legível e consistente entre Linux e Windows.
- Não deve ser decorativo em excesso (sem banners elaborados).
- Deve melhorar a UX operacional sem gerar ruído desnecessário.
- Ordem fixa do fluxo inicial: limpar tela → cabeçalho → resto da execução.

### Padrão esperado
```text
RustForge
Script: <nome curto do script>
Função: <o que o script faz>
----------------------------------------
```

---

## 5. Organização por categoria macro

Todo script deve ficar em uma subpasta que represente sua categoria macro dentro de `./scripts`.

### Categorias previstas
- `setup` — preparação de ambiente e referências (existente)
- `repo-manipulation` — futura
- `compilation` — futura
- `tests` — futura
- `validation` — futura
- `tooling` — futura

### Regras
- Não criar scripts soltos diretamente em `./scripts`, exceto arquivos documentais como este.
- A categoria deve refletir a responsabilidade principal do script.
- Nomes de categoria em inglês, curtos, minúsculos e objetivos.
- Se houver versão por sistema operacional, ela deve ficar abaixo da categoria: `categoria/linux` e `categoria/windows`.
- A organização deve ser previsível e equivalente entre Linux e Windows.
- Não criar pastas de categoria futuras até existir script real para elas.

### Estrutura canônica
```text
./scripts/
  rules_scripts.md
  setup/
    linux/
      setup-references.sh
    windows/
      setup-references.ps1
```

---

## 6. Descoberta do caminho do repositório

Todo script deve verificar de onde está sendo executado e localizar a raiz do repositório antes de operar em arquivos do projeto.

### Regra central
Os scripts devem assumir que o nome da pasta raiz do repositório é:

`rustforge`

### Requisitos obrigatórios
- O script deve detectar o diretório atual de execução e/ou o diretório do próprio script.
- O script deve localizar a raiz `rustforge`, mesmo quando executado a partir de subpastas.
- O script deve definir explicitamente uma variável de caminho para a raiz do repositório.
- Todos os caminhos internos usados pelo script devem derivar dessa variável.
- O script não deve depender implicitamente de “estar no diretório certo”.

### Convenção de variável
- Bash: `REPO_ROOT`
- PowerShell: `$RepoRoot`

### Regra de falha
Se a raiz do repositório não puder ser localizada com segurança, o script deve abortar imediatamente com mensagem clara de erro (sem continuar com caminhos frágeis).

---

## 7. Parâmetros mínimos e input interativo

Os scripts devem funcionar com a menor quantidade possível de parâmetros obrigatórios.

### Regras
- Sempre preferir defaults seguros quando a decisão puder ser inferida com segurança.
- Quando um parâmetro obrigatório não for informado, o script deve solicitar esse valor via input interativo ao usuário.
- O script deve validar a entrada antes de continuar.
- O script deve exibir mensagens objetivas, claras e curtas ao pedir input.
- O script não deve falhar silenciosamente por ausência de parâmetro obrigatório.
- Parâmetros opcionais podem manter default documentado sem prompt (não forçar pergunta desnecessária).

### Regra adicional de escolha do usuário
Sempre que o usuário precisar tomar uma escolha, o script deve exibir uma lista numerada de opções e aguardar que ele digite o número correspondente.

### Convenção obrigatória de seleção
- `0` significa sempre `não`, `false` ou `no`.
- `1` significa sempre `sim`, `true` ou `yes`.
- Pressionar `Enter` sem digitar nada deve selecionar a opção default documentada.
- O script deve validar a opção escolhida antes de seguir.
- Se a entrada for inválida, o script deve repetir a solicitação de forma clara.

### Regra de UX
A lista de opções deve ser curta, objetiva e legível, sem ambiguidade sobre qual número representa cada escolha.

### Exemplo de comportamento esperado
- confirmação simples: `0 = no`, `1 = yes`, `Enter = default`;
- escolha entre modos: lista numerada com default documentado;
- escolha obrigatória: usuário deve informar um número válido.

---

## 8. Uso de caminhos internos

Todo acesso a arquivos e diretórios do repositório deve usar caminhos construídos a partir da variável da raiz do repo.

### Regras
- Proibido hardcode de caminhos relativos frágeis como `../../..` ao longo do script inteiro.
- É permitido caminhar a árvore de diretórios apenas para descobrir `REPO_ROOT` / `$RepoRoot`.
- Após isso, todo uso deve derivar da variável raiz.
- Scripts devem funcionar independentemente do diretório corrente do usuário, desde que a raiz `rustforge` seja localizável.

---

## 9. Mensagens e UX operacional

Os scripts devem ter comportamento previsível e amigável.

### Regras
- Informar claramente o que será feito antes de executar ações relevantes.
- Informar erros com contexto suficiente.
- Evitar output ruidoso desnecessário.
- Sempre que possível, imprimir ao final:
  - ação concluída;
  - diretório raiz detectado;
  - arquivos ou áreas afetadas.

---

## 10. Equivalência comportamental entre Linux e Windows

Quando um script tiver versões para Linux e Windows:
- ambos devem seguir a mesma intenção operacional;
- diferenças de sintaxe não devem gerar diferenças de comportamento desnecessárias;
- nomes, inputs e mensagens devem ser mantidos o mais equivalentes possível;
- a estrutura de pastas `categoria/linux` e `categoria/windows` deve permanecer simétrica.

---

## 11. Scripts de instalação e desinstalação

Todo script de instalação deve oferecer um modo de desinstalação reversa, preferencialmente por `--uninstall` ou equivalente documentado.

### Regras
- O modo de desinstalação deve desfazer exclusivamente as alterações realizadas pelo script.
- O modo de desinstalação deve preservar conteúdo que não foi criado por ele.
- O modo de desinstalação deve falhar de forma segura se não puder reverter algo integralmente.
- Se o script instalar, configurar, registrar ou copiar algo, precisa existir caminho documentado para desfazer isso.
- A reversão deve ser previsível, explícita e segura.

---

## 12. Atualização documental

Sempre que uma nova convenção estrutural de scripts for adotada ou alterada:
- avaliar impacto em `setup.md`;
- avaliar impacto em `tools-linux.md` e `tools-windows.md`;
- atualizar `status.md`;
- registrar a mudança em `timeline.md`.

---

## 13. Regra final

Nenhum script novo deve ser adicionado ao repositório se:
- estiver fora de uma categoria macro adequada;
- depender de execução manual a partir de um diretório específico sem autodetecção da raiz;
- exigir parâmetros obrigatórios sem fallback interativo;
- omitir limpeza de tela ou cabeçalho operacional no início;
- contrariar estas regras sem justificativa explícita.
