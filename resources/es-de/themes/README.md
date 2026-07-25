# Temas ES-DE (espelho no repositorio)

Fonte oficial do grupo: [gitlab.com/es-de/themes](https://gitlab.com/es-de/themes).

Espelho obtido em 2026-07-24 via shallow clone; metadados `.git` das pastas-filhas foram **removidos** para versionar o conteudo neste repositorio (2026-07-25).

## Conteudo (grupo GitLab)

| Pasta | Papel | Tamanho aprox. |
|---|---|---|
| `modern-es-de` | Tema Modern (oficial) | ~32 MB |
| `slate-es-de` | Tema Slate (oficial) | ~16 MB |
| `themes-list` | Lista curada + previews do theme downloader | ~88 MB |
| `carousel-icons` | Assets de icones | ~186 MB |
| `system-backgrounds` | Fundos de sistema | ~64 MB |
| `system-logos` | Logos de sistema | ~12 MB |
| `system-controllers-outline` | Controles outline | ~5 MB |
| `system-graphics-mini` | Graficos mini | ~9 MB |
| `system-graphics-silver-ring` | Graficos silver-ring | ~98 MB |
| `system-metadata` | Metadados de sistema | ~4 MB |
| `theme-engine-examples-es-de` | Exemplos do theme engine | ~16 MB |

Total aproximado: **~530 MB**.

## O que isto nao inclui

A lista curada em `themes-list` aponta dezenas de temas de terceiros hospedados sobretudo no **GitHub**, nao neste grupo GitLab. Esses so entram no aparelho via Theme Downloader do ES-DE (ou download manual sob demanda).

No Android, o tema **Linear** costuma vir embutido no app; Modern/Slate e demais via downloader ou copia manual.

## Uso no aparelho

Destino tipico no storage acessivel pelo ES-DE:

```text
ES-DE/themes/<nome-do-tema>/
```

Para instalar via ADB (exemplo Modern + Slate):

```powershell
adb push "resources\es-de\themes\modern-es-de" /sdcard/ES-DE/themes/modern-es-de
adb push "resources\es-de\themes\slate-es-de" /sdcard/ES-DE/themes/slate-es-de
```

Ajuste o caminho `/sdcard/ES-DE/` se o ES-DE no aparelho usar outro root (confirmar em Main Menu → Settings → Application Paths).

Assets (`system-*`, `carousel-icons`) sao packs compartilhados para autores de temas; so empurrar se o tema escolhido depender deles fora do bundle.

## Atualizar o espelho

As pastas **nao** sao mais clones Git. Para atualizar a partir do upstream:

1. Clonar de novo o repo oficial em pasta temporaria (`git clone --depth 1`).
2. Remover o `.git` da pasta temporaria.
3. Substituir o conteudo correspondente sob `resources/es-de/themes/<nome>/`.
4. Commitar a diferenca neste repositorio.
