#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pull_rg43h_network_saves.py
game-console — Baixa saves e savestates do console RG43H Pro via rede (SMB).

Salva em: core/rg43h-pro/saves-backup/<timestamp>/
- Varre o cartao SD (compartilhamento 'roms'): pastas savestates/ e ficheiros de save (.srm, .sav, .state*)
- Varre o armazenamento interno (compartilhamento 'Storage'): .config/retroarch/saves/
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


SAVE_EXTENSIONS = (
    ".srm",
    ".sav",
    ".state",
    ".rtc",
    ".mcr",
    ".mcd",
    ".vmp",
    ".csf",
    ".eep",
    ".fla",
    ".nv",
    ".hi",
    ".fs",
    ".dsv",
)

SKIP_NAMES = {"desktop.ini", "thumbs.db", "gamelist.xml", ".firstdownload"}
SKIP_DIRS = {"bios", "bezels", "images", "videos", "media", "boxes", "wheels", "manuals"}


def is_save_filename(name: str) -> bool:
    lower = name.lower()
    if lower in SKIP_NAMES or name.startswith("."):
        return False
    if any(lower.endswith(ext) for ext in SAVE_EXTENSIONS):
        return True
    if ".state" in lower and not lower.endswith((".xml", ".txt")):
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Baixa saves do RG43H Pro via rede (SMB).")
    parser.add_argument("--ip", default="172.16.201.25", help="IP do console (padrao: 172.16.201.25)")
    parser.add_argument("--execute", action="store_true", help="Efetua a copia real (sem --execute = dry-run)")
    parser.add_argument("--out", type=Path, default=None, help="Diretorio de destino customizado")
    args = parser.parse_args()

    try:
        import smbprotocol.tree
        import smbclient
    except ImportError:
        print("Erro: smbprotocol / smbclient nao disponiveis no ambiente Python.")
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

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    repo_root = Path(__file__).resolve().parents[2]
    out_dir = args.out if args.out else repo_root / "core" / "rg43h-pro" / "saves-backup" / ts

    print("==================================================")
    print("game-console — Backup de Saves via Rede (SMB)")
    print(f"Console IP: {args.ip}")
    print(f"Destino:    {out_dir}")
    print(f"Modo:       {'EXECUCAO REAL' if args.execute else 'DRY-RUN (use --execute para salvar)'}")
    print("==================================================")

    collected_files: list[tuple[str, str, Path]] = []  # (origem, remote_path, local_rel_path)

    # 1. Varredura do cartao SD (compartilhamento 'roms')
    print("\nProcurando saves no cartao SD (compartilhamento 'roms')...")
    try:
        roms_root = rf"\\{args.ip}\roms"
        top_entries = smbclient.listdir(roms_root)

        for entry in top_entries:
            if entry.lower() in SKIP_DIRS or entry.startswith("."):
                continue

            entry_path = f"{roms_root}\\{entry}"
            try:
                # Testa se eh diretorio
                sub_entries = smbclient.listdir(entry_path)
            except Exception:
                # Arquivo solto na raiz
                if is_save_filename(entry):
                    collected_files.append(("SD (raiz)", entry_path, Path("sd_root") / entry))
                continue

            # Se for a pasta savestates
            if entry.lower() == "savestates":
                def walk_savestates(curr_p: str, rel_p: Path):
                    try:
                        for item in smbclient.listdir(curr_p):
                            item_p = f"{curr_p}\\{item}"
                            try:
                                sub = smbclient.listdir(item_p)
                                walk_savestates(item_p, rel_p / item)
                            except Exception:
                                collected_files.append(("SD (savestates)", item_p, Path("savestates") / rel_p / item))
                    except Exception:
                        pass

                walk_savestates(entry_path, Path())
                continue

            # Se for uma pasta de sistema (ex: snes, gba, psx)
            for sub in sub_entries:
                if is_save_filename(sub):
                    sub_p = f"{entry_path}\\{sub}"
                    collected_files.append((f"SD ({entry})", sub_p, Path("roms") / entry / sub))

    except Exception as exc:
        print(f"Aviso ao varrer compartilhamento 'roms': {exc}")

    # 2. Varredura do armazenamento interno (compartilhamento 'Storage')
    print("Procurando saves no armazenamento interno (compartilhamento 'Storage')...")
    try:
        storage_save_dir = rf"\\{args.ip}\Storage\.config\retroarch\saves"
        try:
            for item in smbclient.listdir(storage_save_dir):
                item_p = f"{storage_save_dir}\\{item}"
                try:
                    smbclient.listdir(item_p)
                except Exception:
                    if is_save_filename(item):
                        collected_files.append(("Storage interno", item_p, Path("internal_saves") / item))
        except Exception:
            pass
    except Exception as exc:
        print(f"Aviso ao varrer armazenamento interno: {exc}")

    print(f"\nTotal de arquivos de save encontrados: {len(collected_files)}")
    for source, remote_p, local_rel in collected_files:
        print(f"  [{source}] {local_rel}")

    if not collected_files:
        print("\nNenhum arquivo de save foi localizado no console.")
        return 0

    if not args.execute:
        print("\n[DRY-RUN] Nenhuma copia foi efetuada. Execute com --execute para salvar os arquivos.")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    success = 0
    errors = 0

    for source, remote_p, local_rel in collected_files:
        target = out_dir / local_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with smbclient.open_file(remote_p, mode="rb") as rf:
                data = rf.read()
            target.write_bytes(data)
            success += 1
        except Exception as exc:
            print(f"Falha ao copiar {remote_p}: {exc}")
            errors += 1

    print(f"\nBackup concluido com sucesso!")
    print(f"  Copiados: {success}")
    print(f"  Erros:    {errors}")
    print(f"  Pasta:    {out_dir}")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
