
get_filename_component(ProjectId ${CMAKE_CURRENT_SOURCE_DIR} NAME)
add_custom_target(${ProjectId} ALL
        COMMAND ${EDEPMANAGER} build ${CMAKE_CURRENT_SOURCE_DIR})
add_dependencies(${ProjectId} glfw vulkan_sdk)
