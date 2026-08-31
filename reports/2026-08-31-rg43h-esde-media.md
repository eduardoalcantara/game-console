# Relatorio — Midia ES-DE → RG43H (2026-08-31)

## Contexto

No RG43H Pro (RGBox) o launcher **nao** oferecea scraper nem edicao de metadados
(SELECT so mostra aleatoriedade/pormenores). Capas precisam vir do PC.

Script: `scripts/tooling/apply_esde_media_rg43h.py`

## Resultado (staging)

| Metrica | Valor |
|---|---|
| ROMs analisadas | 458 |
| Com capa | **126** |
| Sem capa | **332** |

Destaques:

| Sistema | Capas / ROMs |
|---|---|
| nes | 44/45 |
| gba | ~17–21/46 |
| gbc | 13/33 |
| gb | 12–16/33 |
| snes | **14/115** |
| megadrive | 6/62 |
| mastersystem | 3/32 |
| pcengine | 2/25 |
| mame/cps1 | parcial |
| neogeo | 0/45 |

## Limitacao principal

`resources/es-de/downloaded_media/` no Google Drive esta **parcialmente sincronizado**:
pastas de letra so **A–E** (SNES) / **A–C** (MD). Por isso SNES/MD ficaram com poucas capas
mesmo com scrape ES-DE completo no Razr historicamente (~1,6k ficheiros).

**Accao operador:** no Google Drive Desktop, marcar
`resources/es-de/downloaded_media/` como **Disponivel offline** / sincronizar tudo;
depois reexecutar:

```bash
python scripts/tooling/apply_esde_media_rg43h.py --execute --yes
```

## Deploy SD

Unidade **H:** nao estava montada neste host no momento do execute.
Staging atualizado com `images/` + `gamelist.xml`.

Quando o cartao estiver em H: (ou outra letra):

```powershell
python scripts/tooling/apply_esde_media_rg43h.py --execute --yes --deploy H:\
# ou
.\scripts\tooling\windows\deploy_rg43h_sd.ps1 -DriveLetter H -SkipFormat -Yes
```

## Uso

```bash
python scripts/tooling/apply_esde_media_rg43h.py              # dry-run
python scripts/tooling/apply_esde_media_rg43h.py --system snes
python scripts/tooling/apply_esde_media_rg43h.py --execute --yes
python scripts/tooling/apply_esde_media_rg43h.py --uninstall --execute --yes
```

## Arquivos

- Script: `scripts/tooling/apply_esde_media_rg43h.py`
- Relatorio staging: `resources/rg43h/staging/media-report.md`
- Guia: `resources/rg43h/docs/operator-guide.md`
