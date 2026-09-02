# Guia do operador — RG43H PRO (EmuELEC / RGBox)

Notas praticas para o aparelho com o SD curado (FAT32, rotulo **EEROMS**).
Firmware observado: **EmuELEC 4.7 + RGBox**; SO no storage interno; SD = biblioteca de ROMs.

---

## 1. Salvar e restaurar progresso

Existem **dois** mecanismos. Nao sao equivalentes.

### 1.1 Save do proprio jogo (SRAM / battery)

O save “oficial” do cartucho (Zelda, Chrono Trigger, Super Metroid, etc.).

**Salvar**

1. No jogo, usar o menu normal (Save / Save Game / Save Point).
2. Sair do jogo com o atalho de quit (ver abaixo); evitar desligar a meio.

**Restaurar**

1. Abrir o **mesmo** ficheiro ROM.
2. No menu do jogo: Continue / Load.

Esse save fica associado ao ROM. No EmuELEC costuma residir no **storage interno** (nao necessariamente na pasta do jogo no SD).

### 1.2 Savestate (estado da emulacao)

Congela o jogo no instante exacto (meio de fase, boss, etc.). E o metodo mais usado em handhelds.

Hotkeys tipicas do RetroArch no EmuELEC (hotkey = **SELECT**):

| Accao | Comando |
|---|---|
| **Salvar estado** | **SELECT + R1** (ombro direito) |
| **Carregar estado** | **SELECT + L1** (ombro esquerdo) |
| Mudar slot (0, 1, 2…) | **SELECT + ← / →** |
| Menu RetroArch | **SELECT + X** (ou botao Menu, conforme firmware) |
| Sair do jogo | **SELECT + START** |

**Fluxo**

1. Jogar ate ao ponto desejado.
2. **SELECT + R1** → grava o estado.
3. Mais tarde: abrir o mesmo jogo → **SELECT + L1**.

Se SELECT+R1 nao fizer nada: abrir o menu RetroArch → **Settings → Input → Hotkeys** e confirmar Save State / Load State.

### 1.3 Qual usar?

| Situacao | Preferir |
|---|---|
| RPG / jogo com save proprio | Save do jogo (+ savestate como backup) |
| Fase dificil / “continuar ja” | Savestate |
| Trocar / formatar SD | Cuidado: saves e savestates podem ficar no **interno**, nao so no cartao EEROMS |

Savestate de outro core/versao do emulador pode falhar. Nao e backup portavel garantido entre firmwares.

Pastas tipicas no SD original: `savestates/`, `screenshots/` na raiz EEROMS (conforme build).

---

## 2. Capas e metadados (scrape no launcher)

O launcher e o **EmulationStation** (tema RGBox). Capas e descricoes vêm do **scraper** online.

No SD curado v1, muitos sistemas (especialmente **SNES**) ficaram sem `gamelist.xml` / `images/` filtrados — as ROMs jogam, mas a grelha pode aparecer sem capa.

### 2.1 Se o menu START nao mostra "Scraper" (caso RG43H / RGBox)

No aparelho AISLPC RG43H o menu START tipico e:

```text
EmuELEC Settings
Game Settings
User Interface Settings
Controllers
Sound Settings
Network Settings
Game Collection Settings
System Settings
```

**Nao aparece "Scraper"** neste build — e esperado em algumas builds RGBox / UI Mode restrito.
Nao inventar que o item existe: usar um dos caminhos abaixo.

#### Caminho A — Desbloquear UI Mode (pode revelar Scraper)

No menu em **portugues**, os rotulos variam. Procurar isto:

| Ingles | Portugues (pt_BR / pt tipico) |
|---|---|
| User Interface Settings | **Configuracoes da Interface** / Interface do usuario |
| UI Mode | **Modo da Interface** / Modo da UI / Modo de interface |
| Full | **Completo** |
| Kiosk | **Quiosque** |
| Kid | **Crianca** |
| Unlock User Interface Mode | **Desbloquear modo da interface** |
| Scraper | **Extrator** / **Scraper** / **Raspar** / **Baixar midia** |
| Update Game Lists | **Atualizar listas de jogos** |
| Edit this game's metadata | **Editar metadados deste jogo** |
| Scrape (botao) | **Extrair** / **Raspar** / **Scrape** |

No RG43H (menu que o operador reportou), **nao ha item "Modo da Interface"** nem "Scraper"/"Extrator" no START. E um comportamento tipico de builds **RGBox** (menu reduzido), nao necessariamente UI Kid/Kiosk.

Se nao encontrares "Modo da Interface" dentro de **Configuracoes da Interface**: **saltar o Caminho A** — nao existe neste build. Ir para o Caminho B.

#### Caminho B — Scrape jogo a jogo (caminho principal no RG43H)

1. Wi‑Fi ligado: START → **Rede** / Network Settings.
2. Entrar no sistema (ex.: SNES).
3. Destacar um jogo na lista.
4. Premir **SELECT** (botao Select do comando — **nao** e START).
5. No menu do jogo, escolher:
   - **Editar metadados deste jogo**, ou
   - **Editar este jogo**, ou
   - **Informacoes** / **Metadados**
