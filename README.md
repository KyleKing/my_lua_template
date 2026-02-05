# my_lua_template

Copier template for Lua projects supporting three project types:

- **mise-backend**: mise backend plugins with hooks/, metadata.lua, busted testing
- **nvim-config**: Neovim configurations with init.lua, vim.toml
- **nvim-plugin**: Neovim plugins with plugin/, lua/, testing setup

## Features

- Robust Lua tooling: stylua, selene, lua-language-server
- Pre-commit hooks with comprehensive checks
- GitHub Actions CI workflows
- mise task runner configuration
- Conditional file generation based on project type
- Commitizen support for conventional commits

## Usage

### Create New Project

```sh
copier copy gh:kyleking/my_lua_template path/to/new/project
```

### Update Existing Project

```sh
cd path/to/project
copier update
```

## Requirements

- copier >= 9.0.0
- mise (recommended)
- pre-commit
- Python 3.9+

## Template Structure

```
lua_template/
├── .editorconfig                    # Shared: Editor config
├── stylua.toml                      # Shared: Lua formatting
├── selene.toml.jinja               # Conditional: Lua linting
├── .luarc.json.jinja               # Conditional: LSP config
├── mise.toml.jinja                 # Conditional: Task runner
├── .pre-commit-config.yaml.jinja   # Conditional: Git hooks
└── .github/
    └── workflows/
        └── ci.yml.jinja            # Conditional: CI pipeline
```

## Post-Generation

The template automatically:

1. Initializes git repository
2. Cleans up conditional files based on project type
3. Creates project-specific directory structure
4. Removes post-generation script

## Configuration Files

### Shared Across All Types

- `.editorconfig` - Consistent editor behavior
- `stylua.toml` - Lua code formatting
- `.gitignore` - Git ignore patterns
- `LICENSE` - MIT license

### Project-Type Specific

**mise-backend:**
- `hooks/` - mise backend hook scripts
- `metadata.lua` - Plugin metadata
- `busted.yml` - Testing configuration
- `spec/` - Test files

**nvim-config:**
- `init.lua` - Neovim entry point
- `lua/` - Configuration modules
- `vim.toml` - Selene vim standard

**nvim-plugin:**
- `plugin/` - Plugin entry points
- `lua/` - Plugin implementation
- `test/` - Test files
- `vim.toml` - Selene vim standard

## License

MIT License - Copyright (c) 2026 Kyle King
