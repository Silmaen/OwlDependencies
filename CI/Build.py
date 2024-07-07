#!/usr/bin/env python3
from pathlib import Path
from shutil import rmtree
from sys import stderr

from depmanager.api.builder import find_recipes
from depmanager.api.internal.machine import Machine
from depmanager.api.internal.recipe_builder import RecipeBuilder
from depmanager.api.local import LocalManager
from depmanager.api.package import PackageManager

here = Path(__file__).resolve().parent
root = here.parent
lib_dir = root / "Libs"


class Parameters:
    def __init__(self):
        self.verbosity = 0
        self.do_pull = True
        self.do_push = True
        self.do_build = True
        self.machine = Machine(True)
        self.cross_info = {"SINGLE_THREAD": False}


parameters = Parameters()


def parse_args():
    from argparse import ArgumentParser

    global parameters
    parser = ArgumentParser()
    parser.add_argument(
        "--verbose", "-v", action="count", default=0, help="The verbosity level."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Do nothing print the commands."
    )
    parser.add_argument(
        "--no-push", action="store_true", help="Do not push the results."
    )
    args = parser.parse_args()
    print(f"verbosity {args.verbose}")
    parameters.verbosity = args.verbose
    if args.dry_run:
        parameters.do_pull = False
        parameters.do_push = False
        parameters.do_build = False
    else:
        if args.no_push:
            parameters.do_push = False


def query_from_recipe(recipe):
    glibc = ""
    if recipe.kind == "header":
        arch = "any"
        os = "any"
        compiler = "any"
    else:
        if "CROSS_ARCH" in parameters.cross_info:
            arch = parameters.cross_info["CROSS_ARCH"]
        else:
            arch = parameters.machine.arch
        if "CROSS_OS" in parameters.cross_info:
            os = parameters.cross_info["CROSS_OS"]
        else:
            os = parameters.machine.os
        compiler = parameters.machine.default_compiler
        glibc = parameters.machine.glibc
    return {
        "name": recipe.name,
        "version": recipe.version,
        "os": os,
        "arch": arch,
        "kind": recipe.kind,
        "compiler": compiler,
        "glibc": glibc,
    }


def reorder_recipes(recipes):
    """
    Reorder the recipes to take the dependencies into account.
    """

    def _find_recipe(rec_list: list, criteria: dict):
        def version_lt(vers_a: str, vers_b: str) -> bool:
            def safe_to_int(vers: str):
                from re import match

                crr = match(r"^\D*(\d+)", vers)
                if crr:
                    return int(crr.group(1))
                else:
                    return 0

            if vers_a == vers_b:
                return False
            vers_aa = vers_a.split(".")
            vers_bb = vers_b.split(".")
            for i in range(min(len(vers_aa), len(vers_bb))):
                if vers_aa[i] == vers_bb[i]:
                    continue
                return safe_to_int(vers_aa[i]) < safe_to_int(vers_bb[i])
            return len(vers_aa) < len(vers_bb)

        found = False
        for a_rec in rec_list:
            if "name" in criteria:
                if a_rec.name != criteria["name"]:
                    continue
            if "kind" in criteria:
                if a_rec.kind != criteria["kind"]:
                    continue
            if "version" in criteria:
                if version_lt(a_rec.version, criteria["version"]):
                    continue
            found = True
            break
        return found

    new_recipe = []
    stalled = False
    while not stalled:
        for rec in recipes:
            stalled = True
            if rec in new_recipe:  # add recipe only once
                continue
            if len(rec.dependencies) == 0:  # no dependency -> just add it!
                stalled = False
                new_recipe.append(rec)
            else:
                dep_satisfied = True
                for dep in rec.dependencies:
                    if not _find_recipe(new_recipe, dep):
                        dep_satisfied = False
                if dep_satisfied:
                    stalled = False
                    new_recipe.append(rec)
    # add unresolved dependency recipes
    for rec in recipes:
        if rec in new_recipe:  # add recipe only once
            continue
        if parameters.verbosity > 1:
            print(f"WARNING: inserting {rec.to_str()} with missing dependency.")
        new_recipe.append(rec)
    # replace the list
    return new_recipe


def main():
    """
    Do all builds
    """
    parse_args()
    # list the recipes
    local_manager = LocalManager(verbosity=parameters.verbosity)
    package_manager = PackageManager(
        system=local_manager.get_sys(), verbosity=parameters.verbosity
    )
    rem = package_manager.get_default_remote()
    #
    # find all recipes
    #
    err_code = 0
    recipes = find_recipes(lib_dir, 2)
    recipes = reorder_recipes(recipes)
    recipe_to_build = []
    #
    # Select only what need to be build right now!
    #   Eventually pull package from remote
    #
    if rem is not None:
        for recipe in recipes:
            query_result = package_manager.query(query_from_recipe(recipe))
            if len(query_result):
                if parameters.verbosity > 0:
                    print(f"Package {recipe.to_str()} found locally, no build.")
                continue
            query_result = package_manager.query(
                query_from_recipe(recipe), remote_name="default"
            )
            if len(query_result) > 0:
                if parameters.verbosity > 0:
                    print(
                        f"Package {recipe.to_str()} found on remote, pulling, no build."
                    )
                if parameters.do_pull:
                    package_manager.add_from_remote(query_result[0], "default")
                continue
            recipe_to_build.append(recipe)
    nb = len(recipe_to_build)
    if nb == 0:
        print("Nothing else to build!")
        exit(0)
    else:
        print(f"{nb} recipe{['', 's'][nb > 1]} needs to be build.")
        if parameters.verbosity > 0:
            for recipe in recipe_to_build:
                print(f" --- Building: {recipe.to_str()}...")
    #
    # do the build
    #
    recipe_to_build = reorder_recipes(recipe_to_build)
    temp_path = local_manager.get_sys().temp_path / "builder"
    for recipe in recipe_to_build:
        if parameters.verbosity > 0:
            print(f"Building: {recipe.to_str()}...")
        recipe.cache_variables = {}  # reset cache between builds !!
        if temp_path.exists():
            rmtree(temp_path, ignore_errors=True)
        temp_path.mkdir(parents=True, exist_ok=True)
        builder = RecipeBuilder(
            recipe=recipe,
            temp=temp_path,
            local=local_manager.get_sys(),
            cross_info=parameters.cross_info,
        )
        if not builder.has_recipes():
            print("WARNING Something gone wrong with the recipe!", file=stderr)
            continue
        if parameters.do_build:
            if not builder.build():
                err_code += 1
        local_manager.get_sys().local_database.dependencies.clear()
        local_manager.get_sys().local_database.reload()
    rmtree(temp_path, ignore_errors=True)
    #
    # do the push
    #
    for recipe in recipe_to_build:
        packs = package_manager.query(query_from_recipe(recipe))
        if len(packs) == 0:
            if parameters.do_build:
                print(f"ERROR: recipe {recipe.to_str()} should be built", file=stderr)
                err_code += 1
            else:
                print(f"HINT: recipe {recipe.to_str()} should be built")
            continue
        print(f"Pushing {packs[0].properties.get_as_str()} to te remote!")
        if parameters.do_push:
            package_manager.add_to_remote(packs[0], "default")
    if err_code != 0:
        exit(1)


if __name__ == "__main__":
    main()
