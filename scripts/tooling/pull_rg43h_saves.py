#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pull_rg43h_saves.py
game-console — verifica e faz backup de saves/savestates do SD RG43H
para core/rg43h-pro/saves-backup/ antes de formatar ou redeploy completo.

Uso:
  python scripts/tooling/pull_rg43h_saves.py              # dry-run, drive H:
  python scripts/tooling/pull_rg43h_saves.py --execute --yes
  python scripts/tooling/pull_rg43h_saves.py --drive H --execute --yes
  python scripts/tooling/pull_rg43h_saves.py --uninstall --execute --yes

Notas:
- No EmuELEC/RGBox os saves costumam ficar no storage INTERNO; este script
  so captura o que estiver no cartao SD (EEROMS).
- Pastas tipicas: savestates/, saves/, savefiles/, retroarch/, e por sistema
  ficheiros .srm / .state* / .sav / .rtc / .mcr / .vmp / .csf / .eep / .fla
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Set, Tuple

from dedupe_roms import find_repo_root, prompt_yes_no  # noqa: E402

REPO_FOLDER_NAME = "game-console"
BACKUP_REL = Path("core") / "rg43h-pro" / "saves-backup"

SAVE_DIR_NAMES = frozenset(
    {
        "savestates",
        "saves",
        "savefiles",
        "save",
        "states",
        "retroarch",
        "rr",
        "memcards",
        "memorycard",
        "memorycards",
    }
)

SAVE_SUFFIXES = frozenset(
    {
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
        ".ups",
        ".ips",
        ".bps",
    }
)

# Prefixo/sufixo tipico de savestate RetroArch (.state, .state1, .state.auto, etc.)
SKIP_NAMES = frozenset({"desktop.ini", "thumbs.db", "gamelist.xml", ".firstdownload"})


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    print("game-console")
    print("Script: pull_rg43h_saves")
    print("Funcao: Verificar/backup saves do SD RG43H -> saves-backup")
    print("----------------------------------------")


def resolve_drive_root(drive: str) -> Path:
    d = drive.strip().rstrip("\\/")
    if len(d) == 1 and d.isalpha():
        return Path(f"{d}:/")
    return Path(drive)


def is_save_file(path: Path) -> bool:
    name = path.name
    lower = name.lower()
    if lower in SKIP_NAMES or name.startswith("."):
        return False
    suf = path.suffix.lower()
    if suf in SAVE_SUFFIXES:
        return True
    # .state0 .. .state9, .state.auto
    if ".state" in lower and not lower.endswith((".png", ".jpg", ".xml", ".txt")):
        return True
    return False


def collect_save_items(sd_root: Path) -> Tuple[List[Path], List[Path]]:
    """Retorna (ficheiros_save, pastas_save_raiz)."""
    files: List[Path] = []
    dirs: List[Path] = []
    seen_files: Set[str] = set()

    if not sd_root.is_dir():
        return files, dirs

    # Pastas nomeadas na raiz e um nivel abaixo (ex.: snes/savestates)
    for child in sd_root.iterdir():
        if not child.is_dir():
            continue
        if child.name.lower() in SAVE_DIR_NAMES:
            dirs.append(child)
            continue
        # subpastas de save dentro de sistemas
        try:
            for sub in child.iterdir():
                if sub.is_dir() and sub.name.lower() in SAVE_DIR_NAMES:
                    dirs.append(sub)
        except OSError:
            pass

    # Ficheiros save soltos na raiz e nas pastas de sistema (nao recursivo profundo em bios)
    skip_walk = {"bios", "bezels", "images", "videos", "media", "boxes", "wheels", "manuals"}
    for root, dirnames, filenames in os.walk(sd_root):
        root_path = Path(root)
        # nao entrar em pastas de media pesadas
        dirnames[:] = [d for d in dirnames if d.lower() not in skip_walk]
        rel_parts = root_path.relative_to(sd_root).parts if root_path != sd_root else ()
        if any(p.lower() in skip_walk for p in rel_parts):
            continue
        for fn in filenames:
            fp = root_path / fn
            if is_save_file(fp):
                key = str(fp.resolve())
                if key not in seen_files:
                    seen_files.add(key)
                    files.append(fp)

    return files, dirs


def copy_tree(src: Path, dst: Path, execute: bool) -> int:
    count = 0
    if not execute:
        for _r, _d, files in os.walk(src):
            count += len(files)
        return count
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)
    for _r, _d, files in os.walk(dst):
        count += len(files)
    return count


