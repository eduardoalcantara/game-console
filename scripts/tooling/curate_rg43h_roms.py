#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
curate_rg43h_roms.py
game-console — curadoria RG43H: manifestos YAML -> staging EmuELEC (EEROMS).

Requer PyYAML opcional; fallback parser minimo incluido.
Dry-run por padrao. Nao altera resources/roms/android/ (so copia para staging).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from dedupe_roms import (  # noqa: E402
    RomFile,
    SKIP_SUFFIXES,
    build_rom,
    collect_roms,
    detect_region,
    find_repo_root,
    plan_group,
    prompt_yes_no,
)

REPO_FOLDER_NAME = "game-console"
STAGING_REL = Path("resources") / "rg43h" / "staging"
MANIFESTS_REL = Path("resources") / "rg43h" / "manifests"
SD_ORIGINAL_REL = Path("resources") / "rg43h" / "sd-original"
ANDROID_REL = Path("resources") / "roms" / "android"
BIOS_REL = Path("resources") / "roms" / "bios"

FAT32_LIMIT = 4 * 1024 * 1024 * 1024 - 1
COPY_CHUNK = 1024 * 1024
COPY_RETRIES = 3

MEDIA_SUFFIXES = ("-image.png", "-marquee.png", "-thumb.png", ".png", ".jpg")

# system arcade -> pastas PC
ARCADE_PC_SOURCES = ("mame", "fbneo")

REGION_RANK = {"USA": 3, "World": 2, "Japan": 2, "Europe": 1, "other": 0}


@dataclass
class GameEntry:
    base: str
    rom_set: Optional[str] = None
    region_prefer: List[str] = field(default_factory=list)
    include_all_regions: bool = False
    sd_folder: Optional[str] = None
    note: str = ""


@dataclass
class Manifest:
    path: Path
    system: str
    sd_folder: str
    tier: str
    games: List[GameEntry]


@dataclass
class MatchResult:
    manifest: str
    base: str
    status: str  # matched | missing | all_regions
    source: str = ""
    dest: str = ""
    size: int = 0


@dataclass
class CurateReport:
    matched: List[MatchResult] = field(default_factory=list)
    missing: List[MatchResult] = field(default_factory=list)
    by_sd_folder: Dict[str, int] = field(default_factory=dict)
    total_bytes: int = 0
    fat32_violations: List[str] = field(default_factory=list)
    copy_errors: List[str] = field(default_factory=list)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    print("game-console")
    print("Script: curate_rg43h_roms")
    print("Funcao: Curadoria RG43H (manifestos -> staging EmuELEC)")
    print("----------------------------------------")


