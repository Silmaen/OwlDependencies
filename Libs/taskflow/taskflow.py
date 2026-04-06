"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class TaskflowShared(Recipe):
    """
    Header-only version
    """

    name = "taskflow"
    version = "4.0.0"
    source_dir = "taskflow"
    kind = "header"
    description = "Taskflow is a fast C++ header-only library to help you quickly write parallel and heterogeneous programs with complex task dependencies."

    def configure(self):
        self.cache_variables["TF_BUILD_TESTS"] = False
        self.cache_variables["TF_BUILD_EXAMPLES"] = False
