# Inventario de recursos — Android

Lista normativa do que vai em `resources/android/`, com coluna **Origem**:

- **Manual** — so o operador pode obter (compra, dump proprio, Play Store ou arquivo local).
- **Automatizavel** — download publico oficial; o agente/scripts podem baixar para a pasta.

Caminho primario de instalacao: ADB (`setup-adb.md`). Play Store: fallback restrito (`setup-play-store.md`).

## Regras

- Nao versionar APK, BIOS ou ROM neste repositorio (`.gitignore` cobre `*.apk` e dumps).
- Nao usar espelhos de terceiros (APKMirror, Aptoide e similares) como fonte canonica.
- ES-DE Android e app pago: nao redistribuir o APK.
- Registrar versao e hash na tabela "Estado atual do inventario".

### Comandos de hash

PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 .\resources\android\apk\arquivo.apk
```

Linux:

```bash
sha256sum resources/android/apk/arquivo.apk
```

---

## Obrigatorios

| Item | Origem | Funcao | Fonte oficial | Destino | Nome esperado |
|---|---|---|---|---|---|
| ES-DE Android (pago) | **Manual** | Frontend | Canal pago via `https://es-de.org/`; APK 3.4.1-58: `https://packages.es-de.org/android/b829bd05/ES-DE_3.4.1-58.apk` | `resources/android/apk/` | `ES-DE_3.4.1-58.apk` (nome do canal) |
| RetroArch AArch64 | **Automatizavel** | Emulador multi-sistema | `https://buildbot.libretro.com/stable/1.22.2/android/RetroArch_aarch64.apk` | `resources/android/apk/` | `retroarch-aarch64-1.22.2.apk` |
| DuckStation | **Manual** (ver nota) | Emulador PS1 | Play Store: `com.github.stenzek.duckstation` | `resources/android/apk/` (se tiver APK) **ou** install direto no aparelho | `duckstation-android.apk` |
| BIOS PS1 | **Manual** | Boot PS1 | Dump do console proprio | `resources/android/bios/` | ex.: `ps1-scphXXXX.bin` |
| Android platform-tools | **Manual** (maquina) | `adb` | `https://developer.android.com/tools/releases/platform-tools` | PATH do PC (nao no repo) | platform-tools |
| Temas ES-DE (grupo GitLab) | **Automatizavel** | UI do frontend | [gitlab.com/es-de/themes](https://gitlab.com/es-de/themes) | `resources/es-de/themes/` | clones shallow; ver README da pasta |

### Nota DuckStation (2026-07-24)

Tentativa de download automatizado falhou: URLs oficiais
`https://www.duckstation.org/android/duckstation-android.apk` e variantes retornam **404**.
Releases do GitHub `stenzek/duckstation` **nao** publicam APK Android (so desktop).
F-Droid: pacote nao encontrado.

Conclusao: ate reaparecer um APK publico oficial, DuckStation fica **Manual** via Play Store no aparelho (ou voce coloca um APK que ja tenha em `resources/android/apk/`). Para ADB puro sem Play Store, o frontend ES-DE ainda pode apontar o player apos a instalacao pela loja.

## Condicionais

| Item | Origem | Quando | Fonte | Destino |
|---|---|---|---|---|
| BIOS Neo Geo | **Manual** | Usar `android/neogeo` ou `neogeocd` | Dump proprio | `resources/android/bios/` |
| BIOS Saturn / Sega CD / FDS / etc. | **Manual** | Ao popular pastas que exigem BIOS | Dump proprio | `resources/android/bios/` |
| PPSSPP APK | **Automatizavel** | Quando houver ISOs em `android/psp/` | `https://www.ppsspp.org/` | `resources/android/apk/` |

## Fora do inventario obrigatorio

| Item | Motivo |
|---|---|
| Daijisho | Frontend primario = ES-DE |
| Standalones N64/NDS/Dreamcast/Saturn | Pastas reservadas; APKs sob demanda |
| Conteudo `pc-only/` | Fora do escopo Android |

---

## Quem faz o que

### So voce (manual)

1. Comprar/baixar **ES-DE Android** (acesso pago) e salvar em `resources/android/apk/` — ja feito para 3.4.1-58.
2. Instalar **DuckStation** pela Play Store no celular/tablet **ou** fornecer APK local se tiver.
3. Colocar **BIOS PS1** (e outras BIOS se necessario) em `resources/android/bios/` — PS1: `SCPH1001.BIN` ja presente.
4. Garantir **platform-tools** (`adb`) no PC.
5. Preencher hashes de DuckStation (se APK) / BIOS adicionais na tabela (ES-DE e BIOS PS1 ja registrados).

### Automatizavel (feito / a repetir)

1. Baixar **RetroArch AArch64** stable do buildbot Libretro.
2. Calcular SHA-256 e registrar na tabela.

Comando de referencia (repetir em nova versao):

```powershell
curl.exe -L -o resources/android/apk/retroarch-aarch64-1.22.2.apk `
  https://buildbot.libretro.com/stable/1.22.2/android/RetroArch_aarch64.apk
Get-FileHash -Algorithm SHA256 resources/android/apk/retroarch-aarch64-1.22.2.apk
```

---

## Notas por item

### ES-DE (manual)

- Pago; fora da Play Store; nao redistribuir.
- Ja presente em `resources/android/apk/ES-DE_3.4.1-58.apk` (2026-07-24). O nome original do canal oficial foi mantido no lugar de `es-de-<versao>.apk` para preservar rastreabilidade.
- A versao registrada vem do nome do arquivo; confirmar no aparelho apos instalar (Main Menu → Help/About).
- URL de download desta build (acesso autenticado / token no path; nao e publico aberto):

```text
https://packages.es-de.org/android/b829bd05/ES-DE_3.4.1-58.apk
```

Comando de referencia (requer acesso ao pacote; nao automatizar sem autenticacao valida):

```powershell
curl.exe -L -o resources/android/apk/ES-DE_3.4.1-58.apk `
  https://packages.es-de.org/android/b829bd05/ES-DE_3.4.1-58.apk
Get-FileHash -Algorithm SHA256 resources/android/apk/ES-DE_3.4.1-58.apk
```

- O segmento `b829bd05` no path e especifico desta distribuicao; builds futuras terao outro path — obter o link atualizado pelo canal oficial apos a compra.

### RetroArch (automatizavel)

- Play Store = nao recomendada.
- Se a build da loja ja estiver no aparelho, desinstalar antes do APK oficial.

### DuckStation (manual por indisponibilidade do APK)

- Preferir Play Store enquanto o APK oficial estiver offline.
- Sem suporte ativo do autor no Android.

### BIOS PS1 (manual)

- Arquivo local: `resources/android/bios/SCPH1001.BIN` (operador, 2026-07-25).
- **Nao versionar** (`.gitignore` cobre `*.bin`; firmware proprietario).
- Hash registrado so no inventario local do operador para conferencia apos copia/perda.

---

## Estado atual do inventario

| Arquivo local | Origem | Versao / data | SHA-256 | Data do registro | Notas |
|---|---|---|---|---|---|
| `apk/ES-DE_3.4.1-58.apk` | Manual | **3.4.1-58** (build indicada pelo nome do arquivo) | `4B8C06F1CF505945EDD77F9B8FA523E8F580A13EAEF1A02F0092390F3739B387` | 2026-07-24 | ~79 MB; URL: `https://packages.es-de.org/android/b829bd05/ES-DE_3.4.1-58.apk`; versao nao conferida via `aapt` |
| `apk/retroarch-aarch64-1.22.2.apk` | Automatizavel | **1.22.2** (stable, 2025-11-20 buildbot) | `7BD5D208DFE93CC8E2EA6C04608948CE1A045980F160A58CA2D0993AA20AD213` | 2026-07-24 | ~175 MB; baixado do buildbot |
| `apk/duckstation-android.apk` | Manual | _(pendente — APK oficial 404)_ | | | Instalar via Play Store ou fornecer APK |
| `bios/SCPH1001.BIN` | Manual | SCPH-1001 (nome do arquivo) | `71AF94D1E47A68C11E8FDB9F8368040601514A42A5A399CDA48C7D3BFF1E99D3` | 2026-07-25 | 512 KB; **fora do Git**; dump/arquivo do operador |
| `bios/...` (Neo Geo) | Manual | _(pendente se usado)_ | | | dump proprio |

## Proximo passo

1. Operador: DuckStation (Play Store ou APK proprio). ES-DE, RetroArch e BIOS PS1 ja arquivados localmente.
2. Seguir `setup-adb.md` (ES-DE e RetroArch em `apk/`; BIOS em `bios/`).
