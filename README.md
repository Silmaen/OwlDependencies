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

|     | name          | submodule? | platforms | custom cmake? | version/tag    | dependency                    | link                                                        |
|-----|---------------|------------|-----------|---------------|----------------|-------------------------------|-------------------------------------------------------------|
| `X` | debugbreak    | `X`        | n/a       | missing       | 1.0            |                               | [github](https://github.com/scottt/debugbreak)              |
| `X` | entt          | `X`        | n/a       |               | 3.12.2         |                               | [github](https://github.com/skypjack/entt)                  |
| `X` | magic_enum    | `X`        | n/a       |               | 0.9.5          |                               | [github](https://github.com/Neargye/magic_enum)             |
| `X` | stb_image     | `0`        | n/a       | missing       | 2.28           |                               | [github](https://github.com/nothings/stb)                   |
| `X` | mavlink       | `X`        | n/a       |               | 2.0.1          |                               | [github](https://github.com/mavlink/mavlink)                |
|     |               |            |           |               |                |                               |                                                             |
| `X` | cpptrace      | `X`        | W L       |               | 0.3.1          |                               | [github](https://github.com/jeremy-rifkin/cpptrace)         |
| `X` | curl          | `X`        | W L       |               | 8.5.0          |                               | [github](https://github.com/curl/curl)                      |
| `X` | fmt           | `X`        | W L       |               | 10.2.1         |                               | [github](https://github.com/fmtlib/fmt)                     |
| `X` | glad          | `0`        | W L       | missing       | 2.0.4          |                               | [glad](https://glad.dav1d.de/)                              |
| `X` | glfw          | `X`        | W L       |               | 3.3.9          |                               | [github](https://github.com/glfw/glfw)                      |
| `X` | glm           | `X`        | W L       |               | 0.9.9.9        |                               | [github](https://github.com/g-truc/glm)                     |
| `X` | googletest    | `X`        | W L       |               | 1.14.0         |                               | [github](https://github.com/google/googletest)              |
| `X` | imgui         | `X`        | W L       | missing       | 1.90.1-docking | glfw vulkan_sdk               | [github](https://github.com/ocornut/imgui)                  |
| `X` | imguizmo      | `X`        | W L       | missing       | 1.90.1         | imgui vulkan_sdk              | [github](https://github.com/CedricGuillemet/ImGuizmo)       |
| `X` | jsoncpp       | `X`        | W L       |               | 1.9.5          |                               | [github](https://github.com/open-source-parsers/jsoncpp)    |
| `X` | mavsdk        | `X`        | W L       |               | 2.0.1          | jsoncpp tinyxml2 curl mavlink | [github](https://github.com/mavlink/MAVSDK)                 |
| `X` | nfd           | `X`        | W L       |               | 1.1.1          |                               | [github](https://github.com/btzy/nativefiledialog-extended) |
| `X` | spdlog        | `X`        | W L       |               | 1.13.0         | fmt                           | [github](https://github.com/gabime/spdlog)                  |
| `X` | tinyxml2      | `X`        | W L       |               | 10.0.0         |                               | [github](https://github.com/leethomason/tinyxml2)           |
| `X` | tinyobjloader | `X`        | W L       |               | 2.0.0          |                               | [github](https://github.com/tinyobjloader/tinyobjloader)    |
| `X` | yaml-cpp      | `X`        | W L       |               | 0.8.0          |                               | [github](https://github.com/jbeder/yaml-cpp)                |
| `X` | vulkan_sdk    | `X`        | W L       |               | 1.3.275        |                               | [github](https://github.com/KhronosGroup/Vulkan-Loader)     |
