"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent

file_modif = [
    "CMakeLists.txt",
    "cmake/msdfgenConfig.cmake.in",
    "core/Contour.h",
    "core/contour-combiners.h",
    "core/DistanceMapping.h",
    "core/edge-coloring.h",  # ***
    "core/edge-segments.h",
    "core/edge-selectors.h",
    "core/EdgeHolder.h",
    "core/equation-solver.h",  # ***
    "core/export-svg.h",  # ***
    "core/msdf-error-correction.h",
    "core/MSDFErrorCorrection.h",
    "core/Projection.h",
    "core/rasterization.h",
    "core/render-sdf.h",  # ***
    "core/save-bmp.h",  # ***
    "core/save-fl32.h",  # ***
    "core/save-rgba.h",  # ***
    "core/save-tiff.h",  # ***
    "core/Scanline.h",
    "core/sdf-error-estimation.h",  # ***
    "core/SDFTransformation.h",
    "core/Shape.h",
    "core/shape-description.h",  # ***
    "msdfgen.h",
]
corrections = [
    # CMake packages
    [b"find_package(Freetype", b"find_package(Freetype CONFIG", None],
    [b"find_package(tinyxml2", b"find_package(tinyxml2 CONFIG", None],
    [b"find_package(PNG", b"find_package(PNG CONFIG", None],
    # CMake configure
    [b"find_dependency(Freetype", b"find_package(Freetype CONFIG", None],
    [b"find_dependency(tinyxml2", b"find_package(tinyxml2 CONFIG", None],
    [b"find_dependency(PNG", b"find_package(PNG CONFIG", None],
    # class declarations
    [b"class Contour {", b"class MSDFGEN_PUBLIC Contour {", None],
    [
        b"class SimpleContourCombiner {",
        b"class MSDFGEN_PUBLIC SimpleContourCombiner {",
        None,
    ],
    [
        b"class OverlappingContourCombiner {",
        b"class MSDFGEN_PUBLIC OverlappingContourCombiner {",
        None,
    ],
    [b"class DistanceMapping {", b"class MSDFGEN_PUBLIC DistanceMapping {", None],
    [b"class EdgeSegment {", b"class MSDFGEN_PUBLIC EdgeSegment {", None],
    [
        b"class TrueDistanceSelector {",
        b"class MSDFGEN_PUBLIC TrueDistanceSelector {",
        None,
    ],
    [b"struct EdgeCache {", b"struct MSDFGEN_PUBLIC EdgeCache {", None],
    [
        b"class PerpendicularDistanceSelectorBase {",
        b"class MSDFGEN_PUBLIC PerpendicularDistanceSelectorBase {",
        None,
    ],
    [
        b"class PerpendicularDistanceSelector {",
        b"class MSDFGEN_PUBLIC PerpendicularDistanceSelector {",
        None,
    ],
    [
        b"class MultiDistanceSelector {",
        b"class MSDFGEN_PUBLIC MultiDistanceSelector {",
        None,
    ],
    [
        b"class MultiAndTrueDistanceSelector {",
        b"class MSDFGEN_PUBLIC MultiAndTrueDistanceSelector {",
        None,
    ],
    [b"class EdgeHolder {", b"class MSDFGEN_PUBLIC EdgeHolder {", None],
    [
        b"class MSDFErrorCorrection {",
        b"class MSDFGEN_PUBLIC MSDFErrorCorrection {",
        None,
    ],
    [b"class Projection {", b"class MSDFGEN_PUBLIC Projection {", None],
    [b"class Scanline {", b"class MSDFGEN_PUBLIC Scanline {", None],
    [b"class SDFTransformation {", b"class MSDFGEN_PUBLIC SDFTransformation {", None],
    [b"class Shape {", b"class MSDFGEN_PUBLIC Shape {", None],
    # functions
    [b"void rasterize(", b"MSDFGEN_PUBLIC void rasterize(", None],
    [
        b"void distanceSignCorrection(",
        b"MSDFGEN_PUBLIC void distanceSignCorrection(",
        None,
    ],
    [b"void generate", b"MSDFGEN_PUBLIC void generate", None],
    [b"void msdfErrorCorrection", b"MSDFGEN_PUBLIC void msdfErrorCorrection", None],
    [
        b"void msdfFastDistanceErrorCorrection",
        b"MSDFGEN_PUBLIC void msdfFastDistanceErrorCorrection",
        None,
    ],
    [
        b"void msdfFastEdgeErrorCorrection",
        b"MSDFGEN_PUBLIC void msdfFastEdgeErrorCorrection",
        None,
    ],
    [
        b"void msdfErrorCorrection_legacy",
        b"MSDFGEN_PUBLIC void msdfErrorCorrection_legacy",
        None,
    ],
]


class MsdfGenShared(Recipe):
    """
    Shared version
    """

    name = "msdfgen"
    version = "1.11"
    source_dir = "msdfgen"
    kind = "shared"
    dependencies = [
        {"name": "tinyxml2", "kind": "shared"},
        {"name": "libpng", "kind": "shared"},
        {"name": "zlib", "kind": "shared"},
        {"name": "freetype", "kind": "shared"},
    ]

    def source(self):
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
        self.cache_variables["MSDFGEN_DISABLE_SVG"] = "ON"
        self.cache_variables["MSDFGEN_CORE_ONLY"] = "OFF"
        self.cache_variables["MSDFGEN_BUILD_STANDALONE"] = "OFF"
        self.cache_variables["MSDFGEN_USE_VCPKG"] = "OFF"
        self.cache_variables["MSDFGEN_USE_OPENMP"] = "OFF"
        self.cache_variables["MSDFGEN_USE_CPP11"] = "ON"
        self.cache_variables["MSDFGEN_USE_SKIA"] = "OFF"
        self.cache_variables["MSDFGEN_INSTALL"] = "ON"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class MsdfGenStatic(MsdfGenShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "tinyxml2", "kind": "static"},
        {"name": "libpng", "kind": "static"},
        {"name": "zlib", "kind": "static"},
        {"name": "freetype", "kind": "static"},
    ]

    def configure(self):
        super().configure()
