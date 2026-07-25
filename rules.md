# rules.md

## 1. Hierarquia normativa

1. `spec_root.md` (autoridade arquitetural)
2. `.cursorrules` (comportamento do agente)
3. `rules.md` e `rules_scripts.md` (governanca permanente)
4. `flow.md` (ordem operacional)
5. Specs em `specs/` (requisitos formais de entrega)
6. `status.md` / `timeline.md` (estado e historico; nao sobrepoem regras)

Em conflito, prevalece o nivel mais alto. Se a contradicao persistir, pausar e pedir esclarecimento.

## 2. Regras gerais permanentes

- Ser objetivo, consistente e disciplinado com o repositorio.
- Nao inventar requisitos.
- Nao extrapolar escopo.
- Distinguir fato de suposicao.
- Conteudo especifico do dominio vive sob `/core`.

## 3. Regras de escopo

- Android: limitar a sistemas 8-bit ate PS1, N64 e PSP. Sem Switch/PS2 no Poco X3 NFC.
- Windows 11: Ryujinx, ES-DE, Blur e dependencias documentadas.
- Linux Ubuntu 26: Flatpak para emuladores; Lutris/Proton para PC games.

## 4. Regras de qualidade

- UTF-8 sem BOM.
- Sem emojis em nomes de arquivos ou dentro de scripts.
- Documentacao clara, sem ruido.
- Scripts previsiveis e com falha segura.

## 5. Regras de documentacao

- Mudancas relevantes refletem em `status.md` e `timeline.md`.
- Entregas formais produzem relatorio em `reports/`.
- Specs novas usam `spec_template.md`.

## 6. Regras de validacao

- Validar estrutura, nomes e consistencia documental.
- Nao afirmar que um host foi configurado se o script nao foi executado la.
- Evidencias de validacao vao para `reports/` quando formal.

## 7. Regras de bloqueio

Pausar e pedir esclarecimento quando:

- faltar contexto;
- houver contradicao entre documentos;
- o escopo estiver indefinido;
- a acao puder destruir dados sem caminho de reversao documentado.

## 8. Regras de atualizacao

- Apos mudanca estrutural de scripts: avaliar `setup.md`, `tools-linux.md`, `tools-windows.md`.
- Apos entrega: atualizar status e timeline no mesmo ciclo.
- Manter `readme.md` alinhado ao proposito e estado.
