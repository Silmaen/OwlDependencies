---
globs: Libs/**/*.py
---

# DepManager Recipe Conventions

Recipe files define how a library is built via `depmanager.api.recipe.Recipe`.

## Class structure

- Always define a `Shared` class first, then a `Static` class inheriting from it with only `kind = "static"` overridden (and `dependencies` if the kind changes per-dependency).
- Header-only libraries define a single class with `kind = "header"`.
- Some libraries (vulkan_sdk, slang) only have a shared variant.

## Required attributes

- `name` - package name (lowercase, matches directory name)
- `version` - must match the git tag/version of the submodule
- `source_dir` - subdirectory containing the submodule source
- `kind` - `"header"`, `"shared"`, or `"static"`
- `description` - short one-line description of the library

## Methods

- `configure()` - set CMake cache variables via `self.cache_variables["KEY"] = "VALUE"`. Always disable tests and docs when available.
- `source()` - pre-build source modifications (patching upstream CMake). Must be reversible by `clean()`.
- `clean()` - reverse all changes made by `source()` so submodule stays unmodified.

## Source patching pattern

When upstream CMake needs modification, use module-level `file_modif` and `corrections` lists:

```python
file_modif = ["CMakeLists.txt"]
corrections = [
    [b"original bytes", b"replacement bytes", None],  # None = apply to all files in file_modif
    [b"original", b"replacement", "specific/file.txt"],  # only apply to this file
]
```

The `source()` applies `correction[0] -> correction[1]`, and `clean()` reverses `correction[1] -> correction[0]`. Always use `bytes` literals (`b"..."`).

## Dependencies

Declare via `dependencies = [{"name": "libname", "kind": "shared"}]`. The `kind` key can be omitted if the dependency is the same kind as the recipe, but it's clearer to be explicit. Static variants often need to override `dependencies` to change kinds.
