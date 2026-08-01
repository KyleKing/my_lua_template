#!/usr/bin/env python3
"""Post-generation tasks for lua_template."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).parent


def read_project_type() -> str | None:
    answers_file = ROOT / ".copier-answers.yml"
    if not answers_file.exists():
        return None
    import yaml

    with answers_file.open() as f:
        return yaml.safe_load(f).get("project_type")


def cleanup_conditional_directories(project_type: str | None) -> None:
    if project_type != "mise-backend":
        for path in ["hooks", "spec", "metadata.lua", "busted.yml"]:
            target = ROOT / path
            if target.is_dir():
                shutil.rmtree(target)
                print(f"Removed {path}/ (not mise-backend)")
            elif target.is_file():
                target.unlink()
                print(f"Removed {path} (not mise-backend)")

    if project_type == "mise-backend":
        vim_toml = ROOT / "vim.toml"
        if vim_toml.exists():
            vim_toml.unlink()
            print("Removed vim.toml (mise-backend)")


def cleanup_empty_renders() -> None:
    """Remove files whose conditional content rendered to nothing."""
    for pattern in ["init.lua", "lua/init.lua", "plugin/init.lua", ".github/workflows/*.yml"]:
        for target in ROOT.glob(pattern):
            if target.is_file() and not target.read_text().strip():
                target.unlink()
                print(f"Removed empty render: {target.relative_to(ROOT)}")

    for directory in ["plugin", "scripts", "lua", ".github/workflows", ".github"]:
        target = ROOT / directory
        if target.is_dir():
            gitkeep = target / ".gitkeep"
            others = [p for p in target.rglob("*") if p != gitkeep]
            if not others:
                shutil.rmtree(target)
                print(f"Removed empty directory: {directory}/")


def create_missing_directories(project_type: str | None) -> None:
    if project_type == "mise-backend":
        (ROOT / "hooks").mkdir(exist_ok=True)
        (ROOT / "spec").mkdir(exist_ok=True)
    elif project_type in {"nvim-config", "nvim-plugin"}:
        (ROOT / "lua").mkdir(exist_ok=True)


def delete_myself() -> None:
    Path(__file__).unlink()


def main() -> None:
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("Warning: pyyaml not installed, skipping project-type cleanup")
        print("Install with: pip install pyyaml")
        delete_myself()
        return

    project_type = read_project_type()
    cleanup_conditional_directories(project_type)
    cleanup_empty_renders()
    create_missing_directories(project_type)
    delete_myself()


if __name__ == "__main__":
    main()
