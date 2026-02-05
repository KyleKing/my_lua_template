#!/usr/bin/env python3
"""Post-generation tasks for lua_template."""

import shutil
from pathlib import Path


def cleanup_conditional_directories():
    """Remove directories that were conditionally excluded."""
    root = Path(__file__).parent

    # Read answers to determine project type
    answers_file = root / ".copier-answers.yml"
    project_type = None
    if answers_file.exists():
        import yaml

        with answers_file.open() as f:
            answers = yaml.safe_load(f)
            project_type = answers.get("project_type")

    # Remove mise-backend specific files for non-mise projects
    if project_type != "mise-backend":
        for path in ["hooks", "spec", "metadata.lua", "busted.yml"]:
            target = root / path
            if target.is_dir():
                shutil.rmtree(target)
                print(f"Removed {path}/ (not mise-backend)")
            elif target.is_file():
                target.unlink()
                print(f"Removed {path} (not mise-backend)")

    # Remove nvim-config specific files for non-nvim-config projects
    if project_type != "nvim-config":
        init_lua = root / "init.lua"
        if init_lua.exists():
            init_lua.unlink()
            print("Removed init.lua (not nvim-config)")

    # Remove nvim-plugin specific files for non-nvim-plugin projects
    if project_type != "nvim-plugin":
        for path in ["plugin", "test"]:
            target = root / path
            if target.is_dir() and not any(target.iterdir()):
                shutil.rmtree(target)
                print(f"Removed empty {path}/ (not nvim-plugin)")

    # Clean up vim.toml for mise-backend projects
    if project_type == "mise-backend":
        vim_toml = root / "vim.toml"
        if vim_toml.exists():
            vim_toml.unlink()
            print("Removed vim.toml (mise-backend)")


def cleanup_empty_workflows():
    """Remove empty or conditional workflow files."""
    root = Path(__file__).parent
    workflows_dir = root / ".github" / "workflows"

    if workflows_dir.exists():
        for workflow in workflows_dir.glob("*.yml"):
            content = workflow.read_text().strip()
            if not content or len(content) < 50:
                workflow.unlink()
                print(f"Removed empty workflow: {workflow.name}")

        # Remove .github if empty
        github_dir = root / ".github"
        if github_dir.exists() and not any(github_dir.rglob("*")):
            shutil.rmtree(github_dir)
            print("Removed empty .github/")


def create_missing_directories():
    """Create expected directories based on project type."""
    root = Path(__file__).parent

    # Read project type
    answers_file = root / ".copier-answers.yml"
    project_type = None
    if answers_file.exists():
        import yaml

        with answers_file.open() as f:
            answers = yaml.safe_load(f)
            project_type = answers.get("project_type")

    # Create directories based on project type
    if project_type == "mise-backend":
        (root / "hooks").mkdir(exist_ok=True)
        (root / "spec").mkdir(exist_ok=True)
    elif project_type == "nvim-config":
        (root / "lua").mkdir(exist_ok=True)
    elif project_type == "nvim-plugin":
        (root / "plugin").mkdir(exist_ok=True)
        (root / "lua").mkdir(exist_ok=True)
        (root / "test").mkdir(exist_ok=True)


def delete_myself():
    """Remove this script after execution."""
    Path(__file__).unlink()


def main():
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("Warning: pyyaml not installed, skipping project-type cleanup")
        print("Install with: pip install pyyaml")
        delete_myself()
        return

    cleanup_conditional_directories()
    cleanup_empty_workflows()
    create_missing_directories()
    delete_myself()


if __name__ == "__main__":
    main()
