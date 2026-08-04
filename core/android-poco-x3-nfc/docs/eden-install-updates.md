# Eden — instalar atualizacao NSP de um jogo

Tutorial operacional deste repositorio. Alvo validado: **Eden Android** no Razr 50 Ultra (`dev.eden.eden_emulator`), com a arvore sob `/storage/emulated/0/game-console/`.

Objetivo: aplicar um arquivo **update** (`.nsp`) ao jogo **base** ja reconhecido pelo Eden, sem listar o update como jogo no ES-DE.

## Premissas

1. Keys e firmware ja configurados no Eden (smoke test anterior OK).
2. Jogo **base** em:

   `game-console/ROMs/switch/<Nome do Jogo>.nsp`

3. Arquivo de **atualizacao** em:

   `game-console/ROMs/switch/updates/<Nome do Jogo>.nsp`

4. O update pertence ao **mesmo jogo** (mesmo Title ID de base / mesma regiao). O Eden identifica isso pelo conteudo interno do NSP — o nome do arquivo nao precisa ter `[UPD]` nem Title ID.

Convencao de pastas: `rom-layout.md` (secao Switch — base vs updates).

## O que nao fazer

- Nao abrir o NSP de update pelo carrossel do **ES-DE** (ele aparece como “jogo” e nao e o fluxo correto).
- Nao substituir o arquivo base pelo update na pasta `ROMs/switch/`.
- Nao misturar update de outra regiao / outro Title ID com o base.

## Procedimento (Android — Eden)

### 1. Confirmar pastas

No gerenciador de arquivos do aparelho:

```text
/storage/emulated/0/game-console/ROMs/switch/            <- so bases
/storage/emulated/0/game-console/ROMs/switch/updates/    <- so UPD (e DLC, se houver)
```

Exemplo (Mario Kart 8 Deluxe):

| Papel | Caminho |
|---|---|
| Base | `.../ROMs/switch/Mario Kart 8 Deluxe.nsp` |
| Update | `.../ROMs/switch/updates/Mario Kart 8 Deluxe.nsp` |

### 2. Abrir o Eden

Abra o app **Eden**. Espere a biblioteca carregar. O jogo base deve aparecer na lista (pasta de jogos apontando para `game-console/ROMs/switch` ou apos adicionar o diretorio / o arquivo base).

### 3. Instalar o update na NAND virtual

O update **nao** fica “ao lado” do base como segundo jogo. Ele e **instalado** na NAND do Eden.

Passos tipicos neste build (rotulos podem variar levemente entre versoes):

1. Na tela principal do Eden, abra o menu de arquivos / conteudo (icone de menu ou equivalente a **File**).
2. Escolha **Install Files to NAND** (ou **Install Content to NAND** / **Install to NAND**).
3. No seletor de arquivos do Android, navegue ate:

   `Armazenamento interno` → `game-console` → `ROMs` → `switch` → `updates`

4. Selecione o `.nsp` de atualizacao do jogo.
5. Confirme e **aguarde** o fim da instalacao (nao force o fechamento do app).
6. Quando aparecer sucesso, feche o Eden por completo (force stop se necessario) e abra de novo.

**Alternativa em alguns builds:** toque longo na capa do jogo base → opcao de instalar conteudo / add-ons → escolher o NSP em `updates/`.

### 4. Verificar

1. Toque longo (ou menu) no jogo base → **Properties** / **Info**.
2. Confira se a **versao** do jogo subiu (nao permanece em `1.0.0` / v0 se o update era mais novo).
3. Inicie o jogo pelo Eden (ou pelo ES-DE apontando para o **base**).

Se a versao nao mudou: o update nao foi aplicado (arquivo errado, instalacao incompleta, ou firmware/keys insuficientes para aquele patch).

## Ordem quando houver DLC

1. Jogo base (ja na pasta / ja listado).
2. **Update** (Install to NAND).
3. **DLC** (mesmo fluxo Install to NAND, um arquivo por vez).
4. Reiniciar o Eden.

Muitos DLCs exigem o jogo ja na versao do update.

## Relacao com o ES-DE

| Onde | O que fica |
|---|---|
| `ROMs/switch/` | So o NSP **base** — o ES-DE lista e lanca isto |
| `ROMs/switch/updates/` | UPD/DLC — **nao** para o carrossel; so para Install to NAND no Eden |
| NAND do Eden | Conteudo ja instalado (update/DLC) — o jogo “enxerga” ao abrir o base |

O ES-DE 3.4.1-58 ja mapeia `switch` → **Eden (Standalone)**. Ele so precisa do base; o update ja instalado na NAND acompanha.

## Push a partir do PC (quando o aparelho estiver no ADB)

Apos organizar no repo (`resources/roms/switch/` e `.../updates/`):

```bash
adb shell mkdir -p /storage/emulated/0/game-console/ROMs/switch/updates
adb push "resources/roms/switch/<Jogo>.nsp" /storage/emulated/0/game-console/ROMs/switch/
adb push "resources/roms/switch/updates/<Jogo>.nsp" /storage/emulated/0/game-console/ROMs/switch/updates/
```

Depois execute os passos 2–4 neste tutorial no aparelho.

## Problemas comuns

| Sintoma | Causa provavel | O que fazer |
|---|---|---|
| Erro ao instalar / encryption | Keys ausentes ou desatualizadas | Conferir `prod.keys` / `title.keys` na pasta keys do Eden |
| Install falha apos keys OK | Firmware antigo demais para o patch | Reinstalar firmware (`firmware.zip`) compativel |
| Versao do jogo nao sobe | NSP errado ou instalacao cancelada | Confirmar Title ID / arquivo em `updates/`; reinstalar |
| ES-DE mostra dois “jogos” | Update ainda na pasta base | Mover UPD para `updates/` e fazer rescan |
| Jogo abre mas crasha com DLC | Update nao instalado antes do DLC | Instalar update, depois DLC, reiniciar Eden |

## Relacionados

- `rom-layout.md` — convencao `switch/` vs `switch/updates/`
- `stage-razr-50-ultra-test.md` — contexto da bancada Razr
- `setup-adb.md` — raiz `game-console/` e ADB
- `tools-android.md` — `adb` no PATH

## Escopo

Procedimento da bancada **Razr + Eden**. Nao faz parte do escopo permanente do Poco X3 NFC (`rules.md` / `spec_root.md`: sem Switch no Poco).
