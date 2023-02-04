# Owl Dependencies

This project only aims to gather all dependencies for the Owl Engine

## Rebuild Package

Regenerate all the dependencies by running python script:

```bash
python3 PyUtils/regenerate.py
```

A cmake target `regenerate` will do the same or with the `all` target.

## lib summary

|     | name             | version | dependency | link                                            |
|-----|------------------|---------|------------|-------------------------------------------------|
| `X` | debugbreak       | 1.0     |            | [github](https://github.com/scottt/debugbreak)  |
| `X` | entt             | 3.11.1  |            | [github](https://github.com/skypjack/entt)      |
| `X` | magic_enum       | 0.8.2   |            | [github](https://github.com/Neargye/magic_enum) |
|     |                  |         |            |                                                 |
| `X` | fmt              | 9.1.0   |            | [github](https://github.com/fmtlib/fmt)         |
| `X` | glad             | 0.1.36  |            | [glad](https://glad.dav1d.de/)                  |
| ` ` | glfw             | 3.3.8   |            | [github](https://github.com/glfw/glfw)          |
| ` ` | glm              |         |            |                                                 |
| ` ` | glslang          |         |            |                                                 |
| ` ` | googletest       |         |            |                                                 |
| ` ` | imgui            |         |            |                                                 |
| ` ` | imguizmo         |         |            |                                                 |
| ` ` | nativefiledialog |         |            |                                                 |
| ` ` | shaderc          |         |            |                                                 |
| `X` | spdlog           | 1.11.0  | fmt        | [github](https://github.com/gabime/spdlog)      |
| ` ` | SPIRV-Cross      |         |            |                                                 |
| ` ` | SPIRV-Headers    |         |            |                                                 |
| ` ` | SPIRV-Tools      |         |            |                                                 |
| ` ` | stb              |         |            |                                                 |
| ` ` | yaml-cpp         |         |            |                                                 |

## header-only

### DebugBreak

Version: 1.0
Depends: None
Source: [github](https://github.com/scottt/debugbreak)

### Magic Enum

Version: 0.8.2
Depends: None
Source: [github](https://github.com/Neargye/magic_enum)

### entt

Version: 3.11.1
Depends: None
Source: [github](https://github.com/skypjack/entt)

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
Source: [github](https://github.com/glfw/glfw)

### spdlog

Version: 1.11.0
Depends: fmt
Source : [github](https://github.com/gabime/spdlog)
