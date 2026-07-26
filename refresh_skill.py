#!/usr/bin/env python3
"""Refresh generated MCP files in the bundled Inf2 skill."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / ".claude" / "skills" / "inf2-management"


def main() -> int:
    for name in ("server.py", "project-setup.sh", "requirements.txt"):
        source = ROOT / name
        destination = SKILL / "mcp" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        print(f"copied {name} -> {destination.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
