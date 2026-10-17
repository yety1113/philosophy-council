#!/usr/bin/env python3
"""Register an isolated personal marketplace, then install through Codex."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--destination',type=Path,default=Path.home()/'.codex/plugins/philosophy-council-source')
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
dest=a.destination.expanduser().resolve()
if dest == root or dest in root.parents or root in dest.parents:
    raise SystemExit('安装目标必须与源目录分离')
if dest.exists():
    raise SystemExit('目标已存在；为保护本地改动，请先检查或选择其他 --destination')
shutil.copytree(root,dest,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
# Dedicated catalog; no edits to existing Personal catalog.
subprocess.run(['codex','plugin','marketplace','add',str(dest)],check=True)
subprocess.run(['codex','plugin','add','philosophy-council@philosophy-council','--json'],check=True)
print('Installed via Codex. Start a new chat to load the new skill and tools.')