6. No ecran de edicao, em baixo: **Extrair** / **Raspar** / **Scrape** / botao **Y**.
7. Escolher o resultado correcto → gravar/voltar.
8. START → **Configuracoes de Jogos** → **Atualizar listas de jogos**.

Se no SELECT **nao** aparecer nenhuma opcao de metadados/editar, o launcher RGBox pode ter desactivado a edicao. Nesse caso: Caminho D (capas no PC).

#### Achado no aparelho (2026-08-31, operador)

No RG43H Pro (RGBox, UI em portugues):

- Menu START **sem** Extrator/Scraper e **sem** Modo da Interface.
- **SELECT** no jogo so mostra opcoes de **aleatoriedade** e **pormenores** — **nao** ha "Editar metadados" nem scrape individual.

Conclusao: neste firmware o scrape **no aparelho nao esta disponivel** (menu reduzido / metadados bloqueados). Nao insistir em UI Mode nem SELECT→Scrape.

**Caminho valido:** Caminho D — capas e metadados no PC → copiar para o SD.

#### Caminho C — Procurar dentro de Game Settings / EmuELEC Settings

Em algumas builds o scrape esta aninhado:

- START → **Game Settings** — procurar Scrape / Download media / Update Game Lists.
- START → **EmuELEC Settings** — procurar Scrapers / Tools / Download.

Se encontrares um item com nome diferente (ex.: chines/ingles misturado), anotar o rotulo exacto para actualizar este guia.

#### Caminho D — Offline no PC (caminho suportado neste RGBox)

Script: `scripts/tooling/apply_esde_media_rg43h.py`

Copia capas de `resources/es-de/downloaded_media/` para
`resources/rg43h/staging/<sistema>/images/` e gera `gamelist.xml`.

```bash
python scripts/tooling/apply_esde_media_rg43h.py              # dry-run
python scripts/tooling/apply_esde_media_rg43h.py --execute --yes
python scripts/tooling/apply_esde_media_rg43h.py --execute --yes --deploy H:\
python scripts/tooling/apply_esde_media_rg43h.py --uninstall --execute --yes
```

Preferencia de imagem: covers > miximages > screenshots > 3dboxes > titlescreens > marquees.

**Importante:** se o Google Drive so sincronizou pastas A–E, muitas capas faltam.
Marcar `resources/es-de/downloaded_media/` como disponivel offline e reexecutar.

Relatorio: `reports/2026-08-31-rg43h-esde-media.md` / `staging/media-report.md`.

### 2.2 Pre-requisitos (qualquer caminho)

1. **Wi‑Fi ligado** — START → Network Settings → Connected.
2. Conta **ScreenScraper** (opcional): [screenscraper.fr](https://www.screenscraper.fr/) — ajuda se o bulk scraper existir.
3. Depois de qualquer scrape: START → **Game Settings** → **Update Game Lists** / Actualizar listas.

### 2.3 Se o menu Scraper existir (EmuELEC stock)

1. START → **Scraper** (scroll se necessario).
2. **Scrape From:** ScreenScraper.
3. Sistemas: so o actual (ex. SNES); jogos: missing image.
4. **Scrape Now**.
5. Game Settings → **Update Game Lists**.

### 2.4 Onde ficam os ficheiros

| Conteudo | Local aproximado |
|---|---|
| Metadados | `gamelist.xml` na pasta do sistema no SD |
| Imagens | `<sistema>/images/` ou media do ES no storage |

### 2.5 Problemas comuns

| Sintoma | Accao |
|---|---|
| Sem item Scraper no START | UI Mode Full (2.1 A); ou scrape por SELECT (2.1 B); ou offline (2.1 D) |
| SELECT no jogo nao mostra Edit metadata | UI Mode Kid/Kiosk — desbloquear |
| Capas nao aparecem apos scrape | Game Settings → Update Game Lists |
| Sem Wi‑Fi | Network Settings |
| ScreenScraper busy | Tentar mais tarde |
| Tema sem capa mas XML tem dados | Tema pede screenshot vs box — mudar tipo de media |

---

## 3. Checklist rapido (operador)

- [ ] Wi‑Fi ligado (so se scrape no aparelho existir — neste RGBox **nao**)
- [ ] Confirmado: SELECT = aleatoriedade/pormenores; **sem** editar metadados (2026-08-31)
- [ ] Usar capas do PC: `resources/es-de/downloaded_media/` → SD (fase 2)
- [ ] Testar save do jogo + SELECT+R1 / SELECT+L1
- [ ] Smoke test outros sistemas

---

## Referencias

- Analise SD: `reports/2026-08-30-rg43h-sd-analysis.md`
- Curadoria / deploy: `reports/2026-08-30-rg43h-curate-deploy.md`
- Plano: `resources/rg43h/docs/curation-plan.md`
- ScreenScraper: https://www.screenscraper.fr/
- Nota: builds **RGBox** no RG43H podem omitir o item Scraper do menu START; o caminho SELECT → metadata → Scrape e o fallback oficial do EmulationStation.
