"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

file_modif = [
    "imgui_node_editor/imgui_extra_math.h",
    "imgui_node_editor/imgui_extra_math.inl",
]
corrections = [
    [
        b"inline ImVec2 operator*(const float lhs, const ImVec2& rhs);",
        b"# if IMGUI_VERSION_NUM < 19270\ninline ImVec2 operator*(const float lhs, const ImVec2& rhs);\n# endif",
        "imgui_node_editor/imgui_extra_math.h",
    ],
    [
        b"inline ImVec2 operator*(const float lhs, const ImVec2& rhs)\n{\n    return ImVec2(lhs * rhs.x, lhs * rhs.y);\n}",
        b"# if IMGUI_VERSION_NUM < 19270\ninline ImVec2 operator*(const float lhs, const ImVec2& rhs)\n{\n    return ImVec2(lhs * rhs.x, lhs * rhs.y);\n}\n# endif",
        "imgui_node_editor/imgui_extra_math.inl",
    ],
]


class ImguiNodeEditor(Recipe):
    """
    Static version
    """

    name = "imgui_node_editor"
    version = "0.9.4"
    source_dir = "sources"
    kind = "static"
    dependencies = [
        {"name": "imgui", "kind": "shared"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]
    description = "Node editor built around Dear ImGui."

    def source(self):
        for file in file_modif:
            path = self.path / self.source_dir / file
            if not path.exists():
                print(f"Error: file {file} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != file:
                        continue
                lines = lines.replace(correction[0], correction[1])
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {file} @ {path} found and modified.")

    def clean(self):
        for file in file_modif:
            path = self.path / self.source_dir / file
            if not path.exists():
                print(f"Error: file {file} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != file:
                        continue
                lines = lines.replace(correction[1], correction[0])
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {file} @ {path} restored.")

    def configure(self):
        self.cache_variables["PROJECT_VERSION"] = self.version
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
