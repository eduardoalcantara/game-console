#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_roms.py
game-console — move ROMs de fontes externas para resources/roms/
com prioridade USA (mesmas regras de regiao que dedupe_roms.py).
Dry-run por padrao.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Reutiliza parsing e regras de regiao/revisao
from dedupe_roms import (  # noqa: E402
    RomFile,
    build_rom,
    collect_roms,
    find_repo_root,
    plan_group,
    prompt_yes_no,
)

REPO_FOLDER_NAME = "game-console"
DEFAULT_DEST = Path("resources") / "roms"

# Biblioteca externa documentada em rom-layout.md
EXTERNAL_LIBRARY = Path(r"G:\Meu Drive\Recursos\Jogos\roms")

# Pastas externas (maiusculas) -> (faixa, pasta ES-DE)
EXTERNAL_MAP: Dict[str, Tuple[str, str]] = {
    "2600": ("android", "atari2600"),
    "LYNX": ("android", "atarilynx"),
    "WSWAN": ("android", "wonderswan"),
    "GB": ("android", "gb"),
    "GBA": ("android", "gba"),
    "GBC": ("android", "gbc"),
    "NES": ("android", "nes"),
    "SNES": ("android", "snes"),
    "SMS": ("android", "mastersystem"),
    "SMD": ("android", "megadrive"),
    "PCE": ("android", "pcengine"),
    "NEOGEO": ("android", "neogeo"),
    "MAME": ("android", "mame"),
    "PS1": ("android", "psx"),
    "PC": ("pc-only", "dos"),
}

# EmuELEC (new-roms) -> pasta ES-DE quando diferente
EMUELEC_RENAME: Dict[str, str] = {
    "lynx": "atarilynx",
    "wswan": "wonderswan",
    "wswanc": "wonderswancolor",
    "sg1000": "sg-1000",
    "msx1": "msx",
    "gamecube": "gc",
}

# Sistemas pesados / desktop
PC_ONLY_SYSTEMS: Set[str] = {
    "ps2",
    "ps3",
    "wii",
    "wiiu",
    "xbox",
    "xbox360",
    "gamecube",
    "gc",
    "dos",
    "windows",
    "windows_installers",
}

# Ignorar placeholders EmuELEC (1 arquivo pequeno)
MIN_FILES_OR_BYTES = (2, 1_000_000)  # >=2 arquivos OU >=1 MB total

SKIP_TOP_LEVEL = {"roms", "bios", "desktop.ini", "thumbs.db"}


@dataclass
class MergeStats:
    moved: int = 0
    discarded_incoming: int = 0
    replaced_existing: int = 0
    skipped_dup: int = 0
    skipped_empty: int = 0
    errors: int = 0
    systems: Set[str] = field(default_factory=set)


@dataclass
class MergeAction:
    kind: str  # move | discard_incoming | skip_dup
    src: Path
    dst: Optional[Path] = None
    reason: str = ""
    delete_existing: List[Path] = field(default_factory=list)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    print("game-console")
    print("Script: merge_roms")
    print("Funcao: Mover ROMs para resources/roms/ (prioridade USA)")
    print("----------------------------------------")


def has_real_content(folder: Path) -> bool:
    files = [p for p in folder.rglob("*") if p.is_file()]
    if not files:
        return False
    total = sum(p.stat().st_size for p in files)
    min_files, min_bytes = MIN_FILES_OR_BYTES
    return len(files) >= min_files or total >= min_bytes


def resolve_dest(
    repo_root: Path,
    band: str,
    system: str,
) -> Path:
    if band == "bios":
        return (repo_root / DEFAULT_DEST / "bios").resolve()
    if system == "switch":
        return (repo_root / DEFAULT_DEST / "switch").resolve()
    return (repo_root / DEFAULT_DEST / band / system).resolve()


def emuelec_target(system: str) -> Tuple[str, str]:
    canonical = EMUELEC_RENAME.get(system, system)
    if system == "switch":
        return "switch", "switch"
    if canonical in PC_ONLY_SYSTEMS:
        return "pc-only", canonical
    return "android", canonical


