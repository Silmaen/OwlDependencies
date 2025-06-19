"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

file_modif = [
    "CMakeLists.txt",
]
corrections = [
    [
        b"cmake_minimum_required(VERSION 3.4)",
        b"cmake_minimum_required(VERSION 3.5)",
        None,
    ],
]


class YamlCppShared(Recipe):
    """
    Shared version
    """

    name = "yaml-cpp"
    version = "0.8.0"
    source_dir = "yaml-cpp"
    kind = "shared"

    def source(self):
        # Files to modify
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
        # Files to restore
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
                pass
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {file} @ {path} restored.")

    def configure(self):
        self.cache_variables["YAML_CPP_BUILD_CONTRIB"] = "OFF"
        self.cache_variables["YAML_CPP_BUILD_TOOLS"] = "OFF"
        self.cache_variables["YAML_CPP_BUILD_TESTS"] = "OFF"


class YamlCppStatic(YamlCppShared):
    """
    Static version
    """

    kind = "static"
