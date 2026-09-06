#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_esde_media_rg43h.py
game-console — copia capas/metadados do ES-DE PC para layout EmuELEC (RG43H).

Fonte: resources/es-de/downloaded_media/<sistema>/{covers,miximages,...}/
Destino: core/rg43h-pro/staging/<sistema>/images/ + gamelist.xml

Dry-run por padrao. --execute --yes para aplicar.
--uninstall remove images/ e gamelist.xml gerados nos sistemas processados.
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
from typing import Dict, List, Optional, Set, Tuple

from dedupe_roms import find_repo_root, prompt_yes_no  # noqa: E402

REPO_FOLDER_NAME = "game-console"
STAGING_REL = Path("core") / "rg43h-pro" / "staging"
ESDE_MEDIA_REL = Path("resources") / "es-de" / "downloaded_media"

COPY_CHUNK = 1024 * 1024
COPY_RETRIES = 3

# Preferencia de media para tag <image> do EmuELEC
MEDIA_PREF = ("covers", "miximages", "screenshots", "3dboxes", "titlescreens", "marquees")

ROM_EXTS = {
    ".smc",
    ".sfc",
    ".nes",
    ".unf",
    ".gb",
    ".gbc",
    ".gba",
    ".md",
    ".gen",
    ".bin",
    ".sms",
    ".gg",
    ".pce",
    ".cue",
    ".chd",
    ".pbp",
    ".cso",
    ".iso",
    ".z64",
    ".n64",
    ".v64",
    ".zip",
    ".7z",
}

SKIP_NAMES = {"gamelist.xml", "desktop.ini", "thumbs.db", "neogeo.zip", ".firstdownload"}

# Pasta SD -> pasta ES-DE downloaded_media
SYSTEM_MAP = {
    "snes": "snes",
    "megadrive": "megadrive",
    "nes": "nes",
    "gba": "gba",
    "gbc": "gbc",
    "gb": "gb",
    "mastersystem": "mastersystem",
    "pcengine": "pcengine",
    "mame": "mame",
    "cps1": "mame",
    "neogeo": "mame",  # fallback fraco; muitas capas MAME/FBNeo
}

# Remove tags No-Intro / dump entre () ou []
TAG_RE = re.compile(r"\s*[\(\[][^\)\]]*[\)\]]")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


@dataclass
class MediaHit:
    rom_name: str
    rom_stem: str
    media_src: Path
    media_kind: str
    match_how: str


@dataclass
class SystemReport:
    system: str
    roms: int = 0
    matched: int = 0
    missing: List[str] = field(default_factory=list)
    hits: List[MediaHit] = field(default_factory=list)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    print("game-console")
    print("Script: apply_esde_media_rg43h")
    print("Funcao: Capas ES-DE -> staging/SD EmuELEC (RG43H)")
    print("----------------------------------------")


def normalize_key(name: str) -> str:
    stem = Path(name).stem
    stem = TAG_RE.sub("", stem)
    stem = stem.replace(", The", "").replace(", the", "")
    if stem.casefold().startswith("the "):
        stem = stem[4:]
    stem = stem.casefold().strip()
    return NON_ALNUM_RE.sub("", stem)


def copy_file(src: Path, dst: Path, execute: bool) -> bool:
    if not execute:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        src_size = src.stat().st_size
    except OSError as exc:
        print(f"ERRO stat: {src} ({exc})")
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


def index_esde_media(media_root: Path) -> Dict[str, List[Tuple[str, Path]]]:
    """
    Retorna map normalize_key -> [(kind, path), ...] ordenado por preferencia.
    """
    by_key: Dict[str, List[Tuple[str, Path]]] = {}
    if not media_root.is_dir():
        return by_key
    for kind in MEDIA_PREF:
        kind_dir = media_root / kind
        if not kind_dir.is_dir():
            continue
        for path in kind_dir.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
                continue
            # Ignorar placeholders de letra tipo A.png na raiz da pasta covers
            if path.parent == kind_dir and len(path.stem) <= 2:
                continue
            key = normalize_key(path.name)
            if not key:
                continue
            by_key.setdefault(key, []).append((kind, path))
            # Tambem indexar stem exacto (com tags) para match exacto
            exact = path.stem.casefold()
            by_key.setdefault(f"exact:{exact}", []).append((kind, path))
    return by_key


def list_roms(system_dir: Path) -> List[Path]:
    roms: List[Path] = []
    if not system_dir.is_dir():
        return roms
    for path in system_dir.iterdir():
        if not path.is_file():
            continue
        if path.name.lower() in SKIP_NAMES:
            continue
        if path.name.startswith("."):
            continue
        if path.suffix.lower() not in ROM_EXTS:
            continue
        roms.append(path)
    return sorted(roms, key=lambda p: p.name.casefold())


