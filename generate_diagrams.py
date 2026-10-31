"""Render every diagrams-as-code script in diagrams/ to docs/assets/.

Run from the repo root: python generate_diagrams.py
"""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
os.makedirs("docs/assets", exist_ok=True)

scripts = sorted(Path("diagrams").glob("*.py"))
if not scripts:
    sys.exit("No diagram scripts found in diagrams/")

for script in scripts:
    print(f"Rendering {script}")
    runpy.run_path(str(script), run_name="__main__")

print(f"Rendered {len(scripts)} diagram(s) to docs/assets/")
