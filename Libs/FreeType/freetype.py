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
        b"find_package(BrotliDec MODULE",
        None,
    ],
    [
        b"find_package(HarfBuzz",
        b"find_package(HarfBuzz MODULE",
        None,
    ],
    [
        b"find_package(PNG",
        b"find_package(PNG MODULE",
        None,
    ],
    [
        b"find_package(ZLIB",
        b"find_package(ZLIB MODULE",
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
        {"name": "libpng", "kind": "shared"},
        {"name": "harfbuzz", "kind": "static"},
        {"name": "brotli", "kind": "shared"},
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
        pass


class FreeTypeStatic(FreeTypeShared):
    """
    Static version
    """

    kind = "static"
