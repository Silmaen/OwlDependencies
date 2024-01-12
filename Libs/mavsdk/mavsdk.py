"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

ignore_list = [
    "SUPERBUILD",
    "BUILD_TESTS",
    "BUILD_MAVSDK_SERVER",
    "BUILD_WITH_PROTO_REFLECTION",
]


class MavSDKShared(Recipe):
    """
    Shared version
    """

    name = "mavsdk"
    version = "2.0.1"
    source_dir = "MAVSDK"
    kind = "shared"
    dependencies = [
        {"name": "jsoncpp", "kind": kind},
        {"name": "tinyxml2", "kind": kind},
    ]


class MavSDKStatic(MavSDKShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "jsoncpp", "kind": kind},
        {"name": "tinyxml2", "kind": kind},
    ]
