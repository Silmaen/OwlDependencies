---
globs: "*"
---

# General Project Rules

## Language

This project is maintained by a French-speaking developer. Comments in CI scripts may be in French. Respond in the language the user writes in.

## Python

- Python 3.12+ required
- Dependencies managed via Poetry (`pyproject.toml`)
- The only Python runtime dependency is `depmanager` (and its transitive deps)
- No linter/formatter configured for the recipe files

## Git submodules

- All library sources are git submodules (except stb which is vendored)
- Never modify files inside submodule directories directly; use the `source()`/`clean()` patching pattern in recipes instead
- Submodule paths are registered in `.gitmodules`

## Platform support

Target platforms: Windows x86_64, Linux x86_64, Linux aarch64. Some recipes check `self.settings["os"]` to apply platform-specific configuration.
