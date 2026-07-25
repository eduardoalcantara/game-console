# Setup ADB — caminho primario (Android)

Fluxo unico para preparar o ambiente: primeiro no **celular** (Poco X3 NFC), depois no **tablet** (mesmo procedimento; registrar o modelo do tablet na checklist quando conhecido).

Pre-requisito: APKs e BIOS arquivados conforme `resources-inventory.md`. Layout de ROMs: `rom-layout.md`.

## 1. Pre-requisitos

No PC:

- Android platform-tools instalado (`adb` no PATH). Ver `tools-android.md`.
- Cabo USB de dados.
- APKs em `resources/android/apk/` (ES-DE, RetroArch AArch64, DuckStation).

No aparelho:

- Opcoes do desenvolvedor ativadas.
- Depuracao USB ativada.
- Autorizar o PC na caixa de dialogo do aparelho na primeira conexao.
- Se necessario: permitir instalacao de apps de fontes desconhecidas / via ADB (conforme a versao do MIUI/HyperOS).

## 2. Conferencia do dispositivo

```bash
adb devices
adb shell getprop ro.product.model
adb shell getprop ro.product.cpu.abi
```

Esperado no celular:

- modelo: POCO X3 NFC (ou equivalente reportado pelo firmware);
- ABI: `arm64-v8a`.

Se houver mais de um dispositivo: `adb -s <serial> ...` ou desconecte o outro.

Estado `unauthorized`: revogue autorizacoes USB no aparelho, reconecte e aceite novamente.

## 3. Criar arvore de pastas ES-DE

```bash
adb shell mkdir -p /storage/emulated/0/ROMs/atari2600
adb shell mkdir -p /storage/emulated/0/ROMs/atarilynx
adb shell mkdir -p /storage/emulated/0/ROMs/wonderswan
adb shell mkdir -p /storage/emulated/0/ROMs/gb
adb shell mkdir -p /storage/emulated/0/ROMs/gbc
adb shell mkdir -p /storage/emulated/0/ROMs/gba
adb shell mkdir -p /storage/emulated/0/ROMs/nes
adb shell mkdir -p /storage/emulated/0/ROMs/snes
adb shell mkdir -p /storage/emulated/0/ROMs/mastersystem
adb shell mkdir -p /storage/emulated/0/ROMs/megadrive
adb shell mkdir -p /storage/emulated/0/ROMs/pcengine
adb shell mkdir -p /storage/emulated/0/ROMs/neogeo
adb shell mkdir -p /storage/emulated/0/ROMs/mame
adb shell mkdir -p /storage/emulated/0/ROMs/psx
adb shell mkdir -p /storage/emulated/0/Games/BIOS
```

## 4. Instalar APKs (ordem)

A partir da raiz do repositorio `game-console`:

```bash
adb install -r resources/android/apk/retroarch-aarch64-1.22.2.apk
adb install -r resources/android/apk/ES-DE_3.4.1-58.apk
```

DuckStation: se houver APK local:

```bash
adb install -r resources/android/apk/duckstation-android.apk
```

Se o APK oficial estiver indisponivel (situacao em 2026-07-24), instalar DuckStation pela Play Store no aparelho e seguir com o restante via ADB.

Ordem sugerida: RetroArch → DuckStation (APK ou loja) → ES-DE.

### RetroArch ja instalado pela Play Store

Desinstalar a build da loja antes do APK oficial. Assinaturas diferentes geram `INSTALL_FAILED_UPDATE_INCOMPATIBLE`.

```bash
adb uninstall com.retroarch.aarch64
# ou o package id da build instalada; confirmar com pm list packages
```

## 5. Verificar pacotes

```bash
adb shell pm list packages | findstr /i "retroarch duckstation es_de es-de"
```

Em Linux/macOS, use `grep -i` no lugar de `findstr`.

Pacotes tipicos (podem mudar entre releases):

| App | Package id de referencia |
|---|---|
| RetroArch AArch64 | `com.retroarch.aarch64` |
| DuckStation | `com.github.stenzek.duckstation` |
| ES-DE | `org.es_de.frontend` (ou variante Galaxy Store; confirmar no aparelho) |

Se o id divergir, registrar o valor real em `reports/` / checklist.

## 6. Enviar BIOS e ROMs

BIOS (exemplo):

```bash
adb push resources/android/bios/SCPH1001.BIN /storage/emulated/0/Games/BIOS/
```

ROMs: usar **somente** o espelho Android `resources/roms/android/`, ja com nomes canonicos ES-DE (ver `rom-layout.md`). A faixa `resources/roms/pc-only/` nao entra neste fluxo.