def load_yaml_file(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return _parse_manifest_minimal(text)


def _parse_manifest_minimal(text: str) -> Dict[str, Any]:
    """Parser minimo para manifestos do repo (sem PyYAML)."""
    data: Dict[str, Any] = {"games": []}
    current_game: Optional[Dict[str, Any]] = None
    in_games = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "games:":
            in_games = True
            continue
        if not in_games:
            if line.startswith("- ") or ":" not in line:
                continue
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.lower() in ("true", "false"):
                data[key] = val.lower() == "true"
            elif val.isdigit():
                data[key] = int(val)
            else:
                data[key] = val
            continue
        if line.startswith("- base:"):
            if current_game:
                data["games"].append(current_game)
            val = line.split(":", 1)[1].strip().strip('"').strip("'")
            current_game = {"base": val}
            continue
        if current_game is not None and ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key == "include_all_regions":
                current_game[key] = val.lower() == "true"
            elif key == "region_prefer":
                current_game[key] = [
                    x.strip().strip('"').strip("'")
                    for x in val.strip("[]").split(",")
                    if x.strip()
                ]
            elif key in ("sd_folder", "note", "rom_set"):
                current_game[key] = val

    if current_game:
        data["games"].append(current_game)
    return data


def parse_manifest(path: Path) -> Manifest:
    data = load_yaml_file(path)
    games: List[GameEntry] = []
    for g in data.get("games") or []:
        if not isinstance(g, dict) or "base" not in g:
            continue
        games.append(
            GameEntry(
                base=str(g["base"]),
                rom_set=str(g["rom_set"]) if g.get("rom_set") else None,
                region_prefer=list(g.get("region_prefer") or []),
                include_all_regions=bool(g.get("include_all_regions")),
                sd_folder=g.get("sd_folder"),
                note=str(g.get("note") or ""),
            )
        )
    system = str(data.get("system") or path.stem)
    sd_folder = str(data.get("sd_folder") or system)
    tier = str(data.get("tier") or "?")
    return Manifest(path=path, system=system, sd_folder=sd_folder, tier=tier, games=games)


def is_rom_candidate(path: Path) -> bool:
    name = path.name
    lower = name.lower()
    if lower in ("desktop.ini", "thumbs.db"):
        return False
    if name.startswith("."):
        return False
    if path.suffix.lower() in SKIP_SUFFIXES:
        return False
    for suf in MEDIA_SUFFIXES:
        if lower.endswith(suf) and path.suffix.lower() in (".png", ".jpg", ".jpeg"):
            return False
    if re.search(r"-(?:image|marquee|thumb)\.(png|jpg|jpeg)$", lower):
        return False
    return path.is_file()


def collect_source_roms(source_roots: List[Path]) -> List[RomFile]:
    roms: List[RomFile] = []
    seen: Set[str] = set()
    for root in source_roots:
        if not root.is_dir():
            continue
        for r in collect_roms(root):
            key = str(r.path.resolve())
            if key not in seen:
                seen.add(key)
                roms.append(r)
    return roms


def matches_rom_set(rom: RomFile, rom_set: str) -> bool:
    return rom.stem.casefold() == rom_set.casefold()


def matches_base(rom: RomFile, base: str) -> bool:
    b = base.casefold()
    return b in rom.name.casefold() or b in rom.stem.casefold()


def matches_entry(rom: RomFile, entry: GameEntry) -> bool:
    if entry.rom_set:
        return matches_rom_set(rom, entry.rom_set)
    return matches_base(rom, entry.base)


def filter_by_region_prefer(candidates: List[RomFile], prefer: List[str]) -> List[RomFile]:
    if not prefer or not candidates:
        return candidates
    pref_cf = [p.casefold() for p in prefer]
    matched: List[RomFile] = []
    for rom in candidates:
        stem_cf = rom.stem.casefold()
        for p in pref_cf:
            if p in stem_cf or p in rom.region_label.casefold():
                matched.append(rom)
                break
    return matched if matched else candidates


def pick_roms_for_entry(
    entry: GameEntry,
    source_roms: List[RomFile],
) -> List[RomFile]:
    candidates = [r for r in source_roms if matches_entry(r, entry)]
    if not candidates:
        return []
    if entry.include_all_regions:
        return candidates
    candidates = filter_by_region_prefer(candidates, entry.region_prefer)
    deletes, keeper = plan_group(candidates)
    if keeper is None:
        return []
    return [keeper]


def resolve_pc_sources(manifest: Manifest, repo_root: Path) -> List[Path]:
    android_root = repo_root / ANDROID_REL
    if manifest.system == "arcade":
        return [android_root / s for s in ARCADE_PC_SOURCES]
    return [android_root / manifest.system]


def resolve_sd_folder(manifest: Manifest, entry: GameEntry) -> str:
    if entry.sd_folder:
        return entry.sd_folder
    return manifest.sd_folder


def copy_file(src: Path, dst: Path, execute: bool) -> bool:
    if not execute:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        src_size = src.stat().st_size
    except OSError as exc:
        print(f"ERRO stat origem: {src} ({exc})")
        return False
    if dst.is_file():
        try:
            if dst.stat().st_size == src_size:
                return True
        except OSError:
            pass
    for attempt in range(1, COPY_RETRIES + 1):
        try:
            with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                while True:
                    chunk = fsrc.read(COPY_CHUNK)
                    if not chunk:
                        break
                    fdst.write(chunk)
            try:
                shutil.copystat(src, dst)
            except OSError:
                pass
            return True
        except OSError as exc:
            if attempt < COPY_RETRIES:
                time.sleep(attempt)
                continue
            print(f"ERRO copia: {src} -> {dst} ({exc})")
            if dst.is_file():
                try:
                    dst.unlink()
                except OSError:
                    pass
            return False
    return False


def filter_gamelist(
    sd_original: Path,
    sd_folder: str,
    copied_filenames: Set[str],
    staging_system: Path,
    execute: bool,
) -> int:
    src_xml = sd_original / sd_folder / "gamelist.xml"
    if not src_xml.is_file() and sd_folder == "nes":
        alt = sd_original / "famicom" / "gamelist.xml"
        if alt.is_file():
            src_xml = alt
    if not src_xml.is_file():
        return 0
    try:
        raw = src_xml.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("gb2312", errors="replace")
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        print(f"AVISO: gamelist invalido {src_xml}: {exc}")
        return 0

    kept = 0
    for game in list(root.findall("game")):
        path_el = game.find("path")
        if path_el is None or not path_el.text:
            root.remove(game)
            continue
        fname = Path(path_el.text.replace("\\", "/")).name
        if fname not in copied_filenames:
            root.remove(game)
            continue
        kept += 1

    if kept == 0:
        return 0

    dst_xml = staging_system / "gamelist.xml"
    if execute:
        staging_system.mkdir(parents=True, exist_ok=True)
        ET.indent(root, space="  ")
        xml_body = ET.tostring(root, encoding="unicode")
        header = '<?xml version="1.0" encoding="UTF-8"?>\n'
        dst_xml.write_text(header + xml_body, encoding="utf-8")

    # Copiar imagens referenciadas
    src_images = sd_original / sd_folder / "images"
    if src_images.is_dir() and execute:
        dst_images = staging_system / "images"
        for game in root.findall("game"):
            img = game.find("image")
            if img is None or not img.text:
                continue
            img_name = Path(img.text.replace("\\", "/")).name
            src_img = src_images / img_name
            if src_img.is_file():
                copy_file(src_img, dst_images / img_name, True)
    return kept


def process_manifest(
    manifest: Manifest,
    repo_root: Path,
    staging: Path,
    sd_original: Path,
    report: CurateReport,
    execute: bool,
    copied_dest: Set[str],
) -> None:
    source_roots = resolve_pc_sources(manifest, repo_root)
    source_roms = collect_source_roms(source_roots)

    copied_by_folder: Dict[str, Set[str]] = {}

    for entry in manifest.games:
        sd_folder = resolve_sd_folder(manifest, entry)
        picked = pick_roms_for_entry(entry, source_roms)
        if not picked:
            report.missing.append(
                MatchResult(
                    manifest=manifest.path.name,
                    base=entry.base,
                    status="missing",
                )
            )
            continue

        for rom in picked:
            dest_dir = staging / sd_folder
            dest_file = dest_dir / rom.name
            dest_key = str(dest_file)
            if dest_key in copied_dest:
                continue
            copied_dest.add(dest_key)
            status = "all_regions" if entry.include_all_regions else "matched"
            report.matched.append(
                MatchResult(
                    manifest=manifest.path.name,
                    base=entry.base,
                    status=status,
                    source=str(rom.path),
                    dest=str(dest_file),
                    size=rom.size,
                )
            )
            report.total_bytes += rom.size
            report.by_sd_folder[sd_folder] = report.by_sd_folder.get(sd_folder, 0) + 1
            if rom.size > FAT32_LIMIT:
                report.fat32_violations.append(str(rom.path))
            copied_by_folder.setdefault(sd_folder, set()).add(rom.name)
            if not copy_file(rom.path, dest_file, execute):
                report.copy_errors.append(f"{rom.path} -> {dest_file}")
                copied_by_folder[sd_folder].discard(rom.name)
                copied_dest.discard(dest_key)

    for sd_folder, filenames in copied_by_folder.items():
        filter_gamelist(
            sd_original,
            sd_folder,
            filenames,
            staging / sd_folder,
            execute,
        )


def copy_bios_and_bezels(
    repo_root: Path,
    staging: Path,
    sd_original: Path,
    execute: bool,
) -> None:
    bios_src = repo_root / BIOS_REL
    if bios_src.is_dir():
        for root, _dirs, files in os.walk(bios_src):
            for name in files:
                src = Path(root) / name
                rel = src.relative_to(bios_src)
                copy_file(src, staging / "bios" / rel, execute)

    bezels_src = sd_original / "bezels"
    if bezels_src.is_dir():
        for root, _dirs, files in os.walk(bezels_src):
            for name in files:
                src = Path(root) / name
                rel = src.relative_to(bezels_src)
                copy_file(src, staging / "bezels" / rel, execute)

    neogeo_zip = repo_root / ANDROID_REL / "neogeo" / "neogeo.zip"
    if neogeo_zip.is_file():
        copy_file(neogeo_zip, staging / "neogeo" / "neogeo.zip", execute)


def write_reports(staging: Path, report: CurateReport, execute: bool) -> None:
    data = {
        "matched_count": len(report.matched),
        "missing_count": len(report.missing),
        "total_bytes": report.total_bytes,
        "by_sd_folder": report.by_sd_folder,
        "fat32_violations": report.fat32_violations,
        "copy_errors": report.copy_errors,
        "missing": [{"manifest": m.manifest, "base": m.base} for m in report.missing],
    }
    md_lines = [
        "# Relatorio curadoria RG43H",
        "",
        f"- Matched: **{len(report.matched)}**",
        f"- Missing: **{len(report.missing)}**",
        f"- Tamanho total: **{report.total_bytes / (1024**3):.2f} GB**",
        "",
        "## Por pasta SD",
        "",
    ]
    for folder, count in sorted(report.by_sd_folder.items()):
        md_lines.append(f"- `{folder}/`: {count} ROMs")
    if report.fat32_violations:
        md_lines.extend(["", "## ALERTA FAT32 (>4GB)", ""])
        for v in report.fat32_violations:
            md_lines.append(f"- {v}")
    if report.copy_errors:
        md_lines.extend(["", "## Erros de copia", ""])
        for v in report.copy_errors[:30]:
            md_lines.append(f"- {v}")
        if len(report.copy_errors) > 30:
            md_lines.append(f"- ... e mais {len(report.copy_errors) - 30}")
    if report.missing:
        md_lines.extend(["", "## Missing (primeiros 50)", ""])
        for m in report.missing[:50]:
            md_lines.append(f"- [{m.manifest}] `{m.base}`")
        if len(report.missing) > 50:
            md_lines.append(f"- ... e mais {len(report.missing) - 50}")

    if execute:
        staging.mkdir(parents=True, exist_ok=True)
        (staging / "manifest-report.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (staging / "manifest-report.md").write_text(
            "\n".join(md_lines) + "\n",
            encoding="utf-8",
        )
    print("\n".join(md_lines[:30]))
    if len(md_lines) > 30:
        print(f"... (+ {len(md_lines) - 30} linhas no relatorio completo)")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Curadoria RG43H -> staging EmuELEC")
    parser.add_argument("--manifest", type=str, default=None, help="Um manifesto YAML")
    parser.add_argument("--all", action="store_true", default=True, help="Todos manifestos")
    parser.add_argument(
        "--staging",
        type=str,
        default=None,
        help="Pasta staging (default: resources/rg43h/staging)",
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument(
        "--deploy",
        type=str,
        default=None,
        help="Letra/caminho SD apos staging (ex.: H:\\)",
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

    staging = Path(args.staging) if args.staging else repo_root / STAGING_REL
    sd_original = repo_root / SD_ORIGINAL_REL
    manifests_dir = repo_root / MANIFESTS_REL

    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"REPO_ROOT={repo_root}")
    print(f"Modo: {mode}")
    print(f"Staging: {staging}")
    print()

    if args.manifest:
        paths = [Path(args.manifest)]
        if not paths[0].is_absolute():
            paths = [repo_root / args.manifest]
    else:
        paths = sorted(manifests_dir.glob("*.yaml"))

    if not paths:
        print("ERRO: nenhum manifesto encontrado.")
        return 1

    if args.execute and not args.yes:
        if prompt_yes_no("Confirmar copia para staging?", default=0) != 1:
            print("Cancelado.")
            return 0

    report = CurateReport()
    copied_dest: Set[str] = set()
    for mp in paths:
        if not mp.is_file():
            print(f"AVISO: manifesto ausente: {mp}")
            continue
        print(f"Processando: {mp.name}")
        manifest = parse_manifest(mp)
        process_manifest(
            manifest, repo_root, staging, sd_original, report, args.execute, copied_dest
        )

    copy_bios_and_bezels(repo_root, staging, sd_original, args.execute)

    if args.execute:
        (staging / ".firstDownload").write_bytes(b"")

    write_reports(staging, report, args.execute)

    print()
    print(f"Matched: {len(report.matched)} | Missing: {len(report.missing)}")
    print(f"Total: {report.total_bytes / (1024**3):.2f} GB")
    if report.fat32_violations:
        print(f"ALERTA: {len(report.fat32_violations)} ficheiro(s) > 4GB (FAT32)")
        return 1
    if report.copy_errors:
        print(f"ERRO: {len(report.copy_errors)} falha(s) de copia (ver manifest-report)")
        return 1

    if args.deploy and args.execute:
        deploy_path = Path(args.deploy)
        print(f"Deploy para {deploy_path} — usar deploy_rg43h_sd.ps1")
        print(f"  robocopy \"{staging}\" \"{deploy_path}\" /E /R:2 /W:5")

    print(f"Diretorio raiz detectado: {repo_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