def pick_media(
    rom: Path, index: Dict[str, List[Tuple[str, Path]]]
) -> Optional[Tuple[str, Path, str]]:
    exact_key = f"exact:{rom.stem.casefold()}"
    if exact_key in index:
        kind, path = index[exact_key][0]
        return kind, path, "exact_stem"
    key = normalize_key(rom.name)
    if key and key in index:
        kind, path = index[key][0]
        return kind, path, "normalized"
    # Fallback: media cujo stem normalizado e prefixo/contido (cuidado com falsos)
    if key and len(key) >= 6:
        candidates: List[Tuple[int, str, Path]] = []
        for k, items in index.items():
            if k.startswith("exact:"):
                continue
            if k == key:
                continue
            if key.startswith(k) or k.startswith(key):
                kind, path = items[0]
                score = min(len(k), len(key))
                candidates.append((score, kind, path))
        if candidates:
            candidates.sort(key=lambda x: -x[0])
            score, kind, path = candidates[0]
            if score >= 6:
                return kind, path, f"prefix({score})"
    return None


def display_name(rom_stem: str) -> str:
    name = TAG_RE.sub("", rom_stem).strip()
    return name or rom_stem


def process_system(
    system: str,
    staging: Path,
    esde_root: Path,
    execute: bool,
) -> SystemReport:
    report = SystemReport(system=system)
    esde_name = SYSTEM_MAP.get(system, system)
    media_root = esde_root / esde_name
    system_dir = staging / system
    roms = list_roms(system_dir)
    report.roms = len(roms)
    if not roms:
        return report
    if not media_root.is_dir():
        report.missing = [r.name for r in roms]
        print(f"  AVISO: sem media ES-DE para '{esde_name}' ({system}/)")
        return report

    index = index_esde_media(media_root)
    images_dir = system_dir / "images"
    for rom in roms:
        picked = pick_media(rom, index)
        if not picked:
            report.missing.append(rom.name)
            continue
        kind, src, how = picked
        dst = images_dir / f"{rom.stem}.png"
        # Se origem nao e png, ainda assim gravamos com .png no path ES
        # (EmuELEC aceita png; se jpg, manter extensao real e ajustar gamelist)
        if src.suffix.lower() != ".png":
            dst = images_dir / f"{rom.stem}{src.suffix.lower()}"
        ok = copy_file(src, dst, execute)
        if not ok and execute:
            report.missing.append(rom.name)
            continue
        hit = MediaHit(
            rom_name=rom.name,
            rom_stem=rom.stem,
            media_src=src,
            media_kind=kind,
            match_how=how,
        )
        # Ajustar path da imagem no hit se extensao != png
        if dst.suffix.lower() != ".png":
            # gamelist usara extensao real — patch via atributo extra no write
            hit.rom_stem = rom.stem  # image name base
        report.hits.append(hit)
        report.matched += 1

    # gamelist: image path com extensao real
    if report.hits:
        root = ET.Element("gameList")
        for hit in report.hits:
            # descobrir extensao destino
            img_png = images_dir / f"{hit.rom_stem}.png"
            img_jpg = images_dir / f"{hit.rom_stem}.jpg"
            img_jpeg = images_dir / f"{hit.rom_stem}.jpeg"
            img_webp = images_dir / f"{hit.rom_stem}.webp"
            if execute:
                if img_png.is_file():
                    img_rel = f"./images/{hit.rom_stem}.png"
                elif img_jpg.is_file():
                    img_rel = f"./images/{hit.rom_stem}.jpg"
                elif img_jpeg.is_file():
                    img_rel = f"./images/{hit.rom_stem}.jpeg"
                elif img_webp.is_file():
                    img_rel = f"./images/{hit.rom_stem}.webp"
                else:
                    img_rel = f"./images/{hit.rom_stem}.png"
            else:
                ext = hit.media_src.suffix.lower() or ".png"
                img_rel = f"./images/{hit.rom_stem}{ext}"
            game = ET.SubElement(root, "game")
            ET.SubElement(game, "path").text = f"./{hit.rom_name}"
            ET.SubElement(game, "name").text = display_name(hit.rom_stem)
            ET.SubElement(game, "image").text = img_rel
        if execute:
            system_dir.mkdir(parents=True, exist_ok=True)
            ET.indent(root, space="  ")
            body = ET.tostring(root, encoding="unicode")
            (system_dir / "gamelist.xml").write_text(
                '<?xml version="1.0" encoding="UTF-8"?>\n' + body + "\n",
                encoding="utf-8",
            )
            marker = system_dir / ".esde-media-applied"
            marker.write_text(
                "apply_esde_media_rg43h.py\n",
                encoding="utf-8",
            )
    return report


def uninstall_systems(staging: Path, systems: List[str], execute: bool) -> None:
    for system in systems:
        system_dir = staging / system
        images = system_dir / "images"
        gamelist = system_dir / "gamelist.xml"
        marker = system_dir / ".esde-media-applied"
        print(f"Uninstall {system}/images + gamelist.xml")
        if not execute:
            continue
        if images.is_dir():
            shutil.rmtree(images, ignore_errors=True)
        if gamelist.is_file():
            gamelist.unlink()
        if marker.is_file():
            marker.unlink()


