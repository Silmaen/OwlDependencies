---
globs: CI/*.py,check_updates.py
---

# CI and Utility Scripts

## CI/Build.py

Main build orchestrator. Pipeline: discover recipes -> resolve dependency order -> pull from remote -> build missing ->
push results. Uses `depmanager` API directly (not CLI).

Key classes/functions:

- `Parameters` - global build config (verbosity, pull/push/build flags, filter, machine/toolset)
- `reorder_recipes()` - topological sort of recipes by dependency graph
- `query_from_recipe()` - builds a package query dict from a recipe instance

## CI/check_ext_deps.py

Validates that built shared libraries don't link against unexpected system libraries. Uses `ldd` on Linux and
`objdump -p` on Windows. The ignore lists (`ignore_list_lin`, `ignore_list_win`) define allowed system dependencies.

Uses `dmgr info basedir` (depmanager CLI) to find the package data directory.

## check_updates.py

Iterates all git submodules, fetches remote tags, and compares current tag with latest. Filters out pre-release tags (
rc, beta, preview, etc.) via `is_valid_tag()`.
