# my_lua_template

Copier template for Lua projects. One template, three project types:

- `mise-backend`: mise backend plugins with `hooks/`, `metadata.lua`, and busted tests
- `nvim-config`: a Neovim configuration with `init.lua` and mini.test
- `nvim-plugin`: a Neovim plugin with `plugin/`, `lua/<plugin_slug>/`, and mini.test specs

Generated projects get stylua, selene, emmylua_check, hk git hooks, mise tasks (`ci`, `lint`, `typecheck`, `test`, `format`), an `AGENTS.md` with a `CLAUDE.md` pointer, and optionally commitizen plus GitHub Actions CI with auto tag and release.

## Usage

```sh
copier copy --trust gh:KyleKing/my_lua_template path/to/new/project
```

To update an existing project:

```sh
cd path/to/project
copier update --trust
```

`--trust` is required because post-generation tasks run `git init` and a cleanup script.

## Template development

- `lua_template/` is the rendered tree (`_subdirectory`); `copier.yml` holds the questions
- CI generates all three project types on every push and runs their gates
- `python3 scripts/canary.py` runs a real `copier update` plus `mise run ci` against downstream repos listed in `scripts/canary_repos.json` (`CANARY_SIBLINGS=1` targets local sibling checkouts)
- Releases are tagged by commitizen in the bump workflow on pushes to `main`

## License

MIT License - Copyright (c) 2026 Kyle King
