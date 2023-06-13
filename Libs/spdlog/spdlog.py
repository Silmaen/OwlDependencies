"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe
from shutil import copyfile
from tempfile import gettempdir
from pathlib import Path

here = Path(__file__).parent


class SpdlogShared(Recipe):
    """
    Shared version
    """
    name = "spdlog"
    version = "1.11.0"
    source_dir = "spdlog"
    kind = "shared"
    dependencies = [{"name": "fmt", "kind": "shared"}]

    def source(self):
        """
        Done at the beginning of the procedure
        """
        temp = Path(gettempdir()) / "depbuilder"
        temp.mkdir(exist_ok=True, parents=True)
        source = here / Path(self.source_dir)
        # backup
        copyfile(source / "include" / "spdlog" / "common.h", temp / "spdlog_common.h")
        # use ours
        copyfile(here / "configs" / "include" / "spdlog" / "common.h", source / "include" / "spdlog" / "common.h")

    def configure(self):
        self.cache_variables["SPDLOG_BUILD_SHARED"] = "ON"
        self.cache_variables["SPDLOG_BUILD_EXAMPLE"] = "OFF"
        self.cache_variables["SPDLOG_BUILD_TESTS"] = "OFF"
        self.cache_variables["SPDLOG_BUILD_BENCH"] = "OFF"
        self.cache_variables["SPDLOG_FMT_EXTERNAL"] = "ON"
        if self.settings["os"] == "Windows":
            self.cache_variables["SPDLOG_WCHAR_SUPPORT"] = "ON"
            self.cache_variables["SPDLOG_WCHAR_FILENAMES"] = "ON"

    def clean(self):
        temp = Path(gettempdir()) / "depbuilder"
        temp.mkdir(exist_ok=True, parents=True)
        source = here / Path(self.source_dir)
        copyfile(temp / "spdlog_common.h", source / "include" / "spdlog" / "common.h")


class SpdlogStatic(Recipe):
    """
    Shared version
    """
    name = "spdlog"
    version = "1.11.0"
    source_dir = "spdlog"
    kind = "static"
    dependencies = [{"name": "fmt", "kind": "static"}]

    def source(self):
        """
        Done at the beginning of the procedure
        """
        temp = Path(gettempdir()) / "depbuilder"
        temp.mkdir(exist_ok=True, parents=True)
        source = here / Path(self.source_dir)
        # backup
        copyfile(source / "include" / "spdlog" / "common.h", temp / "spdlog_common.h")
        # use ours
        copyfile(here / "configs" / "include" / "spdlog" / "common.h", source / "include" / "spdlog" / "common.h")

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

    def clean(self):
        temp = Path(gettempdir()) / "depbuilder"
        temp.mkdir(exist_ok=True, parents=True)
        source = here / Path(self.source_dir)
        copyfile(temp / "spdlog_common.h", source / "include" / "spdlog" / "common.h")
