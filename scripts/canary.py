"""Run a real `copier update` against downstream repos and their CI gates (canary testing).

Repos to check are configured in 'scripts/canary_repos.json'. For each repo this
clones (or reuses a cached clone of) the child project, points its
'.copier-answers.yml' at this template repo, runs 'copier update' against template
HEAD, and then runs the child's own 'mise run ci'. This proves the template's
current state still applies cleanly to real downstream projects and that the
result still passes their gates, before the template is tagged for release.

Set CANARY_SIBLINGS=1 to source each repo from a local sibling checkout
('../<name>' relative to this template repo) instead of cloning from 'url', to
test local unpushed child state.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

_TEMPLATE_ROOT = Path(__file__).parent.parent
_CANARY_DIR = _TEMPLATE_ROOT / ".canary-cache"
_REPOS_PATH = Path(__file__).parent / "canary_repos.json"

_GIT_IDENTITY = ["-c", "user.name=canary", "-c", "user.email=canary@localhost"]

_TAIL_LINES = 40


@dataclass(frozen=True)
class Repo:
    """A downstream repository to canary test against template HEAD."""

    name: str
    url: str

    @property
    def display(self) -> str:
        """Derive 'org/repo' from URL for display."""
        return "/".join(self.url.rstrip("/").split("/")[-2:])

    def source(self) -> str:
        """Resolve the clone source, honoring CANARY_SIBLINGS."""
        if os.environ.get("CANARY_SIBLINGS") == "1":
            sibling = _TEMPLATE_ROOT.parent / self.name
            if sibling.is_dir():
                return str(sibling)
        return self.url


@dataclass(frozen=True)
class CheckResult:
    """Outcome of canary testing a single repo."""

    repo: Repo
    passed: bool
    detail: str = ""


def _load_repos(path: Path) -> list[Repo]:
    """Parse 'canary_repos.json', ignoring fields this version doesn't know."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Repo(name=entry["name"], url=entry["url"]) for entry in data.get("repos", [])]


def _resolve_repos(argv: list[str], all_repos: list[Repo]) -> list[Repo]:
    if not argv:
        return list(all_repos)
    valid = {r.name for r in all_repos}
    unknown = [name for name in argv if name not in valid]
    if unknown:
        print(f"Unknown repo(s): {', '.join(unknown)}. Valid: {', '.join(sorted(valid))}")
        sys.exit(1)
    return [r for r in all_repos if r.name in argv]


def _clone_or_pull(repo: Repo, target_dir: Path) -> None:
    source = repo.source()
    if not target_dir.exists():
        subprocess.run(
            ["git", "clone", "--depth", "1", source, str(target_dir)],
            check=True,
        )
    else:
        subprocess.run(
            ["git", "fetch", "--depth", "1", "origin"],
            cwd=target_dir,
            check=True,
        )
        subprocess.run(
            ["git", "reset", "--hard", "FETCH_HEAD"],
            cwd=target_dir,
            check=True,
        )


def _rewrite_src_path(answers_path: Path) -> None:
    lines = answers_path.read_text(encoding="utf-8").splitlines(keepends=True)
    rewritten = [
        f"_src_path: {_TEMPLATE_ROOT}\n" if line.startswith("_src_path:") else line
        for line in lines
    ]
    answers_path.write_text("".join(rewritten), encoding="utf-8")


def _commit_answers_edit(target_dir: Path) -> None:
    subprocess.run(
        ["git", *_GIT_IDENTITY, "commit", "-am", "canary"],
        cwd=target_dir,
        check=True,
    )


def _tail(text: str, n: int = _TAIL_LINES) -> str:
    return "\n".join(text.splitlines()[-n:])


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def _copier_update(target_dir: Path) -> str | None:
    result = _run(
        ["uvx", "copier", "update", "--trust", "--defaults", "--conflict=rej", "--vcs-ref=HEAD"],
        target_dir,
    )
    if result.returncode != 0:
        return f"copier update failed:\n{_tail(result.stdout + result.stderr)}"

    rej_files = sorted(str(p.relative_to(target_dir)) for p in target_dir.rglob("*.rej"))
    if rej_files:
        return "template diff left .rej file(s):\n" + "\n".join(rej_files)

    return None


def _run_mise_gates(target_dir: Path) -> str | None:
    subprocess.run(["mise", "trust"], cwd=target_dir)

    install = _run(["mise", "install"], target_dir)
    if install.returncode != 0:
        return f"mise install failed:\n{_tail(install.stdout + install.stderr)}"

    ci = _run(["mise", "run", "ci"], target_dir)
    if ci.returncode != 0:
        return f"mise run ci failed:\n{_tail(ci.stdout + ci.stderr)}"

    return None


def _check_repo(repo: Repo) -> CheckResult:
    target_dir = _CANARY_DIR / repo.name
    try:
        _clone_or_pull(repo, target_dir)
    except subprocess.CalledProcessError as err:
        return CheckResult(repo=repo, passed=False, detail=f"clone/fetch failed: {err}")

    answers_path = target_dir / ".copier-answers.yml"
    if not answers_path.is_file():
        return CheckResult(
            repo=repo, passed=False, detail=f"missing {answers_path.name}; not a copier project"
        )

    _rewrite_src_path(answers_path)
    _commit_answers_edit(target_dir)

    update_failure = _copier_update(target_dir)
    if update_failure:
        return CheckResult(repo=repo, passed=False, detail=update_failure)

    gate_failure = _run_mise_gates(target_dir)
    if gate_failure:
        return CheckResult(repo=repo, passed=False, detail=gate_failure)

    return CheckResult(repo=repo, passed=True)


def _print_results(results: list[CheckResult]) -> None:
    print("--- Canary Results ---")
    for result in results:
        label = "PASS" if result.passed else "FAIL"
        print(f"{label}  {result.repo.display}")
        if not result.passed:
            for line in result.detail.splitlines():
                print(f"      {line}")


def main(argv: list[str]) -> None:
    """Run canary checks against all or a named subset of repos."""
    all_repos = _load_repos(_REPOS_PATH)

    if not all_repos:
        print("No canary repos configured in scripts/canary_repos.json.")
        return

    repos = _resolve_repos(argv, all_repos)

    _CANARY_DIR.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=len(repos)) as pool:
        results = list(pool.map(_check_repo, repos))

    _print_results(results)

    failures = [r for r in results if not r.passed]
    count = len(failures)
    if count:
        noun = "failure" if count == 1 else "failures"
        names = "  ".join(r.repo.name for r in failures)
        print(f"\n{count} {noun}. Run: python3 scripts/canary.py {names}  to isolate.")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
