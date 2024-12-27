"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent

file_modif = [
    "include/spdlog/common.h",
]
corrections = [
    [
        b"fmt::basic_format_string",
        b"fmt::fstring",
        None,
    ],
]


class SpdlogShared(Recipe):
    """
    Shared version
    """

    name = "spdlog"
    version = "1.15.0"
    source_dir = "spdlog"
    kind = "shared"
    dependencies = [{"name": "fmt", "kind": "shared"}]

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
        self.cache_variables["SPDLOG_BUILD_SHARED"] = "ON"
        self.cache_variables["SPDLOG_BUILD_EXAMPLE"] = "OFF"
        self.cache_variables["SPDLOG_BUILD_TESTS"] = "OFF"
        self.cache_variables["SPDLOG_BUILD_BENCH"] = "OFF"
        self.cache_variables["SPDLOG_FMT_EXTERNAL"] = "ON"
        if self.settings["os"] == "Windows":
            self.cache_variables["SPDLOG_WCHAR_SUPPORT"] = "ON"
            self.cache_variables["SPDLOG_WCHAR_FILENAMES"] = "ON"


class SpdlogStatic(SpdlogShared):
    """
    Static  version
    """

    kind = "static"
    dependencies = [{"name": "fmt", "kind": "static"}]

    def configure(self):
        self.cache_variables["SPDLOG_BUILD_SHARED"] = "OFF"
        self.cache_variables["SPDLOG_BUILD_EXAMPLE"] = "OFF"
        self.cache_variables["SPDLOG_BUILD_TESTS"] = "OFF"
        self.cache_variables["SPDLOG_BUILD_BENCH"] = "OFF"
        self.cache_variables["SPDLOG_FMT_EXTERNAL"] = "ON"
        if self.settings["os"] == "Windows":
            self.cache_variables["SPDLOG_WCHAR_SUPPORT"] = "ON"
            self.cache_variables["SPDLOG_WCHAR_FILENAMES"] = "ON"
        elif self.settings["os"] == "Linux":
            self.cache_variables["SPDLOG_BUILD_PIC"] = "ON"
