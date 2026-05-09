#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence
from pathlib import Path

IGNORED_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "site-packages",
}


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect shadow adaptix_contracts packages in a polyrepo workspace.")
    parser.add_argument(
        "--workspace-root",
        default=os.environ.get("ADAPTIX_CONTRACTS_WORKSPACE_ROOT"),
        help="Workspace root containing Adaptix repos. Defaults to ADAPTIX_CONTRACTS_WORKSPACE_ROOT or the current repo parent.",
    )
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit a machine-readable JSON report.")
    return parser.parse_args(argv)


def _discover_shadow_packages(workspace_root: Path, current_repo: Path) -> list[str]:
    shadows: list[str] = []
    for repo_dir in sorted(workspace_root.iterdir()):
        if not repo_dir.is_dir() or repo_dir.resolve() == current_repo:
            continue
        for root, dirs, _files in os.walk(repo_dir):
            dirs[:] = [directory for directory in dirs if directory not in IGNORED_DIR_NAMES]
            if "adaptix_contracts" in dirs:
                candidate = Path(root) / "adaptix_contracts"
                if candidate.resolve().is_dir():
                    shadows.append(str(candidate.resolve()))
    return shadows


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    current_repo = Path(__file__).resolve().parents[1]
    workspace_root = Path(args.workspace_root).resolve() if args.workspace_root else current_repo.parent

    shadows = _discover_shadow_packages(workspace_root=workspace_root, current_repo=current_repo)
    passed = not shadows
    report = {
        "workspace_root": str(workspace_root),
        "current_repo": str(current_repo),
        "shadow_package_count": len(shadows),
        "shadow_package_paths": shadows,
        "status": "PASS" if passed else "FAIL",
    }

    if args.json_output:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("ADAPTIX CONTRACT WORKSPACE AUDIT")
        print(f"Workspace root: {workspace_root}")
        print(f"Current repo: {current_repo}")
        if passed:
            print("PASS - No shadow adaptix_contracts packages detected.")
        else:
            print("FAIL - Shadow adaptix_contracts packages detected:")
            for path in shadows:
                print(f" - {path}")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())