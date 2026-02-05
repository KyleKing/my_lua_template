# Template Structure

This document describes the structure and files included in my_lua_template.

## Template Files (35 total)

### Core Template Configuration

- `copier.yml` - Main copier configuration with questions and settings
- `README.md` - Template documentation
- `LICENSE` - MIT license for the template itself
- `CHANGELOG.md` - Template version history
- `.gitignore` - Git ignore patterns for template repo
- `.editorconfig` - Editor configuration for template development
- `.cz.toml` - Commitizen configuration for template repo
- `ctt.toml` - CTT (Copier Template Tool) configuration

### Post-Generation Scripts

- `lua_template/_copier_post_generation.py` - Cleanup script that runs after project generation

### Shared Files (All Project Types)

These files are generated for all project types:

- `lua_template/.editorconfig` - Editor configuration
- `lua_template/stylua.toml` - Lua code formatter configuration
- `lua_template/vim.toml` - Selene vim standard definition
- `lua_template/LICENSE.jinja` - MIT license
- `lua_template/{{ _copier_conf.answers_file }}.jinja` - Copier answers file

### Conditional Files (Varies by Project Type)

- `lua_template/selene.toml.jinja` - Lua linter config (std varies)
- `lua_template/.luarc.json.jinja` - Lua LSP config (workspace varies)
- `lua_template/mise.toml.jinja` - Task runner config (tasks vary)
- `lua_template/.pre-commit-config.yaml.jinja` - Git hooks (hooks vary)
- `lua_template/.gitignore.jinja` - Git ignore patterns (patterns vary)
- `lua_template/.cz.toml.jinja` - Commitizen config (conditional on use_cz)
- `lua_template/README.md.jinja` - Project README (content varies)
- `lua_template/CONTRIBUTING.md.jinja` - Contribution guide (content varies)
- `lua_template/.github/workflows/ci.yml.jinja` - CI workflow (conditional on include_ci)

### mise-backend Specific Files

Only generated when `project_type == 'mise-backend'`:

- `lua_template/metadata.lua.jinja` - Plugin metadata
- `lua_template/busted.yml` - Busted testing configuration
- `lua_template/hooks/lib.lua.jinja` - Shared library functions
- `lua_template/spec/lib_spec.lua.jinja` - Example test spec

### nvim-config Specific Files

Only generated when `project_type == 'nvim-config'`:

- `lua_template/init.lua.jinja` - Neovim entry point

### nvim-plugin Specific Files

Only generated when `project_type == 'nvim-plugin'`:

- `lua_template/plugin/init.lua.jinja` - Plugin entry point
- `lua_template/lua/init.lua.jinja` - Plugin main module
- `lua_template/test/init_test.lua.jinja` - Example test
- `lua_template/scripts/minimal_init.lua.jinja` - Minimal neovim config for testing

## Directory Structure

```
my_lua_template/
├── copier.yml                          # Main template configuration
├── README.md                           # Template documentation
├── LICENSE                             # Template license
├── CHANGELOG.md                        # Template changelog
├── TEMPLATE_STRUCTURE.md              # This file
├── .gitignore                         # Template repo gitignore
├── .editorconfig                      # Template repo editorconfig
├── .cz.toml                          # Template repo commitizen
├── ctt.toml                          # CTT configuration
└── lua_template/                      # Template subdirectory
    ├── _copier_post_generation.py     # Post-generation cleanup
    ├── {{ _copier_conf.answers_file }}.jinja
    ├── .editorconfig                  # Shared
    ├── .gitignore.jinja              # Conditional
    ├── .luarc.json.jinja             # Conditional
    ├── .pre-commit-config.yaml.jinja # Conditional
    ├── .cz.toml.jinja                # Conditional
    ├── stylua.toml                    # Shared
    ├── selene.toml.jinja             # Conditional
    ├── vim.toml                       # Shared (nvim projects)
    ├── mise.toml.jinja               # Conditional
    ├── LICENSE.jinja                  # Shared
    ├── README.md.jinja               # Conditional
    ├── CONTRIBUTING.md.jinja         # Conditional
    ├── .github/
    │   └── workflows/
    │       └── ci.yml.jinja          # Conditional
    ├── busted.yml                     # mise-backend only
    ├── metadata.lua.jinja            # mise-backend only
    ├── init.lua.jinja                # nvim-config only
    ├── hooks/
    │   ├── .gitkeep
    │   └── lib.lua.jinja             # mise-backend only
    ├── spec/
    │   ├── .gitkeep
    │   └── lib_spec.lua.jinja        # mise-backend only
    ├── lua/
    │   ├── .gitkeep
    │   └── init.lua.jinja            # nvim-plugin/config
    ├── plugin/
    │   ├── .gitkeep
    │   └── init.lua.jinja            # nvim-plugin only
    ├── test/
    │   ├── .gitkeep
    │   └── init_test.lua.jinja       # nvim-plugin only
    └── scripts/
        ├── .gitkeep
        └── minimal_init.lua.jinja    # nvim-plugin only
```

## Project Types

### mise-backend

For creating mise backend plugins:

**Generated files:**
- metadata.lua, busted.yml
- hooks/lib.lua, spec/lib_spec.lua
- mise.toml with busted tasks
- selene.toml with busted std

