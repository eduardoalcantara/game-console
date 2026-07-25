# resources/android/config

Arquivo de configuracoes do RetroArch (e futuros overrides) puxados dos aparelhos apos calibracao na GUI.

Fluxo normativo: `core/android-poco-x3-nfc/docs/setup-adb.md` secao 8.

## Layout sugerido

```text
resources/android/config/
  README.md
  poco-x3-nfc/
    retroarch.cfg          # apos calibracao no celular
    overrides/             # opcional: overrides por core
  <modelo-tablet>/
    retroarch.cfg          # apos reajuste no tablet (nao reutilizar viewport cego)
```

## Regras

- Calibrar **sempre** na GUI na primeira vez por resolucao de tela.
- ADB so replica o `.cfg` ja validado (`adb pull` / `adb push`).
- Um cfg por modelo de aparelho quando houver Custom viewport ou escala de overlay diferente.
- Nao inventar `aspect_ratio_index`: ler o valor gravado pelo RetroArch apos salvar na GUI.
- Os `.cfg` sao texto pequeno e **podem** ser versionados se nao contiverem caminhos ou dados sensíveis indesejados; conferir `input_overlay` e diretorios antes do commit.

## O que nao entra aqui

- APKs, BIOS, ROMs (pastas irmas / `resources/roms/`).
- Automacao de cliques na GUI do RetroArch.
