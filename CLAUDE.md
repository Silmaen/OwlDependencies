# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OwlDependencies manages all third-party C/C++ library dependencies for the [Owl Engine](https://github.com/Silmaen/Owl). It uses [DepManager](https://github.com/Silmaen/DepManager), a custom Python-based dependency manager, to build, package, and distribute pre-built libraries across platforms (Windows x86_64, Linux x86_64, Linux aarch64).

## Key Commands

### Setup
```bash
git submodule update --init --recursive   # fetch all library source code
poetry install --with build               # install Python deps (depmanager, etc.)
```

### Building
```bash
# Build all libraries (pulls from remote first, builds what's missing, pushes results)
python CI/Build.py

# Build with verbosity
python CI/Build.py -v        # show what's happening
python CI/Build.py -vvv      # maximum verbosity (dependency resolution details)

# Build specific libraries only (regex filter on recipe name)
python CI/Build.py --filter "fmt"

# Build without pushing to remote
python CI/Build.py --no-push

# Dry run (no pull, build, or push - just show what would happen)
python CI/Build.py --dry-run

# Cross-compile with custom toolset
python CI/Build.py --toolset "<name>:<compiler_path>:<abi>"
```

### Single library build via depmanager
```bash
depmanager build Libs/<library_name>
```

### Check for submodule updates
```bash
python check_updates.py       # check all submodules for newer tags
python check_updates.py -v    # verbose output with current/latest tags
```

### Validate built library dependencies
```bash
python CI/check_ext_deps.py   # ensure no unintended external linkage
```

## Architecture

### How Libraries Are Organized

Each library lives in `Libs/<name>/` with three components:
- **`<name>.py`** - DepManager recipe defining how to build the library
- **`<name>/` or `sources/`** - Git submodule containing the actual source code
- **`CMakeLists.txt`** - Thin wrapper that invokes `depmanager build` and declares dependencies

### Recipe System

Recipes are Python classes inheriting from `depmanager.api.recipe.Recipe`. Key class attributes:

- `name`, `version`, `description` - package identity
- `source_dir` - subdirectory containing the source (submodule name)
- `kind` - one of `"header"`, `"shared"`, or `"static"`
- `dependencies` - list of dicts like `[{"name": "zlib", "kind": "shared"}]`
- `config` - build configurations (defaults to both Release and Debug; some like vulkan_sdk restrict to `["Release"]`)

Most libraries define a `Shared` class and a `Static` class inheriting from it:

```python
class FmtShared(Recipe):
    name = "fmt"
    version = "12.1.0"
    source_dir = "fmt"
    kind = "shared"
    def configure(self):       # set CMake cache variables via self.cache_variables
class FmtStatic(FmtShared):
    kind = "static"
```

Not all libraries follow this pattern: header-only libs define only one class with `kind = "header"`, and some (like vulkan_sdk, slang) only have a shared variant.

### Source Patching Pattern

Several libraries (vulkan_sdk, FreeType, slang) need to patch upstream CMake files before building. They use a `corrections` list of `[original_bytes, replacement_bytes, file_filter]` tuples applied in `source()`, then reverted in `clean()`:

```python
file_modif = ["CMakeLists.txt"]
corrections = [
    [b"find_package(PNG", b"find_package(PNG CONFIG", None],  # None = apply to all files
]
```

The `source()` method applies all corrections before the build; `clean()` reverses them so submodule sources stay unmodified. When adding corrections, use `bytes` literals (`b"..."`) and respect the `[original, replacement, file_or_None]` tuple structure.

### Build Order and Dependency Chain

The root `CMakeLists.txt` and `CI/Build.py` both enforce dependency ordering. Libraries are grouped:

1. **Header-only** (debugbreak, entt, magic_enum, stb, zeus) - no compilation
2. **No dependencies** (box2d, brotli, curl, fmt, glad, glfw, glm, googletest, harfbuzz, jsoncpp, libsndfile, nanosvg, nfd, openal, spdlog, tinygltf, tinyobjloader, tinyply, tinyxml2, ufbx, vulkan_sdk, yaml-cpp, zlib, zstd)
3. **With dependencies** - built after their prerequisites:
   - zlib -> libpng -> FreeType -> msdfgen -> msdf-atlas-gen
   - brotli, harfbuzz -> FreeType
   - zstd -> libdwarf -> cpptrace
   - tinyxml2, jsoncpp -> mavsdk
   - glfw, vulkan_sdk -> imgui -> imguizmo

Each library's `CMakeLists.txt` uses `add_dependencies()` to declare which other library targets must build first.

### Special Cases

- **vulkan_sdk** - A composite library with ~10 Khronos submodules (Vulkan-Headers, Vulkan-Loader, SPIRV-Tools, glslang, shaderc, etc.) all built as a single package. Heavily patched via `source()`/`clean()`.
- **glad, imgui, imguizmo, debugbreak** - Have custom CMake (`sources/CMakeLists.txt`) since upstream doesn't provide one.
- **stb** - Header-only with vendored source (not a submodule), lives at `stb_image/stb_image-2.28/`.
- **spdlog** - Depends on fmt at the recipe level (`dependencies`) but not via CMake `add_dependencies` since it uses fmt headers at compile time.

### Adding a New Library

1. Add git submodule: `git submodule add <url> Libs/<name>/<name>`
2. Create `Libs/<name>/<name>.py` with recipe classes inheriting from `Recipe`
3. Create `Libs/<name>/CMakeLists.txt` invoking `depmanager build`
4. Add `add_subdirectory(Libs/<name>)` to the root `CMakeLists.txt` in the correct dependency group
5. If it has dependencies, add `add_dependencies()` calls in both the library's CMakeLists.txt and set `dependencies` in the recipe
6. If upstream CMake needs patching, use the `file_modif`/`corrections`/`source()`/`clean()` pattern

## Requirements

- CMake 3.24+
- Python 3.12+
- DepManager (`depmanager` must be on PATH, installed via `poetry install --with build`)
- Poetry (for Python dependency management)
