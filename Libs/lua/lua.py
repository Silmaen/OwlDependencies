"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class LuaShared(Recipe):
    """
    Shared version
    """

    name = "lua"
    version = "5.5.0"
    source_dir = "sources"
    kind = "shared"
    description = "Lua is a powerful, efficient, lightweight, embeddable scripting language."

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class LuaStatic(LuaShared):
    """
    Static version
    """

    kind = "static"
