"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GladShared(Recipe):
    """
    Shared version
    """
    name = "glad"
    version = "0.1.36"
    source_dir = "sources"
    kind = "shared"

    def configure(self):
        self.cache_variables["GLAD_VERSION_1"] = "ON"


class GladStatic(Recipe):
    """
    Shared version
    """
    name = "glad"
    version = "0.1.36"
    source_dir = "sources"
    kind = "static"

    def configure(self):
        self.cache_variables["GLAD_VERSION_1"] = "ON"


class GladSharedNew(Recipe):
    """
    Shared version
    """
    name = "glad"
    version = "2.0.4"
    source_dir = "sources"
    kind = "shared"


class GladStaticNew(Recipe):
    """
    Shared version
    """
    name = "glad"
    version = "2.0.4"
    source_dir = "sources"
    kind = "static"