A partir da raiz do repositorio:

```bash
adb push resources/roms/android/gb/. /storage/emulated/0/ROMs/gb/
adb push resources/roms/android/gbc/. /storage/emulated/0/ROMs/gbc/
adb push resources/roms/android/gba/. /storage/emulated/0/ROMs/gba/
adb push resources/roms/android/nes/. /storage/emulated/0/ROMs/nes/
adb push resources/roms/android/snes/. /storage/emulated/0/ROMs/snes/
adb push resources/roms/android/mastersystem/. /storage/emulated/0/ROMs/mastersystem/
adb push resources/roms/android/megadrive/. /storage/emulated/0/ROMs/megadrive/
adb push resources/roms/android/pcengine/. /storage/emulated/0/ROMs/pcengine/
adb push resources/roms/android/neogeo/. /storage/emulated/0/ROMs/neogeo/
adb push resources/roms/android/mame/. /storage/emulated/0/ROMs/mame/
```

Nao enviar neste passo:

- `resources/roms/pc-only/` (dos, wii, ps2, switch)
- pastas Android vazias (`atari2600`, `atarilynx`, `wonderswan`, `psx`)

Scoped storage: se o push falhar por permissao, liberar acesso a pastas no aparelho (Files / permissao do ES-DE e dos emuladores) e repetir.

## 7. Pos-install manual (no aparelho)

ADB nao substitui o first-run nem a calibracao ergonômica na GUI. No aparelho:

1. Abrir ES-DE (first-run); confirmar diretorio de ROMs.
2. Configurar scrapers / artes.
3. Definir players: RetroArch para os sistemas da tabela; DuckStation para `psx`.
4. No RetroArch: baixar cores (Online Updater / Core Downloader do APK oficial); video Vulkan.
5. No RetroArch: calibrar layout paisagem (jogo no centro, overlay nas laterais) — secao 8.
6. No DuckStation: resolucao interna 2x (720p); GPU Vulkan; apontar BIOS.
7. Validar um jogo por sistema conforme `checklist.md`.

## 8. RetroArch — layout paisagem (overlay + video)

Objetivo: imagem do jogo no centro; controles virtuais nas laterais (dedos nao cobrem a acao).

| Etapa | Quem | Como |
|---|---|---|
| Calibracao (1a vez / por resolucao) | **Operador na GUI** | Menus do RetroArch |
| Replicar config ja validada | **ADB** | `pull` / `push` do `retroarch.cfg` (e overrides, se houver) |
| “Clicar” nos menus via ADB | **Nao** | Sem automacao de UI neste projeto |

ADB nao controla a GUI do RetroArch de forma confiavel. O que o ADB faz bem e transportar o arquivo de configuracao depois que a GUI gravou os valores certos.

### 8.1 Calibracao na GUI (obrigatoria na primeira vez)

Com o aparelho em paisagem e um core/jogo carregado (ou pelo menos o overlay visivel):

1. **Sobreposicao (overlay)**  
   Configuracoes → Exibicao na Tela (On-Screen Display) → Sobreposicao de Tela (On-Screen Overlay):
   - ativar **Exibir Sobreposicao**;
   - **Predefinicao de Sobreposicao**: pasta `flat` ou `neo-retropad` (ou equivalente embutido); escolher o `.cfg` desejado (D-pad esquerda, acao direita).
2. **Video no centro**  
   Configuracoes → Video → Escalonamento (Scaling):
   - **Proporcao de Tela**: `4:3` ou `Core Provided` (barras laterais naturais para o overlay); **ou**
   - `Custom` + Width / Height / X / Y para encaixe milimetrico entre os controles.
3. **Ergonomia**  
   Voltar a Sobreposicao de Tela: **Escala** e **Opacidade** da sobreposicao.
4. **Persistir**  
   Menu principal → Arquivo de Configuracao → **Salvar Configuracao Atual**.  
   Opcional: Quick Menu → Overrides → salvar override por core/jogo se o layout for so para alguns sistemas.

Confirmar no aparelho (Settings / Directory / Paths, conforme a build) onde o RetroArch esta gravando o cfg antes do `adb pull`.

### 8.2 Chaves equivalentes no `retroarch.cfg`

Apos salvar na GUI, estas chaves refletem o layout (nomes canonicos do RetroArch; confirmar no arquivo puxado):

