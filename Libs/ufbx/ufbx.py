"""
Depmanager recipes
"""

from pathlib import Path
from shutil import copy2

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class UfbxStatic(Recipe):
    """
    Shared version
    """

    name = "ufbx"
    version = "0.20.1"
    source_dir = "ufbx"
    kind = "static"

    def source(self):
        print(
            f"Copying from {here / 'modif' / 'CMakeLists.txt'} to {here / self.source_dir / 'CMakeLists.txt'}"
        )
        copy2(
            here / "modif" / "CMakeLists.txt", here / self.source_dir / "CMakeLists.txt"
        )
        copy2(
            here / "modif" / "ufbx-config.cmake.in",
            here / self.source_dir / "ufbx-config.cmake.in",
        )

    def clean(self):
        print(f"Removing {here / self.source_dir / 'CMakeLists.txt'}")
        (here / self.source_dir / "CMakeLists.txt").unlink()
        (here / self.source_dir / "ufbx-config.cmake.in").unlink()

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
