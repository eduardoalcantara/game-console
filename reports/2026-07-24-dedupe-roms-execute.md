# Relatorio — execucao dedupe_roms (producao)

**Data:** 2026-07-24  
**Script:** `scripts/tooling/dedupe_roms.py`  
**Modo:** EXECUTE (`--execute --yes`)  
**Biblioteca:** `resources/roms/`  
**Dry-run previo:** `reports/2026-07-24-dedupe-roms-dryrun.md`

## Resultado

| Metrica | Valor |
|---|---|
| Arquivos considerados | 2839 |
| Protegidos (hack/traducao/mod) | 0 |
| Apagados | 40 |
| Renomeados (strip ` (USA)`) | 1919 |
| Erros | 0 |

Nenhum erro de permissao ou I/O. Acao concluida com sucesso.

## O que foi feito

1. Removidas duplicatas por regiao (Europe quando existia USA) e por revisao inferior/empate na mesma regiao.
2. Removido o sufixo ` (USA)` dos jogos que ficaram com uma unica versao nao-protegida.

## Artefatos

- Log bruto da execucao: `reports/_dedupe_roms_execute_raw.txt`
- Dry-run de auditoria previa: `reports/2026-07-24-dedupe-roms-dryrun.md`
- Log bruto do dry-run: `reports/_dedupe_roms_dryrun_raw.txt`

## Validacao pos-execucao

Segundo dry-run apos a producao:

| Metrica | Valor |
|---|---|
| Arquivos considerados | 2799 |
| Delecoes planejadas | 0 |
| Renomeacoes planejadas | 0 |
| Total de arquivos em `resources/roms/` (incl. saves/companions) | 2824 (~2,63 GB) |

Biblioteca estabilizada: nenhuma acao adicional necessaria pelas regras atuais.

## Proximo passo

- Seguir com o fluxo Android (APKs em `resources/android/apk/`, depois ADB no celular).
- Opcional: remover os logs brutos `_dedupe_roms_*_raw.txt` apos auditoria humana.
