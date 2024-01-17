"""
Depmanager recipes
"""
import os
import shutil
import subprocess
from pathlib import Path
from sys import executable

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


def copy_tree_overwrite(source: Path, destination: Path):
    """
    Copy a directory into another, keeping existing files, overwriting destination files
    :param source: From.
    :param destination: To.
    """
    for root, dirs, files in os.walk(source):
        relative = Path(root).relative_to(source)
        dest_root = destination / relative
        src_root = Path(root)
        for _dir in dirs:
            dest = dest_root / relative / _dir
            dest.mkdir(parents=True, exist_ok=True)
        for _file in files:
            src = src_root / _file
            dest = dest_root / _file
            shutil.copy2(src, dest)


class ShadercShared(Recipe):
    """
    Shared version
    """

    name = "shaderc"
    version = "1.3.275"
    source_dir = "sources"
    kind = "shared"

    def source(self):
        print(f"Do copytree {self.path / self.source_dir / 'modif'} -> {self.path / self.source_dir}")
        copy_tree_overwrite(self.path / self.source_dir / "modif", self.path / self.source_dir)

    def common_configure(self):
        self.cache_variables["pack_version"] = self.version
        self.cache_variables["DO_INSTALL"] = "ON"
        self.cache_variables["SHADERC_SKIP_TESTS"] = "ON"
        self.cache_variables["SHADERC_SKIP_EXAMPLES"] = "ON"
        self.cache_variables["SHADERC_SKIP_COPYRIGHT_CHECK"] = "ON"
        self.cache_variables["ENABLE_GLSLANG_BINARIES"] = "OFF"
        self.cache_variables["ENABLE_SPVREMAPPER"] = "OFF"
        self.cache_variables["SPIRV_SKIP_EXECUTABLES"] = "ON"
        self.cache_variables["SPIRV_SKIP_TESTS"] = "ON"
        self.cache_variables["SPIRV_TOOLS_BUILD_STATIC"] = "OFF"
        self.cache_variables["BUILD_SHARED_LIBS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["PYTHON_EXECUTABLE"] = executable

    def configure(self):
        self.common_configure()
        self.cache_variables["SPIRV_TOOLS_BUILD_STATIC"] = "OFF"
        self.cache_variables["BUILD_SHARED_LIBS"] = "ON"

    def clean(self):
        print("Do clean by git reset!")
        subprocess.run("git reset --hard", shell=True, cwd=self.path/self.source_dir/"glslang")
        subprocess.run("git reset --hard", shell=True, cwd=self.path/self.source_dir/"SPIRV-Headers")


class ShadercStatic(ShadercShared):
    """
    Any version
    """

    kind = "static"

    def configure(self):
        self.common_configure()
        self.cache_variables["SPIRV_TOOLS_BUILD_STATIC"] = "ON"
        self.cache_variables["BUILD_SHARED_LIBS"] = "OFF"
