
get_filename_component(ProjectId ${CMAKE_CURRENT_SOURCE_DIR} NAME)
add_custom_target(${ProjectId} ALL
        COMMAND ${EDEPMANAGER} build ${CMAKE_CURRENT_SOURCE_DIR})
add_dependencies(${ProjectId} zlib)
add_dependencies(${ProjectId} zstd)
add_dependencies(${ProjectId} brotli)