def plan_incoming(
    incoming: RomFile,
    index: Dict[str, List[RomFile]],
) -> MergeAction:
    """Decide o que fazer com um arquivo de origem."""
    existing = list(index.get(incoming.base_key, []))
    if not existing:
        return MergeAction(
            kind="move",
            src=incoming.path,
            reason="novo titulo no sistema",
        )

    group = existing + [incoming]
    deletes, keeper = plan_group(group)
    delete_paths = {p.resolve() for p, _ in deletes}

    if incoming.path.resolve() in delete_paths:
        return MergeAction(
            kind="discard_incoming",
            src=incoming.path,
            reason="regiao/revisao inferior (mantida versao existente)",
        )

    losers = [p for p, _ in deletes if p.resolve() != incoming.path.resolve()]
    reason = "versao preferida (USA/revisao)"
    if keeper is not None and keeper.path.resolve() != incoming.path.resolve():
        reason = f"substitui {keeper.name} (regiao/revisao superior)"

    return MergeAction(
        kind="move",
        src=incoming.path,
        delete_existing=[p for p in losers],
        reason=reason,
    )


def build_system_index(system_root: Path) -> Dict[str, List[RomFile]]:
    index: Dict[str, List[RomFile]] = defaultdict(list)
    if not system_root.is_dir():
        return index
    for rom in collect_roms(system_root):
        index[rom.base_key].append(rom)
    return index


def refresh_index_entry(
    index: Dict[str, List[RomFile]],
    rom: RomFile,
    remove: Optional[Path] = None,
) -> None:
    if remove is not None:
        key = build_rom(remove).base_key
        index[key] = [r for r in index[key] if r.path.resolve() != remove.resolve()]
        if not index[key]:
            del index[key]
    index[rom.base_key].append(rom)


def apply_action(
    action: MergeAction,
    dest_dir: Path,
    stats: MergeStats,
    execute: bool,
) -> None:
    if action.kind == "skip_dup":
        stats.skipped_dup += 1
        return

    if action.kind == "discard_incoming":
        stats.discarded_incoming += 1
        if execute:
            try:
                action.src.unlink()
            except OSError as exc:
                stats.errors += 1
                print(f"ERRO ao descartar {action.src}: {exc}")
        return

    dst = action.dst if action.dst is not None else dest_dir / action.src.name

    # Duplicata exata
    if dst.exists() and action.src.resolve() != dst.resolve():
        try:
            if dst.stat().st_size == action.src.stat().st_size:
                stats.skipped_dup += 1
                if execute:
                    action.src.unlink()
                return
        except OSError:
            pass

    if action.delete_existing:
        stats.replaced_existing += len(action.delete_existing)
        if execute:
            for old_path in action.delete_existing:
                try:
                    if old_path.exists():
                        old_path.unlink()
                except OSError as exc:
                    stats.errors += 1
                    print(f"ERRO ao apagar existente {old_path}: {exc}")
                    return

    stats.moved += 1
    if not execute:
        return

    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(action.src), str(dst))
    except OSError as exc:
        stats.errors += 1
        print(f"ERRO ao mover {action.src} -> {dst}: {exc}")


def merge_system_folder(
    src_root: Path,
    dest_root: Path,
    stats: MergeStats,
    execute: bool,
    system_label: str,
) -> None:
    if not has_real_content(src_root):
        stats.skipped_empty += 1
        return

    stats.systems.add(system_label)
    index = build_system_index(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    incoming_files = sorted(
        p for p in src_root.rglob("*") if p.is_file()
    )

    for src_path in incoming_files:
        incoming = build_rom(src_path)
        action = plan_incoming(incoming, index)

        if action.kind == "move":
            action.dst = dest_root / incoming.name

        apply_action(action, dest_root, stats, execute)

        if not execute:
            continue

        if action.kind == "discard_incoming":
            if incoming.base_key in index:
                index[incoming.base_key] = [
                    r for r in index[incoming.base_key]
                    if r.path.resolve() != incoming.path.resolve()
                ]
            continue

        dst = action.dst if action.dst is not None else dest_root / incoming.name
        if dst.exists():
            new_rom = build_rom(dst)
            for old_path in action.delete_existing:
                refresh_index_entry(index, new_rom, remove=old_path)
            if not action.delete_existing:
                refresh_index_entry(index, new_rom)


def merge_emuelec(
    repo_root: Path,
    stats: MergeStats,
    execute: bool,
) -> None:
    src_base = repo_root / "resources" / "new-roms" / "roms"
    if not src_base.is_dir():
        print(f"AVISO: fonte ausente: {src_base}")
        return

    for entry in sorted(src_base.iterdir()):
        if not entry.is_dir():
            continue
        system = entry.name.casefold()
        band, canonical = emuelec_target(system)
        dest = resolve_dest(repo_root, band, canonical)
        print(f"  EmuELEC/{entry.name} -> {band}/{canonical}")
        merge_system_folder(entry, dest, stats, execute, f"emuelec:{entry.name}")


def merge_external(
    repo_root: Path,
    stats: MergeStats,
    execute: bool,
) -> None:
    if not EXTERNAL_LIBRARY.is_dir():
        print(f"AVISO: biblioteca externa ausente: {EXTERNAL_LIBRARY}")
        return

    for entry in sorted(EXTERNAL_LIBRARY.iterdir()):
        if not entry.is_dir():
            continue
        key = entry.name.upper()
        if key not in EXTERNAL_MAP:
            print(f"  AVISO: pasta externa nao mapeada, ignorada: {entry.name}")
            continue
        band, canonical = EXTERNAL_MAP[key]
        dest = resolve_dest(repo_root, band, canonical)
        print(f"  Externa/{entry.name} -> {band}/{canonical}")
        merge_system_folder(entry, dest, stats, execute, f"externa:{entry.name}")


def merge_bios(
    repo_root: Path,
    stats: MergeStats,
    execute: bool,
) -> None:
    src = repo_root / "resources" / "new-roms" / "BIOS"
    if not src.is_dir():
        print(f"AVISO: BIOS ausente: {src}")
        return
    dest = resolve_dest(repo_root, "bios", "")
    dest.mkdir(parents=True, exist_ok=True)
    print(f"  new-roms/BIOS -> bios/")

    for src_path in sorted(src.rglob("*")):
        if not src_path.is_file():
            continue
        rel = src_path.relative_to(src)
        dst = dest / rel
        if dst.exists():
            try:
                if dst.stat().st_size == src_path.stat().st_size:
                    stats.skipped_dup += 1
                    if execute:
                        src_path.unlink()
                    continue
            except OSError:
                pass
        stats.moved += 1
        stats.systems.add("bios")
        if execute:
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src_path), str(dst))
            except OSError as exc:
                stats.errors += 1
                print(f"ERRO BIOS {src_path}: {exc}")