| Chave | Papel |
|---|---|
| `input_overlay_enable` | Liga a sobreposicao |
| `input_overlay` | Caminho absoluto do preset `.cfg` no aparelho |
| `input_overlay_opacity` | Transparencia |
| `input_overlay_scale` | Tamanho geral dos botoes |
| `aspect_ratio_index` | Indice da proporcao (4:3, Core Provided, Custom, …) |
| `custom_viewport_width` / `height` / `x` / `y` | Viewport quando a proporcao e Custom |

**Nao inventar** o valor de `aspect_ratio_index` de memoria: a ordem da lista muda entre versoes. Escolher na GUI, salvar, e ler o numero no cfg puxado. Referencia tipica em builds recentes do upstream (comentario do `retroarch.cfg` oficial): Custom costuma ser o indice de “Custom Aspect Ratio”; validar sempre no aparelho com RetroArch **1.22.2** deste inventario.

### 8.3 Localizar, arquivar e reaplicar via ADB

Caminhos comuns no Android (podem coexistir; usar o que a GUI indica apos “Salvar”):

```text
/storage/emulated/0/RetroArch/config/retroarch.cfg
/storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg
```

Descobrir no aparelho (exemplo):

```bash
adb shell "ls -la /storage/emulated/0/RetroArch/config/retroarch.cfg 2>/dev/null; ls -la /storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg 2>/dev/null"
```

Arquivar no PC (apos calibracao no Poco), a partir da raiz do repositorio:

```bash
mkdir -p resources/android/config/poco-x3-nfc
adb pull /storage/emulated/0/RetroArch/config/retroarch.cfg resources/android/config/poco-x3-nfc/retroarch.cfg
```

Se o pull do primeiro caminho falhar, repetir com o caminho em `Android/data/...` (ou o path real anotado na checklist).

Reaplicar (reinstalacao no mesmo modelo, ou ponto de partida no tablet):

```bash
adb push resources/android/config/poco-x3-nfc/retroarch.cfg /storage/emulated/0/RetroArch/config/retroarch.cfg
```

Se houver overrides por core:

```bash
adb pull /storage/emulated/0/RetroArch/config/<CoreName>/ resources/android/config/poco-x3-nfc/overrides/<CoreName>/
# e o push inverso apos confirmar os paths no aparelho
```

Contrato da pasta: `resources/android/config/README.md`.

### 8.4 Limites (importante)

- Viewport **Custom** e escala do overlay dependem da **resolucao e DPI** do aparelho. Um cfg “perfeito” no Poco X3 NFC **nao** e garantia no tablet — no tablet: push como base, depois reajustar na GUI e salvar um cfg proprio (`resources/android/config/<modelo-tablet>/`).
- O caminho em `input_overlay` deve existir no aparelho de destino; se o preset nao estiver la, reescolher o overlay na GUI uma vez.
- Fechar o RetroArch antes do `push` e reabrir depois, para ele reler o cfg (se o app estiver aberto, pode sobrescrever o arquivo ao sair).

## 9. Celular depois tablet

1. Completar e validar no Poco X3 NFC (incluindo secao 8).
2. Repetir as secoes 2–7 no tablet (mesmo inventario de APKs e mesma arvore).
3. Layout RetroArch: pode partir do cfg do Poco via secao 8.3, mas **revalidar** escala/viewport na GUI do tablet e arquivar cfg separado.
4. Registrar modelo, serial e desvios do tablet na checklist.

## 10. Troubleshooting

| Sintoma | Acao |
|---|---|
| `unauthorized` | Reautorizar depuracao USB; trocar cabo/porta |
| `more than one device` | Usar `adb -s <serial>` |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | Desinstalar a versao anterior (ex.: Play Store) e reinstalar o APK oficial |
| Push negado | Permissoes de armazenamento / scoped storage; confirmar caminho |
| ES-DE nao acha jogos | Conferir nomes das pastas ES-DE (`rom-layout.md`) e rescan no app |
| Overlay some apos push do cfg | Confirmar `input_overlay` e pasta de overlays no aparelho; reescolher preset na GUI |
| Jogo torto / fora do centro no tablet | Viewport do Poco nao serve; recalibrar Custom/escala na GUI do tablet |
| Config “nao pega” apos push | Fechar RetroArch, confirmar path do cfg que a build le na abertura, push de novo, reabrir |

## Relacionados

- `resources-inventory.md`
- `rom-layout.md`
- `checklist.md`
- `setup-play-store.md` (fallback)
- `tools-android.md` (raiz do repo)
- `resources/android/config/README.md` (cfgs RetroArch arquivados)
