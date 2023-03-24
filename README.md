# Owl Dependencies

This project only aims to gather all dependencies for the Owl Engine

## Rebuild Package

Regenerate all the dependencies by running python script:

```bash
python3 PyUtils/regenerate.py
```

A cmake target `regenerate` will do the same or with the `all` target.

Alternatively to build only one of the lib, use:

```bash
python3 PyUtils/regenerate.py -l <lib name>
```

## lib summary

|       | name          | submodule? | version/tag      | dependency           | link                                                        |
|-------|---------------|------------|------------------|----------------------|-------------------------------------------------------------|
| `X`   | debugbreak    |            | 1.0              |                      | [github](https://github.com/scottt/debugbreak)              |
| `X`   | entt          |            | 3.11.1           |                      | [github](https://github.com/skypjack/entt)                  |
| `X`   | magic_enum    |            | 0.8.2            |                      | [github](https://github.com/Neargye/magic_enum)             |
| `X`   | stb_image     |            | 2.28             |                      | [github](https://github.com/nothings/stb)                   |
|       |               |            |                  |                      |                                                             |
| `X`   | fmt           |            | 9.1.0            |                      | [github](https://github.com/fmtlib/fmt)                     |
| `X`   | glad          |            | 0.1.36           |                      | [glad](https://glad.dav1d.de/)                              |
| `X`   | glfw          |            | 3.3.8            |                      | [github](https://github.com/glfw/glfw)                      |
| `X`   | glm           |            | 0.9.9.8          |                      | [github](https://github.com/g-truc/glm)                     |
| `X`   | googletest    |            | 1.13.0           |                      | [github](https://github.com/google/googletest)              |
| `X`   | imgui         | to move    | docking (branch) |                      | [github](https://github.com/ocornut/imgui)                  |
| `X`   | imguizmo      | to move    | 1.84             |                      | [github](https://github.com/CedricGuillemet/ImGuizmo)       |
| `X`   | nfd           |            | 1.0.1            |                      | [github](https://github.com/btzy/nativefiledialog-extended) |
| `???` | shaderc       | `X`        | v2023.2          | spirv-tools, glslang | [github](https://github.com/google/shaderc/)                |
| `>X`  | glslang       | `X`        | 12.0.0           |                      | [github](https://github.com/KhronosGroup/glslang)           |
| `>X`  | SPIRV-Tools   | `X`        | v2023.1          | spirv-headers        | [github](https://github.com/KhronosGroup/SPIRV-Tools)       |
| `>>X` | SPIRV-Headers | `X`        | sdk-1.3.239.0    |                      | [github](https://github.com/KhronosGroup/SPIRV-Headers)     |
| `X`   | spdlog        |            | 1.11.0           | fmt                  | [github](https://github.com/gabime/spdlog)                  |
| `X`   | SPIRV-Cross   | `X`        | sdk-1.3.239.0    |                      | [github](https://github.com/KhronosGroup/SPIRV-Cross)       |
| `X`   | yaml-cpp      |            | 0.70             |                      | [github](https://github.com/jbeder/yaml-cpp)                |

## header-only

### DebugBreak

Version: 1.0
Depends: None
Source : [github](https://github.com/scottt/debugbreak)

### Magic Enum

Version: 0.8.2
Depends: None
Source : [github](https://github.com/Neargye/magic_enum)

### entt

Version: 3.11.1
Depends: None
Source : [github](https://github.com/skypjack/entt)

### stb

Version: stb_image-2.28
Depends:
Source : [github](https://github.com/nothings/stb)

## Libraries

### fmt

Version: 9.1.0
Depends: None
Source : [github](https://github.com/fmtlib/fmt)

### glad

Version: 0.1.36
Depends: None
Source : [glad](https://glad.dav1d.de/)

### glfw

Version: 3.3.8
Depends:
Source : [github](https://github.com/glfw/glfw)

### glm

Version: 0.9.9.8
Depends:
Source : [github](https://github.com/g-truc/glm)

### glslang

Version: 12.0.0
Depends:
Source : [gitbub](https://github.com/KhronosGroup/glslang)

### googletest

Version: 1.13.0
Depends:
Source : [github](https://github.com/google/googletest)

### imgui

use of a git submodule
Version: branch docking
Depends:
Source : [github](https://github.com/ocornut/imgui)

### imguizmo

use of a git submodule
Version: 1.84
Depends: imgui
Source : [github](https://github.com/CedricGuillemet/ImGuizmo)

### nfd

We use the 'extended' version which is a fork of the original one not maintained. 
Version: 1.0.1
Depends:
Source : [github](https://github.com/btzy/nativefiledialog-extended)

### shaderc

Version: 2023.2
Depends:
Source : [github](https://github.com/google/shaderc/)

### spdlog

Version: 1.11.0
Depends: fmt
Source : [github](https://github.com/gabime/spdlog)

### spirv-tools

Version:
Depends:
Source : [github](https://github.com/KhronosGroup/SPIRV-Tools)

### yaml-cpp


