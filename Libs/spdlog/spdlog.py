"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class SpdlogShared(Recipe):
    """
    Shared version
    """

    name = "spdlog"
    version = "1.14.1"
    source_dir = "spdlog"
    kind = "shared"
    dependencies = [{"name": "fmt", "kind": "shared"}]

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
