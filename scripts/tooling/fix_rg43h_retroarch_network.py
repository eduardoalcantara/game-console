#!/usr/bin/env python3
"""Corrige o mapeamento de botoes do RetroArch via rede (SMB) no AISLPC RG43H Pro.

Conecta ao compartilhamento SMB na porta 445 do console (emuelec / storage),
localiza o retroarch.cfg e restaura os mapeamentos fisicos do play_joystick:
  - A = button 1 (confirm / menu ok)
  - B = button 0 (cancel / menu back)
  - X = button 2
  - Y = button 3
  - L1 = 4, R1 = 5, L2 = 6, R2 = 7, Select = 8, Start = 9, Up/Down/Left/Right = 14..17
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Corrige retroarch.cfg do RG43H Pro via rede (SMB).")
    parser.add_argument("--ip", default="172.16.201.25", help="IP do console na rede local (padrao: 172.16.201.25)")
    parser.add_argument("--dry-run", action="store_true", help="Apenas inspeciona os mapeamentos atuais sem alterar")
    args = parser.parse_args()

    try:
        import smbprotocol.tree
        import smbclient
    except ImportError:
        print("Erro: smbprotocol / smbclient nao estao instalados neste ambiente Python.")
        return 1

    orig_connect = smbprotocol.tree.TreeConnect.connect
    smbprotocol.tree.TreeConnect.connect = lambda self, require_secure_negotiate=True: orig_connect(
        self, require_secure_negotiate=False
    )

    smbclient.reset_connection_cache()
    try:
        smbclient.register_session(args.ip, username="", password="", require_signing=False, encrypt=False)
    except Exception as exc:
        print(f"Falha ao conectar via SMB em {args.ip}: {exc}")
        return 1

    remote_cfg = rf"\\{args.ip}\Storage\.config\retroarch\retroarch.cfg"
    try:
        with smbclient.open_file(remote_cfg, mode="r", encoding="utf-8", errors="replace") as rf:
            content = rf.read()
    except Exception as exc:
        print(f"Falha ao ler {remote_cfg}: {exc}")
        return 1

    lines = content.splitlines()
    fixed_bindings = {
        "input_player1_a": '"x"',
        "input_player1_a_btn": '"1"',
        "input_player1_b": '"z"',
        "input_player1_b_btn": '"0"',
        "input_player1_x": '"s"',
        "input_player1_x_btn": '"2"',
        "input_player1_y": '"a"',
        "input_player1_y_btn": '"3"',
        "input_player1_l_btn": '"4"',
        "input_player1_r_btn": '"5"',
        "input_player1_l2_btn": '"6"',
        "input_player1_r2_btn": '"7"',
        "input_player1_select_btn": '"8"',
        "input_player1_start_btn": '"9"',
        "input_player1_up_btn": '"14"',
        "input_player1_down_btn": '"15"',
        "input_player1_left_btn": '"16"',
        "input_player1_right_btn": '"17"',
    }

    new_lines: list[str] = []
    modified: dict[str, tuple[str, str]] = {}

    for line in lines:
        replaced = False
        for k, v in fixed_bindings.items():
            prefix = k + " ="
            if line.strip().startswith(prefix):
                old_val = line.strip()
                new_line = f"{k} = {v}"
                new_lines.append(new_line)
                if old_val != new_line:
                    modified[k] = (old_val, new_line)
                replaced = True
                break
        if not replaced:
            new_lines.append(line)

    if not modified:
        print("Todas as configuracoes ja estao corretas no console. Nenhuma alteracao necessaria.")
        return 0

    print(f"Foram identificadas {len(modified)} diferencas de configuracao:")
    for k, (o, n) in modified.items():
        print(f"  {o}  ==>  {n}")

    if args.dry_run:
        print("\nModo --dry-run: nenhuma alteracao foi gravada.")
        return 0

    # Gravar backup antes de salvar
    remote_bak = rf"\\{args.ip}\Storage\.config\retroarch\retroarch.cfg.bak"
    try:
        with smbclient.open_file(remote_bak, mode="w", encoding="utf-8") as wf:
            wf.write(content)
        print(f"Backup gravado em: {remote_bak}")
    except Exception as exc:
        print(f"Aviso: nao foi possivel gravar backup em {remote_bak}: {exc}")

    new_content = "\n".join(new_lines) + "\n"
    try:
        with smbclient.open_file(remote_cfg, mode="w", encoding="utf-8") as wf:
            wf.write(new_content)
        print(f"Arquivo atualizado com sucesso em: {remote_cfg}")
    except Exception as exc:
        print(f"Falha ao gravar novo arquivo em {remote_cfg}: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
