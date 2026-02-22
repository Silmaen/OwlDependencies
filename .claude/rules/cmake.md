---
globs: Libs/*/CMakeLists.txt,CMakeLists.txt
---

# CMakeLists.txt Conventions

## Library-level CMakeLists.txt (Libs/<name>/CMakeLists.txt)

Every library CMakeLists.txt follows this exact pattern:

```cmake
get_filename_component(ProjectId ${CMAKE_CURRENT_SOURCE_DIR} NAME)
add_custom_target(${ProjectId} ALL
        COMMAND ${EDEPMANAGER} build ${CMAKE_CURRENT_SOURCE_DIR})
```

If the library has dependencies, append `add_dependencies()`:

```cmake
add_dependencies(${ProjectId} dep1 dep2)
```

The target name is always the directory name (e.g., `imgui`, `fmt`).

## Root CMakeLists.txt

Libraries are added via `add_subdirectory()` in three ordered groups:
1. Header-only (no compilation needed)
2. Compiled without dependencies
3. Compiled with dependencies (ordered so prerequisites come first)

When adding a new library, place it in the correct group with a comment if it has dependencies.
