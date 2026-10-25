#!/usr/bin/env python3
"""Regenerate the pack's generated content and refresh packwiz hashes.

  python3 tools/build_pack.py            # regenerate kubejs/ + quests into pack/, refresh index
  python3 tools/build_pack.py --index    # only refresh index.toml / pack.toml hashes

Generated (do not hand-edit, edit tools/ instead): pack/kubejs/**, pack/config/ftbquests/**.
Hand-maintained: pack/mods/*.pw.toml, pack/config/** (other mods' configs), pack/pack.toml metadata.
"""
import hashlib, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, "pack")
SRC = os.path.join(ROOT, ".cache", "src")
PACK_VERSION = "0.4.0"
MC, NEOFORGE = "1.21.1", "21.1.264"

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def regenerate():
    subprocess.run([os.path.join(ROOT, "tools", "fetch_sources.sh"), SRC], check=True)
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "instance")
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build2.py"), out, SRC], check=True)
        for sub in ("kubejs", os.path.join("config", "ftbquests")):
            dst = os.path.join(PACK, sub)
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(os.path.join(out, "minecraft", sub), dst)

def write_index():
    files = []
    for dirpath, dirnames, filenames in os.walk(PACK):
        dirnames.sort()
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, PACK).replace(os.sep, "/")
            if rel in ("pack.toml", "index.toml") or fn.startswith("."):
                continue
            files.append((rel, sha256(full), rel.startswith("mods/") and fn.endswith(".pw.toml")))
    lines = ['hash-format = "sha256"', ""]
    for rel, h, meta in files:
        lines += ["[[files]]", f'file = "{rel}"', f'hash = "{h}"']
        if meta:
            lines.append("metafile = true")
        lines.append("")
    with open(os.path.join(PACK, "index.toml"), "w", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(PACK, "pack.toml"), "w", newline="\n") as f:
        f.write("\n".join([
            'name = "Stellar Foundry"', 'author = "Peter"', f'version = "{PACK_VERSION}"',
            'pack-format = "packwiz:1.1.0"', "", "[index]", 'file = "index.toml"',
            'hash-format = "sha256"', f'hash = "{sha256(os.path.join(PACK, "index.toml"))}"', "",
            "[versions]", f'minecraft = "{MC}"', f'neoforge = "{NEOFORGE}"', ""]))
    print(f"index: {len(files)} files")

if __name__ == "__main__":
    if "--index" not in sys.argv:
        regenerate()
    write_index()
