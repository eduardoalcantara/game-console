#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_rg43h_metadata.py
game-console — copia metadados EmuELEC do SD original (H:) para resources/rg43h/sd-original/
Sem tocar em ROMs; SD fisico permanece intacto.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple

REPO_FOLDER_NAME = "game-console"
DEFAULT_SRC = Path("H:/")
DEFAULT_DST_REL = Path("resources") / "rg43h" / "sd-original"

EXTRA_ROOT_DIRS = ("bezels", "savestates", "splash", "BGM")
META_NAMES = ("gamelist.xml", "gamelist.xml-bak")
META_SUBDIRS = ("images", "videos")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    print("game-console")
    print("Script: extract_rg43h_metadata")
    print("Funcao: Copiar gamelist.xml, images/ e videos/ do SD RG43H")
    print("----------------------------------------")


def find_repo_root(start: Path) -> Optional[Path]:
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if candidate.name.lower() == REPO_FOLDER_NAME:
            return candidate
    return None


def prompt_yes_no(question: str, default: int = 0) -> int:
    while True:
        print(question)
        print("  0 = nao")
        print("  1 = sim")
        print(f"  Enter = default ({'sim' if default == 1 else 'nao'})")
        try:
            raw = input("> ").strip()
        except EOFError:
            return default
        if raw == "":
            return default
        if raw in ("0", "1"):
            return int(raw)
        print("Entrada invalida. Digite 0, 1 ou Enter.")


def copy_file(src: Path, dst: Path, execute: bool) -> bool:
    if dst.exists():
        try:
            if dst.stat().st_size == src.stat().st_size:
                return False
        except OSError:
            pass
    if execute:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return True


def copy_tree(src: Path, dst: Path, execute: bool) -> Tuple[int, int]:
    copied = 0
    skipped = 0
    if not src.is_dir():
        return copied, skipped
    for root, _dirs, files in os.walk(src):
        root_path = Path(root)
        for name in files:
            s = root_path / name
            rel = s.relative_to(src)
            d = dst / rel
            if copy_file(s, d, execute):
                copied += 1
            else:
                skipped += 1
    return copied, skipped


def extract_system(src_sys: Path, dst_sys: Path, execute: bool) -> Tuple[int, int]:
    copied = 0
    skipped = 0
    for name in META_NAMES:
        s = src_sys / name
        if s.is_file():
            if copy_file(s, dst_sys / name, execute):
                copied += 1
            else:
                skipped += 1
    for sub in META_SUBDIRS:
        s = src_sys / sub
        if s.is_dir():
            c, k = copy_tree(s, dst_sys / sub, execute)
            copied += c
            skipped += k
    return copied, skipped


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copia metadados EmuELEC do SD original para o repo."
    )
    parser.add_argument("--src", type=str, default=str(DEFAULT_SRC))
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--yes", action="store_true")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    clear_screen()
    print_header()

    repo_root = find_repo_root(Path(__file__).resolve().parent)
    if repo_root is None:
        print(f"ERRO: pasta '{REPO_FOLDER_NAME}' nao encontrada.")
        return 1

    src = Path(args.src)
    dst = repo_root / DEFAULT_DST_REL
    mode = "EXECUTE" if args.execute else "DRY-RUN"

    print(f"REPO_ROOT={repo_root}")
    print(f"Modo: {mode}")
    print(f"Origem: {src}")
    print(f"Destino: {dst}")
    print()

    if not src.is_dir():
        print(f"ERRO: SD nao encontrado em {src}")
        return 1

    if args.execute and not args.yes:
        if prompt_yes_no("Confirmar copia de metadados?", default=0) != 1:
            print("Cancelado.")
            return 0

    total_copied = 0
    total_skipped = 0
    systems = 0

    for entry in sorted(src.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.lower() in {
            "system volume information",
            "found.000",
            "bios",
            ".update",
            "downloads",
            "ports",
            "ports_scripts",
            "applycenter",
            "mplayer",
        }:
            continue
        c, k = extract_system(entry, dst / entry.name, args.execute)
        if c or k:
            systems += 1
            print(f"  {entry.name}: copiados={c} ignorados={k}")
            total_copied += c
            total_skipped += k

    for name in EXTRA_ROOT_DIRS:
        s = src / name
        if s.is_dir():
            c, k = copy_tree(s, dst / name, args.execute)
            if c or k:
                print(f"  {name}/: copiados={c} ignorados={k}")
                total_copied += c
                total_skipped += k

    print()
    print(f"Sistemas com metadados: {systems}")
    print(f"Ficheiros copiados: {total_copied}")
    print(f"Ficheiros ignorados (ja existiam): {total_skipped}")
    if not args.execute:
        print("Dry-run. Use --execute --yes para copiar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
