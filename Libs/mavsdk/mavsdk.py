"""
Depmanager recipes
"""
from pathlib import Path

from depmanager.api.recipe import Recipe

root_dir = Path(__file__).resolve().parent

ignore_list = [
    "SUPERBUILD",
    "BUILD_TESTS",
    "BUILD_MAVSDK_SERVER",
    "BUILD_WITH_PROTO_REFLECTION",
]


class MavLink(Recipe):
    name = "mavlink"
    version = "2.0.1"
    source_dir = "sources/mavlink"
    kind = "header"

    def __init__(self, possible: bool = True):
        super().__init__(possible)
        self.reqSave = None

    def source(self):
        path = root_dir / self.source_dir / "pymavlink" / "requirements.txt"
        if path.exists():
            with open(path, "r") as fp:
                self.reqSave = fp.read()
            with open(path, "w") as fp:
                fp.write("")
        self.reqSave = ""

    def clean(self):
        if self.reqSave in ["", None]:
            return
        path = root_dir / self.source_dir / "pymavlink" / "requirements.txt"
        with open(path, "w") as fp:
            fp.write(self.reqSave)


class MavSDKShared(Recipe):
    """
    Shared version
    """

    name = "mavsdk"
    version = "2.0.1"
    source_dir = "sources/MAVSDK"
    kind = "shared"
    dependencies = [
        {"name": "jsoncpp", "kind": kind},
        {"name": "tinyxml2", "kind": kind},
        {"name": "curl", "kind": kind},
        {"name": "mavlink", "kind": "header"},
    ]

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"


class MavSDKStatic(MavSDKShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "jsoncpp", "kind": kind},
        {"name": "tinyxml2", "kind": kind},
        {"name": "curl", "kind": kind},
        {"name": "mavlink", "kind": "header"},
    ]
