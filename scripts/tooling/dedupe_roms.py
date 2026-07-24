#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedupe_roms.py
game-console — remove duplicatas de ROMs (No-Intro / Redump) por prioridade
de regiao e revisao. Dry-run por padrao.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

REPO_FOLDER_NAME = "game-console"
DEFAULT_REL_ROMS = Path("resources") / "roms" / "android"

# Tags entre parenteses ou colchetes: (USA), [b1], etc.
TAG_RE = re.compile(r"[\(\[][^\)\]]+[\)\]]")

# Revisoes comuns No-Intro / dumps
REV_RE = re.compile(
    r"(?i)(?:^|[\(\[\s,_-])(?:Rev(?:ision)?\s*([0-9A-Z]+)|v(\d+(?:\.\d+)*))(?:[\)\]\s,_-]|$)"
)

# Protecao: nunca excluir customizacoes / traducoes / hacks
# "Tr" so em forma de tag para nao casar com "Street"
PROTECT_RE = re.compile(
    r"(?i)("
    r"PT-BR|"
    r"Undub|"
    r"Translated|"
    r"T-En|"
    r"\bHack\b|"
    r"\bMod\b|"
    r"[\(\[]\s*Tr\s*[\)\]]|"
    r"(?:^|[\s_\-])Tr(?:$|[\s_\-])"
    r")"
)

# Regiao USA (prioridade maxima), inclusive combinacoes com USA
USA_RE = re.compile(
    r"(?i)\((?:USA|US|U)(?:\s*,\s*[^)]+)?|(?:[^)]+,\s*)?(?:USA|US)\)"
)
# Forma explicita pedida: (USA, Europe)
USA_EUROPE_RE = re.compile(r"(?i)\(USA\s*,\s*Europe\)")

EUROPE_RE = re.compile(
    r"(?i)\((?:Europe|EUR|EU|E)(?:\s*,\s*[^)]+)?|(?:[^)]+,\s*)?(?:Europe|EUR)\)"
)
# Evitar marcar (USA, Europe) so como Europe
EUROPE_ONLY_HINT = re.compile(r"(?i)\b(?:Europe|EUR|EU)\b")

JAPAN_RE = re.compile(
    r"(?i)\((?:Japan|JAP|JP|J)(?:\s*,\s*[^)]+)?|(?:[^)]+,\s*)?(?:Japan|JAP|JP)\)"
)

WORLD_RE = re.compile(r"(?i)\(World\)")

SKIP_NAMES = {"desktop.ini", "thumbs.db", ".ds_store"}

# Companions / saves / patches — nunca entram no dedupe de ROM
SKIP_SUFFIXES = {
    ".srm",
    ".sav",
    ".rtc",
    ".mcr",
    ".mcs",
    ".psv",
    ".sra",
    ".hi",
    ".cfg",
    ".txt",
    ".nfo",
    ".ips",
    ".bps",
    ".ups",
    ".cht",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".bmp",
    ".lnk",
    ".url",
    ".bat",
    ".cmd",
    ".ico",
    ".ss0",
    ".ss1",
    ".ss2",
}


# ---------------------------------------------------------------------------
# Modelos
# ---------------------------------------------------------------------------

@dataclass
class RomFile:
    path: Path
    name: str
    stem: str
    suffix: str
    base_key: str
    protected: bool
    region_rank: int  # 3=USA, 2=Japan, 1=Europe, 0=other/unknown
    region_label: str
    revision: Tuple[int, ...]
    revision_label: str
    size: int


