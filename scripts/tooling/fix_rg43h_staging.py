#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_rg43h_staging.py
Ajusta BIOS e correcoes de ROMs PSX/NeoGeo no staging do RG43H.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from dedupe_roms import find_repo_root


def main() -> int:
    repo_root = find_repo_root(Path(__file__).resolve().parent)
    if repo_root is None:
        print("ERRO: pasta game-console nao encontrada.")
        return 1

    staging = repo_root / "core" / "rg43h-pro" / "staging"
    bios_staging = staging / "bios"
    neogeo_staging = staging / "neogeo"
    psx_staging = staging / "psx"

    # 1. BIOS essenciais na raiz de staging/bios/
    bios_src = repo_root / "resources" / "roms" / "bios"
    flatten_count = 0
    for sub in ["várias do honda", "PS1", "ps2 do honda", "PS2"]:
        sub_dir = bios_src / sub
        if sub_dir.is_dir():
            for root, _dirs, files in os.walk(sub_dir):
                for f in files:
                    ext = Path(f).suffix.lower()
                    if ext in {".bin", ".rom", ".pce", ".img", ".zip", ".dat", ".xml", ".pal", ".sms", ".col", ".chr", ".fnt", ".ini"}:
                        src = Path(root) / f
                        dest = bios_staging / f
                        try:
                            if not dest.exists() or dest.stat().st_size != src.stat().st_size:
                                with open(src, "rb") as fin, open(dest, "wb") as fout:
                                    shutil.copyfileobj(fin, fout, length=1024 * 1024)
                                flatten_count += 1
                        except Exception as e:
                            print(f"Pular {f}: {e}")
    print(f"BIOS na raiz de staging/bios/: {flatten_count} atualizadas/copiadas.")

    # 2. neogeo.zip completo (1.95MB com 38 chips e Uni-BIOS 4.0)
    complete_neo = bios_src / "várias do honda" / "neogeo.zip"
    if complete_neo.is_file():
        shutil.copy2(complete_neo, bios_staging / "neogeo.zip")
        shutil.copy2(complete_neo, neogeo_staging / "neogeo.zip")
        print("neogeo.zip (1.95MB completo FBNeo) copiado para staging/bios/ e staging/neogeo/.")

    # 3. Extrair 7z mascarados como .zip no PSX (Tekken 3, Metal Gear Solid, Gran Turismo)
    seven_zip_candidates = [
        Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "7-Zip" / "7z.exe",
        Path("C:\\Program Files\\7-Zip\\7z.exe"),
        Path("C:\\Program Files (x86)\\7-Zip\\7z.exe"),
    ]
    seven_zip_exe = next((p for p in seven_zip_candidates if p.is_file()), None)

    target_magic = bytes([0x37, 0x7A, 0xBC, 0xAF, 0x27, 0x1C])
    for zip_file in psx_staging.glob("*.zip"):
        try:
            with open(zip_file, "rb") as fp:
                header = fp.read(6)
            if header.startswith(target_magic):
                print(f"Extraindo {zip_file.name} via 7-Zip...")
                if seven_zip_exe:
                    cmd = [str(seven_zip_exe), "e", str(zip_file), f"-o{str(psx_staging)}", "-y"]
                    res = subprocess.run(cmd, capture_output=True, text=True)
                    if res.returncode == 0:
                        zip_file.unlink()
                        print(f"  Extraido e removido: {zip_file.name}")
                    else:
                        print(f"  Erro ao extrair {zip_file.name}: {res.stderr}")
        except Exception as e:
            print(f"Aviso em {zip_file.name}: {e}")

    # 4. CUE para Crash Bandicoot.bin raw
    crash_bin = psx_staging / "Crash Bandicoot.bin"
    crash_cue = psx_staging / "Crash Bandicoot.cue"
    if crash_bin.is_file() and not crash_cue.is_file():
        cue_text = 'FILE "Crash Bandicoot.bin" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n'
        crash_cue.write_text(cue_text, encoding="utf-8")
        print("Criado: Crash Bandicoot.cue")

    # 5. Atualizar gamelist.xml do PSX para apontar para CUE / CHD descompactados
    update_psx_gamelist(psx_staging)

    print("\nStaging pronto para deploy no SD H:.")
    return 0


def update_psx_gamelist(psx_dir: Path) -> None:
    gamelist_path = psx_dir / "gamelist.xml"
    if not gamelist_path.is_file():
        return

    import xml.etree.ElementTree as ET
    try:
        tree = ET.parse(gamelist_path)
        root = tree.getroot()
        changed = False
        # Para cada jogo com .zip que agora virou .cue
        for game in root.findall("game"):
            path_node = game.find("path")
            if path_node is not None and path_node.text:
                p = path_node.text
                if p.endswith(".zip"):
                    stem = p[:-4]
                    cue_name = f"{stem}.cue"
                    if (psx_dir / cue_name.lstrip("./")).is_file():
                        path_node.text = cue_name
                        changed = True
                elif p.endswith("Crash Bandicoot.bin"):
                    path_node.text = "./Crash Bandicoot.cue"
                    changed = True
        if changed:
            tree.write(gamelist_path, encoding="utf-8", xml_declaration=True)
            print("Atualizado gamelist.xml de PSX com novas extensoes .cue.")
    except Exception as e:
        print(f"Aviso ao atualizar gamelist.xml de PSX: {e}")


if __name__ == "__main__":
    raise SystemExit(main())