def write_report(staging: Path, reports: List[SystemReport], execute: bool) -> None:
    total_roms = sum(r.roms for r in reports)
    total_matched = sum(r.matched for r in reports)
    total_missing = sum(len(r.missing) for r in reports)
    data = {
        "total_roms": total_roms,
        "matched": total_matched,
        "missing": total_missing,
        "systems": {
            r.system: {
                "roms": r.roms,
                "matched": r.matched,
                "missing_count": len(r.missing),
                "missing": r.missing[:100],
            }
            for r in reports
        },
    }
    lines = [
        "# Relatorio midia ES-DE -> RG43H",
        "",
        f"- ROMs analisadas: **{total_roms}**",
        f"- Com capa: **{total_matched}**",
        f"- Sem capa: **{total_missing}**",
        "",
        "## Por sistema",
        "",
    ]
    for r in reports:
        lines.append(
            f"- `{r.system}/`: {r.matched}/{r.roms} capas"
            + (f" (faltam {len(r.missing)})" if r.missing else "")
        )
    if total_missing:
        lines.extend(["", "## Missing (amostra)", ""])
        shown = 0
        for r in reports:
            for name in r.missing:
                lines.append(f"- [{r.system}] `{name}`")
                shown += 1
                if shown >= 80:
                    break
            if shown >= 80:
                break
        if total_missing > shown:
            lines.append(f"- ... e mais {total_missing - shown}")
    lines.extend(
        [
            "",
            "## Notas",
            "",
            "- Media ES-DE pode estar parcialmente sincronizada no Google Drive (so pastas A-E).",
            "- Preferencia de imagem: covers > miximages > screenshots > 3dboxes > titlescreens > marquees.",
            "- No RG43H RGBox o scrape in-device esta indisponivel; este script e o caminho suportado.",
            "",
        ]
    )
    text = "\n".join(lines)
    print(text)
    if execute:
        staging.mkdir(parents=True, exist_ok=True)
        (staging / "media-report.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (staging / "media-report.md").write_text(text, encoding="utf-8")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Capas ES-DE -> staging RG43H EmuELEC")
    p.add_argument(
        "--system",
        action="append",
        default=None,
        help="Sistema SD (ex.: snes). Repetivel. Default: todos com ROMs no staging e mapa ES-DE",
    )
    p.add_argument("--staging", type=str, default=None)
    p.add_argument("--esde-media", type=str, default=None)
    p.add_argument("--execute", action="store_true")
    p.add_argument("--yes", action="store_true")
    p.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove images/ + gamelist.xml aplicados por este script",
    )
    p.add_argument(
        "--deploy",
        type=str,
        default=None,
        help="Apos execute, robocopy sistemas tocados para este destino (ex.: H:\\)",
    )
    return p.parse_args(argv)


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
    esde_root = (
        Path(args.esde_media) if args.esde_media else repo_root / ESDE_MEDIA_REL
    )

    print(f"REPO_ROOT={repo_root}")
    print(f"Staging: {staging}")
    print(f"ES-DE media: {esde_root}")
    mode = "UNINSTALL" if args.uninstall else ("EXECUTE" if args.execute else "DRY-RUN")
    print(f"Modo: {mode}")
    print()

    if not staging.is_dir():
        print("ERRO: staging nao encontrado. Rode curate_rg43h_roms.py --execute --yes antes.")
        return 1

    if args.system:
        systems = args.system
    else:
        systems = []
        for child in sorted(staging.iterdir()):
            if child.is_dir() and child.name in SYSTEM_MAP:
                if list_roms(child):
                    systems.append(child.name)

    if not systems:
        print("ERRO: nenhum sistema com ROMs para processar.")
        return 1

    print("Sistemas:", ", ".join(systems))
    print()

    if args.execute and not args.yes:
        q = "Confirmar uninstall de midia?" if args.uninstall else "Confirmar copia de capas para staging?"
        if prompt_yes_no(q, default=0) != 1:
            print("Cancelado.")
            return 0

    if args.uninstall:
        uninstall_systems(staging, systems, args.execute)
        print("Acao concluida: uninstall midia ES-DE")
        print(f"Diretorio raiz detectado: {repo_root}")
        return 0

    reports: List[SystemReport] = []
    for system in systems:
        print(f"Processando: {system}")
        reports.append(process_system(system, staging, esde_root, args.execute))

    write_report(staging, reports, args.execute)

    if args.deploy and args.execute:
        deploy = Path(args.deploy)
        if not deploy.exists():
            print(f"AVISO: deploy {deploy} indisponivel (cartao nao montado?).")
        else:
            print(f"Deploy midia -> {deploy}")
            for r in reports:
                if r.matched == 0:
                    continue
                src = staging / r.system
                dst = deploy / r.system
                # Copia images + gamelist
                cmd = f'robocopy "{src}" "{dst}" gamelist.xml /R:2 /W:5 /NFL /NDL /NJH /NJS /nc /ns /np'
                os.system(cmd)
                img_src = src / "images"
                if img_src.is_dir():
                    cmd = (
                        f'robocopy "{img_src}" "{dst / "images"}" '
                        f"/E /R:2 /W:5 /NFL /NDL /NJH /NJS /nc /ns /np"
                    )
                    os.system(cmd)

    print(f"Diretorio raiz detectado: {repo_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