**Directory structure:**
```
project-name/
├── hooks/
│   └── lib.lua
├── spec/
│   └── lib_spec.lua
├── metadata.lua
└── busted.yml
```

### nvim-config

For Neovim configurations:

**Generated files:**
- init.lua entry point
- mise.toml with nvim testing tasks
- selene.toml with vim std
- vim.toml for selene

**Directory structure:**
```
project-name/
├── init.lua
├── lua/
└── vim.toml
```

### nvim-plugin

For Neovim plugins:

**Generated files:**
- plugin/init.lua entry point
- lua/init.lua main module
- test/init_test.lua example test
- scripts/minimal_init.lua for testing
- mise.toml with mini.test tasks
- selene.toml with vim std
- vim.toml for selene

**Directory structure:**
```
project-name/
├── plugin/
│   └── init.lua
├── lua/
│   └── init.lua
├── test/
│   └── init_test.lua
├── scripts/
│   └── minimal_init.lua
└── vim.toml
```

## Tooling Configuration

### Lua Formatting (stylua)

- 4 space indentation
- Unix line endings
- 120 character line width
- Auto prefer double quotes
- Always use call parentheses
- Collapse simple statements

### Lua Linting (selene)

**mise-backend:**
- std: lua51/lua54 + project-name + busted
- Allow incorrect_standard_library_use
- Allow unused_variable

**nvim projects:**
- std: vim (defined in vim.toml)
- Allow mixed_table
- Allow multiple_statements
- Allow undefined_variable

### Lua LSP (.luarc.json)

**mise-backend:**
- Lua 5.1 or 5.4 runtime
- Workspace library: hooks/, metadata.lua
- Globals: PLUGIN, RUNTIME
- Ignore: .luarocks, .git

**nvim-config:**
- Lua 5.1 runtime
- Workspace library: lua/
- Globals: vim
- Ignore: .git

**nvim-plugin:**
- Lua 5.1 runtime
- Workspace library: plugin/, lua/
- Globals: vim
- Ignore: .git

### Pre-commit Hooks

All projects include:
- check-added-large-files, check-json, check-toml, check-yaml
- end-of-file-fixer, trailing-whitespace, mixed-line-ending
- stylua-system (Lua formatting)
- prettier (JSON, YAML, Shell)
- mdformat (Markdown)
- toml-sort (TOML files)
- selene (Lua linting)
- commitizen (if use_cz=true)

### mise Tasks

**All projects:**
- `mise run lint` - Check code formatting
- `mise run format` - Fix code formatting
- `mise run typecheck` - Run selene linter
- `mise run ci` - Run all checks

**mise-backend:**
- `mise run install` - Install luarocks dependencies
- `mise run test` - Run busted tests
- `mise run test-file` - Run specific test file

**nvim projects:**
- `mise run deps-mini-nvim` - Download mini.nvim for testing
- `mise run test` - Run mini.test tests
- `mise run test-file` - Run specific test file

### GitHub Actions CI

**All projects (if include_ci=true):**
- Lint job: Run formatting, type checking, and tests
- Runs on ubuntu-latest
- Uses mise-action for tool installation

**nvim projects:**
- Additional test-nvim job
- Matrix testing: stable and nightly Neovim
- Uses rhysd/action-setup-vim for Neovim installation

**mise-backend:**
- Focused on plugin testing with LuaRocks

## Usage Examples

### Create a new mise backend plugin

```bash
copier copy path/to/my_lua_template new-plugin
# Select: project_type = mise-backend
# Select: lua_version = 5.4
```

### Create a new Neovim plugin

```bash
copier copy path/to/my_lua_template awesome.nvim
# Select: project_type = nvim-plugin
# Select: lua_version = 5.1
```

### Create a new Neovim config

```bash
copier copy path/to/my_lua_template nvim-config
# Select: project_type = nvim-config
# Select: lua_version = 5.1
```

### Update existing project

```bash
cd existing-project
copier update
```

## Post-Generation Cleanup

The `_copier_post_generation.py` script:

1. Reads `.copier-answers.yml` to determine project_type
2. Removes files/directories not applicable to the project type:
   - mise-backend: Removes nvim-specific files (init.lua, plugin/, test/, vim.toml)
   - nvim-config: Removes mise-backend files (hooks/, spec/, metadata.lua, busted.yml) and plugin/
   - nvim-plugin: Removes mise-backend files and init.lua
3. Removes empty workflow files
4. Creates expected directories based on project type
5. Deletes itself after completion

## Requirements

- copier >= 9.0.0
- Python 3.9+ with pyyaml
- mise (recommended)
- pre-commit
- Lua tooling: stylua, selene, lua-language-server

## Best Practices Alignment

This template incorporates best practices from:

- **mise-postgres-binary**: Robust mise backend plugin structure, comprehensive testing
- **spaghetti-comb.nvim**: Full Lua tooling setup, pre-commit hooks, mise tasks
- **~/.config/nvim**: Minimal nvim configuration patterns
- **calcipy_template**: Python template structure, post-generation cleanup
- **my_go_template**: Multi-project-type support, conditional file generation

## License

MIT License - Copyright (c) 2026 Kyle King