@dataclass
class Plan:
    deletes: List[Tuple[Path, str]] = field(default_factory=list)
    renames: List[Tuple[Path, Path, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# UX / raiz do repo
# ---------------------------------------------------------------------------

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    print("game-console")
    print("Script: dedupe_roms")
    print("Funcao: Eliminar ROMs duplicadas por regiao/revisao (dry-run padrao)")
    print("----------------------------------------")


def find_repo_root(start: Path) -> Optional[Path]:
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if candidate.name.lower() == REPO_FOLDER_NAME:
            return candidate
    return None


def prompt_yes_no(question: str, default: int = 0) -> int:
    """0 = nao, 1 = sim. Enter = default documentado."""
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


# ---------------------------------------------------------------------------
# Parsing de nomes
# ---------------------------------------------------------------------------

def base_key_from_stem(stem: str) -> str:
    """Nome base para agrupamento: remove tags ()/[] e normaliza espacos."""
    cleaned = TAG_RE.sub("", stem)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = cleaned.rstrip(" -_.")
    return cleaned.casefold()


def is_protected(name: str) -> bool:
    return PROTECT_RE.search(name) is not None


def detect_region(stem: str) -> Tuple[int, str]:
    """
    Retorna (rank, label).
    3 = USA / USA,Europe / qualquer tag com USA
    2 = Japan (sem USA)
    1 = Europe (sem USA)
    0 = outras / World / sem tag
    """
    if USA_EUROPE_RE.search(stem) or USA_RE.search(stem):
        # (Japan, USA) e (USA, Europe) caem aqui — USA vence
        if USA_EUROPE_RE.search(stem):
            return 3, "USA,Europe"
        return 3, "USA"
    if JAPAN_RE.search(stem):
        return 2, "Japan"
    if EUROPE_RE.search(stem) or (
        EUROPE_ONLY_HINT.search(stem) and not USA_RE.search(stem)
    ):
        return 1, "Europe"
    if WORLD_RE.search(stem):
        return 0, "World"
    return 0, "other"


def parse_revision(stem: str) -> Tuple[Tuple[int, ...], str]:
    """
    Extrai a maior revisao encontrada.
    Rev 1 / Rev A / v1.1 -> tupla comparavel. Sem revisao -> (0,).
    """
    best: Tuple[int, ...] = (0,)
    label = "base"

    for match in REV_RE.finditer(stem):
        rev_token, ver_token = match.group(1), match.group(2)
        if rev_token:
            token = rev_token.upper()
            parts: List[int] = []
            # Rev A -> 10, Rev B -> 11 (apos digitos)
            if token.isdigit():
                parts = [int(token)]
            elif re.fullmatch(r"[A-Z]", token):
                parts = [ord(token) - ord("A") + 10]
            else:
                # Rev 1A etc.: separa digitos e letra final
                m = re.match(r"(\d+)([A-Z]?)$", token)
                if m:
                    parts = [int(m.group(1))]
                    if m.group(2):
                        parts.append(ord(m.group(2)) - ord("A") + 10)
                else:
                    parts = [0]
            current = tuple(parts)
            text = f"Rev {rev_token}"
        else:
            nums = tuple(int(x) for x in ver_token.split("."))
            current = nums
            text = f"v{ver_token}"

        if current > best:
            best = current
            label = text

    return best, label


def build_rom(path: Path) -> RomFile:
    name = path.name
    stem = path.stem
    rank, region_label = detect_region(stem)
    rev, rev_label = parse_revision(stem)
    try:
        size = path.stat().st_size
    except OSError:
        size = 0
    return RomFile(
        path=path,
        name=name,
        stem=stem,
        suffix=path.suffix,
        base_key=base_key_from_stem(stem),
        protected=is_protected(name),
        region_rank=rank,
        region_label=region_label,
        revision=rev,
        revision_label=rev_label,
        size=size,
    )


# ---------------------------------------------------------------------------
# Coleta e plano
# ---------------------------------------------------------------------------

def collect_roms(root: Path) -> List[RomFile]:
    roms: List[RomFile] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower() in SKIP_NAMES:
                continue
            if filename.startswith("."):
                continue
            path = Path(dirpath) / filename
            if path.suffix.lower() in SKIP_SUFFIXES:
                continue
            if not path.is_file():
                continue
            try:
                # Garante leitura basica (Google Drive / permissao)
                path.stat()
            except OSError as exc:
                print(f"AVISO: ignorando (sem acesso): {path} ({exc})")
                continue
            roms.append(build_rom(path))
    return roms


def choose_keeper(candidates: List[RomFile]) -> RomFile:
    """Maior revisao; empate = maior arquivo; empate = nome lexicografico menor."""
    best_key = max((r.revision, r.size) for r in candidates)
    top = [r for r in candidates if (r.revision, r.size) == best_key]
    return min(top, key=lambda r: r.name.casefold())


def plan_group(group: List[RomFile]) -> Tuple[List[Tuple[Path, str]], Optional[RomFile]]:
    """
    Aplica regras de regiao + revisao no grupo (excluindo protegidos).
    Retorna lista de (path, motivo) a apagar e o keeper principal (se houver).
    """
    protected = [r for r in group if r.protected]
    normal = [r for r in group if not r.protected]

    deletes: List[Tuple[Path, str]] = []

    if not normal:
        # So protegidos / custom — nada a fazer
        return deletes, None

    has_usa = any(r.region_rank == 3 for r in normal)
    has_japan = any(r.region_rank == 2 for r in normal)

    eligible: List[RomFile] = []
    for rom in normal:
        if has_usa:
            if rom.region_rank == 3:
                eligible.append(rom)
            else:
                deletes.append(
                    (
                        rom.path,
                        f"regiao {rom.region_label} inferior a USA "
                        f"(grupo tem versao USA)",
                    )
                )
        elif has_japan:
            if rom.region_rank == 2:
                eligible.append(rom)
            elif rom.region_rank == 1:
                deletes.append(
                    (
                        rom.path,
                        f"regiao Europe inferior a Japan "
                        f"(grupo sem USA, com Japan)",
                    )
                )
            else:
                # other/World com Japan presente: manter so Japan
                deletes.append(
                    (
                        rom.path,
                        f"regiao {rom.region_label} descartada "
                        f"(grupo sem USA, com Japan)",
                    )
                )
        else:
            # Sem USA e sem Japan: manter Europe e others; depois revisao decide
            eligible.append(rom)

    if not eligible:
        return deletes, None

    # Entre elegiveis da mesma "faixa" vencedora, se houver mistura
    # USA-only ja filtrado. Se so Europe/other, filtrar pela melhor faixa presente.
    max_rank = max(r.region_rank for r in eligible)
    top = [r for r in eligible if r.region_rank == max_rank]
    for rom in eligible:
        if rom.region_rank < max_rank:
            deletes.append(
                (
                    rom.path,
                    f"regiao {rom.region_label} inferior a rank {max_rank} "
                    f"no grupo elegivel",
                )
            )

    keeper = choose_keeper(top)
    for rom in top:
        if rom.path == keeper.path:
            continue
        deletes.append(
            (
                rom.path,
                f"revisao {rom.revision_label} inferior ou empate "
                f"(mantida: {keeper.name} / {keeper.revision_label})",
            )
        )

    # Protegidos nunca entram em deletes
    _ = protected
    return deletes, keeper


def strip_usa_suffix(stem: str) -> str:
    """Remove o sufixo literal ' (USA)' (e variantes proximas USA-only)."""
    # Pedido: retirar " (USA)". Tambem cobre " (USA, Europe)" se for unica tag USA.
    new_stem = re.sub(r"(?i)\s*\(USA\)", "", stem)
    new_stem = re.sub(r"\s+", " ", new_stem).strip()
    return new_stem


def build_plan(roms: List[RomFile]) -> Plan:
    plan = Plan()
    groups: Dict[Tuple[str, str], List[RomFile]] = defaultdict(list)

    # Agrupa por pasta pai + nome base (nao misturar SNES com Mega Drive)
    for rom in roms:
        parent_key = str(rom.path.parent.resolve())
        groups[(parent_key, rom.base_key)].append(rom)

    for (_parent, _base), group in groups.items():
        deletes, keeper = plan_group(group)
        plan.deletes.extend(deletes)

        if keeper is None:
            continue

        # Regra 6: unica versao nao-protegida restante e USA -> remover " (USA)"
        delete_set = {p for p, _ in deletes}
        normal_survivors = [
            r for r in group if (not r.protected) and (r.path not in delete_set)
        ]

        if len(normal_survivors) == 1 and keeper.path == normal_survivors[0].path:
            if re.search(r"(?i)\s*\(USA\)", keeper.stem):
                new_stem = strip_usa_suffix(keeper.stem)
                if new_stem and new_stem != keeper.stem:
                    new_path = keeper.path.with_name(new_stem + keeper.suffix)
                    if new_path.exists() and new_path.resolve() != keeper.path.resolve():
                        # Evita colisao com arquivo ja existente
                        continue
                    if new_path != keeper.path:
                        plan.renames.append(
                            (
                                keeper.path,
                                new_path,
                                'remover sufixo " (USA)" (unica versao restante)',
                            )
                        )

    return plan


# ---------------------------------------------------------------------------
# Execucao
# ---------------------------------------------------------------------------

def print_plan(plan: Plan, root: Path) -> None:
    print()
    print(f"Raiz analisada: {root}")
    print(f"Arquivos a apagar: {len(plan.deletes)}")
    print(f"Arquivos a renomear: {len(plan.renames)}")
    print()

    if plan.deletes:
        print("=== DELECOES ===")
        for path, reason in sorted(plan.deletes, key=lambda x: str(x[0]).casefold()):
            try:
                rel = path.relative_to(root)
            except ValueError:
                rel = path
            print(f"APAGAR: {rel}")
            print(f"  motivo: {reason}")
        print()

    if plan.renames:
        print("=== RENOMEACOES ===")
        for src, dst, reason in sorted(
            plan.renames, key=lambda x: str(x[0]).casefold()
        ):
            try:
                rel_s = src.relative_to(root)
                rel_d = dst.relative_to(root)
            except ValueError:
                rel_s, rel_d = src, dst
            print(f"RENOMEAR: {rel_s}")
            print(f"      ->  {rel_d}")
            print(f"  motivo: {reason}")
        print()

    if not plan.deletes and not plan.renames:
        print("Nenhuma acao necessaria.")


def apply_plan(plan: Plan) -> Tuple[int, int, int]:
    """Retorna (deletados, renomeados, erros)."""
    deleted = 0
    renamed = 0
    errors = 0

    # Apagar primeiro (evita conflito de nome em renomeacoes futuras)
    for path, reason in plan.deletes:
        try:
            path.unlink()
            deleted += 1
            print(f"OK apagado: {path.name} ({reason})")
        except PermissionError as exc:
            errors += 1
            print(f"ERRO permissao ao apagar {path}: {exc}")
        except OSError as exc:
            errors += 1
            print(f"ERRO ao apagar {path}: {exc}")

    for src, dst, reason in plan.renames:
        try:
            if not src.exists():
                # Pode ter sido apagado por engano — nao deveria
                print(f"AVISO: origem ausente para renomear: {src}")
                errors += 1
                continue
            if dst.exists():
                print(f"ERRO: destino ja existe, renomeacao abortada: {dst}")
                errors += 1
                continue
            src.rename(dst)
            renamed += 1
            print(f"OK renomeado: {src.name} -> {dst.name} ({reason})")
        except PermissionError as exc:
            errors += 1
            print(f"ERRO permissao ao renomear {src}: {exc}")
        except OSError as exc:
            errors += 1
            print(f"ERRO ao renomear {src}: {exc}")

    return deleted, renamed, errors


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Elimina ROMs duplicadas por regiao/revisao. "
            "Dry-run por padrao; use --execute para aplicar."
        )
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help=(
            "Pasta raiz da biblioteca (default: "
            "<REPO_ROOT>/resources/roms/android)"
        ),
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Aplica delecoes e renomeacoes (sem isto, so simula).",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Com --execute, nao pede confirmacao interativa.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    clear_screen()
    print_header()

    script_path = Path(__file__).resolve()
    repo_root = find_repo_root(script_path.parent)
    if repo_root is None:
        repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        print(
            "ERRO: nao foi possivel localizar a raiz do repositorio "
            f"(pasta '{REPO_FOLDER_NAME}')."
        )
        return 1

    print(f"REPO_ROOT={repo_root}")

    if args.root:
        root = Path(args.root).expanduser()
        if not root.is_absolute():
            root = (Path.cwd() / root).resolve()
        else:
            root = root.resolve()
    else:
        root = (repo_root / DEFAULT_REL_ROMS).resolve()

    if not root.is_dir():
        print(f"ERRO: pasta de ROMs nao encontrada: {root}")
        return 1

    mode = "EXECUTE" if args.execute else "DRY-RUN (simulacao)"
    print(f"Modo: {mode}")
    print(f"Biblioteca: {root}")
    print()

    print("Coletando arquivos...")
    try:
        roms = collect_roms(root)
    except OSError as exc:
        print(f"ERRO ao percorrer a biblioteca: {exc}")
        return 1

    print(f"Arquivos considerados: {len(roms)}")
    protected_n = sum(1 for r in roms if r.protected)
    print(f"Protegidos (hack/traducao/mod): {protected_n}")

    plan = build_plan(roms)
    print_plan(plan, root)

    if not args.execute:
        print(
            "Nada foi alterado (dry-run). "
            "Para aplicar: python dedupe_roms.py --execute"
        )
        print(f"Diretorio raiz detectado: {repo_root}")
        return 0

    if not plan.deletes and not plan.renames:
        print("Nada a aplicar.")
        return 0

    if not args.yes:
        confirm = prompt_yes_no(
            "Confirmar exclusao/renomeacao permanentes?",
            default=0,
        )
        if confirm != 1:
            print("Operacao cancelada pelo usuario.")
            return 0

    deleted, renamed, errors = apply_plan(plan)
    print()
    print("Acao concluida: dedupe_roms")
    print(f"Diretorio raiz detectado: {repo_root}")
    print(f"Apagados: {deleted} | Renomeados: {renamed} | Erros: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
