"""
Depmanager recipes
"""
from shutil import copyfile
from tempfile import gettempdir
from depmanager.api.recipe import Recipe
from pathlib import Path

here = Path(__file__).parent


class NfdShared(Recipe):
    """
    Shared version
    """
    name = "nfd"
    version = "1.0.2"
    source_dir = "nativefiledialog-extended"
    kind = "shared"

    def source(self):
        """
        Done at the beginning of the procedure
        """
        temp = Path(gettempdir()) / "depbuilder"
        temp.mkdir(exist_ok=True, parents=True)
        source = here / Path(self.source_dir)
        # backup
        copyfile(source / "src" / "CMakeLists.txt", temp / "nfd_CMakeLists.txt")
        # use ours
        copyfile(here / "configs" / "CMakeLists.txt", source / "src" / "CMakeLists.txt")

    def configure(self):
        self.cache_variables["NFD_BUILD_TESTS"] = "OFF"
        self.cache_variables["NFD_INSTALL"] = "ON"

    def clean(self):
        temp = Path(gettempdir()) / "depbuilder"
        temp.mkdir(exist_ok=True, parents=True)
        source = here / Path(self.source_dir)
        copyfile(temp / "nfd_CMakeLists.txt", source / "src" / "CMakeLists.txt")


class NfdStatic(Recipe):
    """
    Shared version
    """
    name = "nfd"
    version = "1.0.2"
    source_dir = "nativefiledialog-extended"
    kind = "static"

    def source(self):
        """
        Done at the beginning of the procedure
        """
        temp = Path(gettempdir()) / "depbuilder"
        temp.mkdir(exist_ok=True, parents=True)
        source = here / Path(self.source_dir)
        # backup
        copyfile(source / "src" / "CMakeLists.txt", temp / "nfd_CMakeLists.txt")
        # use ours
        copyfile(here / "configs" / "CMakeLists.txt", source / "src" / "CMakeLists.txt")

    def configure(self):
        self.cache_variables["NFD_BUILD_TESTS"] = "OFF"
        self.cache_variables["NFD_INSTALL"] = "ON"

    def clean(self):
        temp = Path(gettempdir()) / "depbuilder"
        temp.mkdir(exist_ok=True, parents=True)
        source = here / Path(self.source_dir)
        copyfile(temp / "nfd_CMakeLists.txt", source / "src" / "CMakeLists.txt")

