"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

file_modif = [
    "CMakeLists.txt",
]
corrections = [
    [
        b"find_package(BrotliDec",
        b"find_package(BrotliDec CONFIG",
        None,
    ],
    [
        b"find_package(HarfBuzz",
        b"find_package(HarfBuzz CONFIG",
        None,
    ],
    [
        b"find_package(PNG",
        b"find_package(PNG CONFIG",
        None,
    ],
    [
        b"find_package(ZLIB",
        b"find_package(ZLIB CONFIG",
        None,
    ],
    [b'set(HARFBUZZ_MIN_VERSION "2.0.0")', b"set(HARFBUZZ_MIN_VERSION)", None],
    [
        b"target_include_directories(freetype PRIVATE ${ZLIB_INCLUDE_DIRS})",
        b"#target_include_directories(freetype PRIVATE ${ZLIB_INCLUDE_DIRS})",
        None,
    ],
    [
        b'list(APPEND PKGCONFIG_REQUIRES_PRIVATE "zlib")',
        b'#list(APPEND PKGCONFIG_REQUIRES_PRIVATE "zlib")',
        None,
    ],
    [
        b"target_link_libraries(freetype PRIVATE ${ZLIB_LIBRARIES})",
        b"target_link_libraries(freetype PRIVATE ZLIB::ZLIB)",
        None,
    ],
    [
        b"target_compile_definitions(freetype PRIVATE ${PNG_DEFINITIONS})",
        b"#target_compile_definitions(freetype PRIVATE ${PNG_DEFINITIONS})",
        None,
    ],
    [
        b"target_include_directories(freetype PRIVATE ${PNG_INCLUDE_DIRS})",
        b"#target_include_directories(freetype PRIVATE ${PNG_INCLUDE_DIRS})",
        None,
    ],
    [
        b'list(APPEND PKGCONFIG_REQUIRES_PRIVATE "libpng")',
        b'#list(APPEND PKGCONFIG_REQUIRES_PRIVATE "libpng")',
        None,
    ],
    [
        b"target_link_libraries(freetype PRIVATE ${PNG_LIBRARIES})",
        b"target_link_libraries(freetype PRIVATE PNG::PNG)",
        None,
    ],
    [
        b"target_include_directories(freetype PRIVATE ${HarfBuzz_INCLUDE_DIRS})",
        b"#target_include_directories(freetype PRIVATE ${HarfBuzz_INCLUDE_DIRS})",
        None,
    ],
    [
        b'list(APPEND PKGCONFIG_REQUIRES_PRIVATE "harfbuzz >= ${HARFBUZZ_MIN_VERSION}")',
        b'#list(APPEND PKGCONFIG_REQUIRES_PRIVATE "harfbuzz >= ${HARFBUZZ_MIN_VERSION}")',
        None,
    ],
    [
        b"target_link_libraries(freetype PRIVATE ${HarfBuzz_LIBRARY})",
        b"target_link_libraries(freetype PRIVATE harfbuzz)",
        None,
    ],
    [
        b"target_compile_definitions(freetype PRIVATE ${BROTLIDEC_DEFINITIONS})",
        b"#target_compile_definitions(freetype PRIVATE ${BROTLIDEC_DEFINITIONS})",
        None,
    ],
    [
        b"target_include_directories(freetype PRIVATE ${BROTLIDEC_INCLUDE_DIRS})",
        b"#target_include_directories(freetype PRIVATE ${BROTLIDEC_INCLUDE_DIRS})",
        None,
    ],
    [
        b'list(APPEND PKGCONFIG_REQUIRES_PRIVATE "libbrotlidec")',
        b'#list(APPEND PKGCONFIG_REQUIRES_PRIVATE "libbrotlidec")',
        None,
    ],
    [
        b"target_link_libraries(freetype PRIVATE ${BROTLIDEC_LIBRARIES})",
        b"target_link_libraries(freetype PRIVATE brotli)",
        None,
    ],
]


class FreeTypeShared(Recipe):
    """
    Shared version
    """

    name = "freetype"
    version = "2.13.3"
    source_dir = "freetype"
    kind = "shared"
    dependencies = [
        {"name": "libpng", "kind": "static"},
        {"name": "harfbuzz", "kind": "static"},
        {"name": "brotli", "kind": "shared"},
        {"name": "zlib", "kind": "shared"},
    ]

    def source(self):
        # Files to modify
        for file in file_modif:
            path = self.path / self.source_dir / file
            if not path.exists():
                print(f"Error: file {file} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != file:
                        continue
                lines = lines.replace(correction[0], correction[1])
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {file} @ {path} found and modified.")

    def clean(self):
        # Files to restore
        for file in file_modif:
            path = self.path / self.source_dir / file
            if not path.exists():
                print(f"Error: file {file} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != file:
                        continue
                lines = lines.replace(correction[1], correction[0])
                pass
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {file} @ {path} restored.")

    def configure(self):
        self.cache_variables["FT_DISABLE_BZIP2"] = "ON"


class FreeTypeStatic(FreeTypeShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "libpng", "kind": "static"},
        {"name": "harfbuzz", "kind": "static"},
        {"name": "brotli", "kind": "static"},
        {"name": "zlib", "kind": "static"},
    ]
