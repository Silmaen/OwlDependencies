# Owl Dependencies

This project only aims to gather all dependencies for the Owl Engine.

See the git repository [OwlEngine](https://github.com/Silmaen/Owl) for the Engine code.

## Requirement

This project requires that DepManager is installed on the system and available
from PATH. Check it git repository: [DepManager](https://github.com/Silmaen/DepManager)
for more details.

## Get or Update submodules

After cloning this repository, if you don't have clone with the recursive option,
or if you need to update the repository, just run this command:

`git submodule update --init --recursive`

## Rebuild Package

Regenerate all the dependencies by running script:

## lib summary

platforms:
W : Windows x86_64
L : Linux x86_64
La64 : Linux aarch64

|     | name        | submodule? | platforms | custom cmake?             | version/tag      | dependency           | link                                                        |
|-----|-------------|------------|-----------|---------------------------|------------------|----------------------|-------------------------------------------------------------|
| `X` | debugbreak  | `X`        | n/a       | missing                   | 1.0              |                      | [github](https://github.com/scottt/debugbreak)              |
| `X` | entt        | `X`        | n/a       |                           | 3.11.1           |                      | [github](https://github.com/skypjack/entt)                  |
| `X` | magic_enum  | `X`        | n/a       |                           | 0.8.2            |                      | [github](https://github.com/Neargye/magic_enum)             |
| `X` | stb_image   | `0`        | n/a       | missing                   | 2.28             |                      | [github](https://github.com/nothings/stb)                   |
|     |             |            |           |                           |                  |                      |                                                             |
| `X` | fmt         | `X`        | W L La64  |                           | 10.0.0           |                      | [github](https://github.com/fmtlib/fmt)                     |
| `X` | glad        | `0`        | W L La64  | missing                   | 0.1.36           |                      | [glad](https://glad.dav1d.de/)                              |
| `X` | glfw        | `X`        | W L La64  |                           | 3.3.8            |                      | [github](https://github.com/glfw/glfw)                      |
| `X` | glm         | `X`        | W L La64  | replaced                  | 0.9.9.8          |                      | [github](https://github.com/g-truc/glm)                     |
| `X` | googletest  | `X`        | W L La64  |                           | 1.13.0           |                      | [github](https://github.com/google/googletest)              |
| `X` | imgui       | `X`        | W L La64  | missing                   | docking (branch) | glfw                 | [github](https://github.com/ocornut/imgui)                  |
| `X` | imguizmo    | `X`        | W L La64  | missing                   | 1.84             | imgui                | [github](https://github.com/CedricGuillemet/ImGuizmo)       |
| `X` | jsoncpp     | `X`        | W L La64  |                           | 1.9.5            |                      | [github](https://github.com/open-source-parsers/jsoncpp)    |
| `X` | mavsdk      | `X`        | W L La64  |                           | 1.4.17           | jsoncpp tinyxml2     | [github](https://github.com/mavlink/MAVSDK)                 |
| `X` | nfd         | `X`        | W L La64  |                           | 1.0.1            |                      | [github](https://github.com/btzy/nativefiledialog-extended) |
| `X` | shaderc     | `X`        | W L La64  | many modifs for packaging | v2023.2          | spirv-tools, glslang | [github](https://github.com/google/shaderc/)                |
| `X` | spdlog      | `X`        | W L La64  |                           | 1.11.0           | fmt                  | [github](https://github.com/gabime/spdlog)                  |
| `X` | SPIRV-Cross | `X`        | W L La64  |                           | sdk-1.3.243.0    |                      | [github](https://github.com/KhronosGroup/SPIRV-Cross)       |
| `X` | tinyxml2    | `X`        | W L La64  |                           | 9.0.0            |                      | [github](https://github.com/leethomason/tinyxml2)           |
| `X` | yaml-cpp    | `X`        | W L La64  |                           | 0.70             |                      | [github](https://github.com/jbeder/yaml-cpp)                |
|
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

Version: 10.0.0
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

### jsoncpp

use of a git submodule
Version: 1.9.5
Depends: 
Source : [github](https://github.com/CedricGuillemet/ImGuizmo)

### mavsdk

use of a git submodule
Version: 1.4.17
Depends: jsoncpp tinywml2
Source : [github](https://github.com/mavlink/MAVSDK)

### nfd

We use the 'extended' version which is a fork of the original one not maintained. 
Version: 1.0.1
Depends:
Source : [github](https://github.com/btzy/nativefiledialog-extended)

### opencv

use of a git submodule
Version: 4.8.0
Depends:
Source : [github](https://github.com/opencv/opencv)

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

### tinywml2

Version: 9.0.0
Depends:
Source : [github](https://github.com/leethomason/tinyxml2)

### yaml-cpp


