# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.4.1 (2026-09-01)

### Fix

- guard the PR step on a string so an empty output cannot throw

## v0.4.0 (2026-09-01)

### Feat

- **doneram**: install the pinned release instead of building from source

### Fix

- **doneram**: install pkl so the freshness job can read the config

## v0.3.1 (2026-08-31)

### Fix

- render the config modules init.lua has always required

## v0.3.0 (2026-08-31)

### Feat

- **ci**: track tool and action pins with doneram
- **ci**: serialize Bump Version and guard the no-release case
- template-owned AGENTS.md with AGENTS.local.md for project guidance
- ship AGENTS.md with CLAUDE.md pointer, preserve per-directory AGENTS.md
- canary harness runs copier update and ci against downstream repos
- type check with emmylua_check, fold selene into lint

## v0.2.0 (2026-08-01)

### Feat

- make plugin_slug an answerable question stripping .nvim
- initialize lua template

### Fix

- json-quote project_description in the answers file
- derive plugin identifiers and requires from plugin_slug
- do not pre-create deps dir so a failed mini.nvim clone retries
- sweep empty minimal_init render for non-plugin projects
- lint scripts/ and collapse minimal_init simple statement
- correct jinja whitespace control for copier's untrimmed env
- repair luarc and selene whitespace under copier's jinja trimming
- use a real mini.test expectation in the sample spec
- only install standalone lua for mise-backend projects
- repair ci.yml whitespace mangling from jinja trim markers
- repair nvim-plugin generation, port hooks to hk, pin tools
