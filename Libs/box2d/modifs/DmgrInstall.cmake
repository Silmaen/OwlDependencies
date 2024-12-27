include(GNUInstallDirs)

set(version_config ${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake)
set(project_config ${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config.cmake)
set(targets_export_name ${PROJECT_NAME}-targets)

include(CMakePackageConfigHelpers)
set(target_name ${PROJECT_NAME})

write_basic_package_version_file(
        ${version_config}
        VERSION ${VERSION}
        COMPATIBILITY AnyNewerVersion)
configure_package_config_file(
        ${PROJECT_SOURCE_DIR}/${PROJECT_NAME}-config.cmake.in
        ${project_config}
        INSTALL_DESTINATION lib/cmake)

install(TARGETS ${target_name} EXPORT ${targets_export_name}-$<CONFIG>
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        PUBLIC_HEADER DESTINATION include
        FRAMEWORK DESTINATION lib
        CONFIGURATIONS $<CONFIG>
)
install(FILES ${BOX2D_API_FILES}
        DESTINATION include)
# simde dependency
install(TARGETS simde EXPORT ${targets_export_name}-$<CONFIG>
        CONFIGURATIONS $<CONFIG>
)

# Install version, config and target files.
install(
        FILES ${project_config} ${version_config}
        DESTINATION lib/cmake/
)
install(EXPORT ${targets_export_name}-$<CONFIG>
        FILE ${targets_export_name}.cmake
        DESTINATION lib/cmake/
        NAMESPACE ${PROJECT_NAME}::)
