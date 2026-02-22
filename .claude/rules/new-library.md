---
globs: Libs/**/*
---

# Adding a New Library

Follow these steps exactly:

1. **Add git submodule**: `git submodule add <url> Libs/<name>/<name>`
   - Source goes in a subdirectory matching the lib name, or `sources/` for libs needing custom CMake
2. **Create recipe**: `Libs/<name>/<name>.py` with Shared and Static classes
3. **Create CMakeLists.txt**: `Libs/<name>/CMakeLists.txt` using the standard pattern
4. **Register in root CMakeLists.txt**: `add_subdirectory(Libs/<name>)` in the correct dependency group
5. **Declare dependencies in both places**: `add_dependencies()` in CMake AND `dependencies` list in the recipe

## Directory naming

- Library directory: `Libs/<name>/` (lowercase)
- Submodule usually at `Libs/<name>/<name>/`
- Exception: some use `sources/` when a custom `sources/CMakeLists.txt` is needed (imgui, imguizmo, glad, debugbreak, glm, zstd, mavsdk)
- Exception: vulkan_sdk uses `source/` with multiple submodules inside

## Version convention

The `version` field in the recipe must match the git tag of the submodule (without `v` prefix). When updating a library, update both the submodule commit and the version in the recipe.