def copy_file_rel(src: Path, sd_root: Path, backup_root: Path, execute: bool) -> bool:
    rel = src.relative_to(sd_root)
    dst = backup_root / rel
    if not execute:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def uninstall_backup(backup_root: Path, execute: bool) -> int:
    if not backup_root.exists():
        print("Nada a desinstalar (saves-backup ausente).")
        return 0
    n = sum(1 for _ in backup_root.rglob("*") if _.is_file())
    print(f"Remover backup: {backup_root} ({n} ficheiros)")
    if execute:
        shutil.rmtree(backup_root, ignore_errors=True)
    return n


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Backup saves SD RG43H")
    parser.add_argument("--drive", default="H", help="Letra ou caminho do SD (default H)")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove apenas core/rg43h-pro/saves-backup/",
    )
    args = parser.parse_args(argv)

    clear_screen()
    print_header()

    repo_root = find_repo_root(Path(__file__).resolve().parent)
    if repo_root is None:
        repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        print(f"ERRO: pasta '{REPO_FOLDER_NAME}' nao encontrada.")
        return 1

    backup_root = repo_root / BACKUP_REL
    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"REPO_ROOT={repo_root}")
    print(f"Modo: {mode}")
    print(f"Backup: {backup_root}")
    print()

    if args.uninstall:
        if args.execute and not args.yes:
            if prompt_yes_no("Apagar saves-backup?", default=0) != 1:
                print("Cancelado.")
                return 0
        uninstall_backup(backup_root, args.execute)
        print("Acao concluida: pull_rg43h_saves --uninstall")
        return 0

    sd_root = resolve_drive_root(args.drive)
    print(f"SD: {sd_root}")
    if not sd_root.is_dir():
        print(f"ERRO: volume/pasta nao encontrado: {sd_root}")
        print("Insira o cartao SD e indique a letra correcta (--drive H).")
        return 1

    files, dirs = collect_save_items(sd_root)
    print()
    print("=== Verificacao de saves no SD ===")
    print(f"Pastas de save: {len(dirs)}")
    for d in dirs:
        try:
            rel = d.relative_to(sd_root)
        except ValueError:
            rel = d
        print(f"  [dir] {rel}")
    print(f"Ficheiros de save: {len(files)}")
    for f in files[:40]:
        try:
            rel = f.relative_to(sd_root)
        except ValueError:
            rel = f
        print(f"  [file] {rel} ({f.stat().st_size} bytes)")
    if len(files) > 40:
        print(f"  ... +{len(files) - 40}")

    if not dirs and not files:
        print()
        print(
            "Nenhum save/savestate detectado no SD. "
            "Provavel: saves no storage INTERNO do RG43H (seguro ao formatar o cartao)."
        )
        print("Acao concluida: pull_rg43h_saves (nada a copiar)")
        return 0

    print()
    print(
        "ATENCAO: ha dados de save no cartao. "
        "Fazer backup antes de formatar (--execute)."
    )

    if args.execute and not args.yes:
        if prompt_yes_no("Copiar saves do SD para saves-backup?", default=1) != 1:
            print("Cancelado.")
            return 0

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = backup_root / stamp
    print(f"Destino: {dest}")

    copied_dirs = 0
    copied_files = 0
    if args.execute:
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "SOURCE.txt").write_text(
            f"SD={sd_root}\nUTC={stamp}\n", encoding="utf-8"
        )

    for d in dirs:
        try:
            rel = d.relative_to(sd_root)
        except ValueError:
            rel = Path(d.name)
        n = copy_tree(d, dest / rel, args.execute)
        copied_dirs += 1
        copied_files += n
        print(f"  pasta {rel}: {n} ficheiros")

    # ficheiros soltos (evitar duplicar os que ja estao dentro de pastas copiadas)
    dir_prefixes = []
    for d in dirs:
        try:
            dir_prefixes.append(str(d.resolve()))
        except OSError:
            pass

    for f in files:
        try:
            f_res = str(f.resolve())
        except OSError:
            continue
        if any(f_res.startswith(p + os.sep) or f_res.startswith(p + "/") for p in dir_prefixes):
            continue
        if copy_file_rel(f, sd_root, dest, args.execute):
            copied_files += 1
            try:
                print(f"  ficheiro {f.relative_to(sd_root)}")
            except ValueError:
                print(f"  ficheiro {f.name}")

    # pointer "latest"
    if args.execute:
        latest = backup_root / "latest"
        if latest.exists() or latest.is_symlink():
            try:
                if latest.is_symlink() or latest.is_file():
                    latest.unlink()
                else:
                    shutil.rmtree(latest, ignore_errors=True)
            except OSError:
                pass
        # Windows: copiar snapshot latest como junta (sem symlink obrigatorio)
        latest_txt = backup_root / "LATEST.txt"
        latest_txt.write_text(str(dest.relative_to(backup_root)) + "\n", encoding="utf-8")

    print()
    print(f"Pastas de save: {copied_dirs} | Ficheiros (aprox.): {copied_files}")
    print("Acao concluida: pull_rg43h_saves")
    print(f"Diretorio raiz detectado: {repo_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
