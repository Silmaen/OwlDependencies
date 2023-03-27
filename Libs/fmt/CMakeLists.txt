
get_filename_component(ProjectId ${CMAKE_CURRENT_SOURCE_DIR} NAME)
add_custom_target(${ProjectId}
        COMMAND ${EDEPMANAGER} build ${CMAKE_CURRENT_SOURCE_DIR})
add_dependencies(${ProjectId} fmt)