def print_stats(stats: MergeStats, execute: bool) -> None:
    mode = "EXECUTADO" if execute else "SIMULACAO"
    print()
    print(f"=== RESUMO ({mode}) ===")
    print(f"Sistemas tocados: {len(stats.systems)}")
    print(f"Movidos: {stats.moved}")
    print(f"Descartados (origem inferior): {stats.discarded_incoming}")
    print(f"Substituiram existente: {stats.replaced_existing}")
    print(f"Duplicatas exatas ignoradas: {stats.skipped_dup}")
    print(f"Fontes vazias/placeholder: {stats.skipped_empty}")
    print(f"Erros: {stats.errors}")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Move ROMs de new-roms e biblioteca externa para resources/roms/. "
            "Dry-run por padrao."
        )
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Aplica movimentacoes (sem isto, so simula).",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Com --execute, nao pede confirmacao interativa.",
    )
    parser.add_argument(
        "--skip-external",
        action="store_true",
        help="Nao mover biblioteca externa (so new-roms).",
    )
    parser.add_argument(
        "--skip-emuelec",
        action="store_true",
        help="Nao mover new-roms/roms.",
    )
    parser.add_argument(
        "--skip-bios",
        action="store_true",
        help="Nao mover new-roms/BIOS.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    clear_screen()
    print_header()

    repo_root = find_repo_root(Path(__file__).resolve().parent)
    if repo_root is None:
        repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        print(f"ERRO: pasta '{REPO_FOLDER_NAME}' nao encontrada.")
        return 1

    print(f"REPO_ROOT={repo_root}")
    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"Modo: {mode}")
    print()

    if args.execute and not args.yes:
        confirm = prompt_yes_no(
            "Confirmar movimentacao permanente (origens esvaziadas)?",
            default=0,
        )
        if confirm != 1:
            print("Operacao cancelada pelo usuario.")
            return 0

    stats = MergeStats()
    do_apply = args.execute

    if not args.skip_emuelec:
        print("--- new-roms/roms (EmuELEC) ---")
        merge_emuelec(repo_root, stats, do_apply)

    if not args.skip_bios:
        print()
        print("--- new-roms/BIOS ---")
        merge_bios(repo_root, stats, do_apply)

    if not args.skip_external:
        print()
        print("--- biblioteca externa ---")
        merge_external(repo_root, stats, do_apply)

    print_stats(stats, do_apply)

    if not args.execute:
        print()
        print("Nada foi alterado (dry-run).")
        print("Para aplicar: python merge_roms.py --execute --yes")
        return 0

    print()
    print("Acao concluida: merge_roms")
    print(f"Diretorio raiz detectado: {repo_root}")
    return 1 if stats.errors else 0


if __name__ == "__main__":
    sys.exit(main())
