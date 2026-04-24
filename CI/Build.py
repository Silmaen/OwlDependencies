#!/usr/bin/env python3
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from shutil import rmtree
from sys import stderr

from depmanager.api.builder import find_recipes
from depmanager.api.internal.machine import Machine
from depmanager.api.internal.recipe_builder import RecipeBuilder
from depmanager.api.internal.toolset import Toolset
from depmanager.api.local import LocalManager
from depmanager.api.package import PackageManager

here = Path(__file__).resolve().parent
root = here.parent
lib_dir = root / "Libs"

MAX_WORKERS = 2


class Parameters:
    def __init__(self):
        self.verbosity = 0
        self.do_pull = True
        self.do_push = True
        self.do_build = True
        self.machine = Machine(True)
        self.cross_info = {"SINGLE_THREAD": False}
        self.filter = ""

    def __repr__(self):
        return (
            f"Parameters(verbosity={self.verbosity}, do_pull={self.do_pull}, "
            f"do_push={self.do_push}, do_build={self.do_build}, "
            f"machine={self.machine}, cross_info={self.cross_info}) filter={self.filter}"
        )


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
    parser.add_argument(
        "--toolset",
        type=str,
        default="",
        help="The toolset to use, format: '<name>:<compiler_path>:<abi>.",
    )
    parser.add_argument(
        "--filter",
        type=str,
        default="",
        help="The Filter on the recipes.",
    )
    args = parser.parse_args()

    if args.toolset not in ["", None]:
        if ":" not in args.toolset:
            print("ERROR: Toolset must be in the format '<name>:<compiler_path>:<abi>'")
            exit(1)
        toolset_info = args.toolset.split(":")
        if len(toolset_info) != 3:
            print("ERROR: Toolset must be in the format '<name>:<compiler_path>:<abi>'")
            exit(1)
        parameters.machine = Machine(
            True,
            Toolset(
                name=toolset_info[0],
                compiler_path=toolset_info[1],
                abi=toolset_info[2],
            ),
        )
    if args.filter not in ["", None]:
        parameters.filter = args.filter

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
        abi = "any"
    else:
        if "CROSS_ARCH" in parameters.cross_info:
            arch = parameters.cross_info["CROSS_ARCH"]
        else:
            arch = parameters.machine.arch
        if "CROSS_OS" in parameters.cross_info:
            os = parameters.cross_info["CROSS_OS"]
        else:
            os = parameters.machine.os
        abi = parameters.machine.default_abi
        glibc = parameters.machine.glibc
    return {
        "name": recipe.name,
        "version": recipe.version,
        "os": os,
        "arch": arch,
        "kind": recipe.kind,
        "abi": abi,
        "glibc": glibc,
    }


def reorder_recipes(recipes, package_manager: PackageManager, strict_dep: bool = False):
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
            for i_vers in range(min(len(vers_aa), len(vers_bb))):
                if vers_aa[i_vers] == vers_bb[i_vers]:
                    continue
                return safe_to_int(vers_aa[i_vers]) < safe_to_int(vers_bb[i_vers])
            return len(vers_aa) < len(vers_bb)

        rec_found = False
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
            rec_found = True
            break
        return rec_found

    def find_package(criteria):
        q = package_manager.query(criteria)
        return len(q) > 0

    new_recipe = []
    stalled = False
    i = -1
    filter_ = re.compile(".*")
    if parameters.filter not in ["", None]:
        filter_ = re.compile(parameters.filter)
    all_dep_list = []
    while not stalled:
        stalled = True
        i += 1
        if parameters.verbosity > 2:
            print(f"turn {i}")
        for rec in recipes:
            if rec in new_recipe:  # add recipe only once
                continue
            if not filter_.match(rec.name):
                if rec.name not in [d["name"] for d in all_dep_list]:
                    continue
            if len(rec.dependencies) == 0:  # no dependency -> just add it!
                stalled = False
                new_recipe.append(rec)
                if parameters.verbosity > 2:
                    print(f" -- inserting {rec.name} with no dependency")
            else:
                dep_satisfied = True
                deps_list = []
                for dep in rec.dependencies:
                    deps_list.append(dep["name"])
                    all_dep_list.append(dep)
                    if not _find_recipe(new_recipe, dep):
                        dep_satisfied = False
                stalled = False
                if dep_satisfied:
                    new_recipe.append(rec)
                    if parameters.verbosity > 2:
                        print(
                            f" -- inserting {rec.name} with all dependency full filled {deps_list}"
                        )
    # add dependencies not satisfied
    stalled = False
    while not stalled:
        stalled = True
        for rrec in new_recipe:
            print(f"new recipe {rrec.name}")
            for dep in rrec.dependencies:
                if not _find_recipe(new_recipe, dep):
                    if parameters.verbosity > 2:
                        print(
                            f" -- adding dependency {dep['name']} for {rrec.name} ({rrec.kind})"
                        )
                    new_recipe.append(dep)
                    stalled = False
                else:
                    if parameters.verbosity > 2:
                        print(
                            f" -- dependency {dep['name']} for {rrec.name} ({rrec.kind}) already satisfied"
                        )

    # add unresolved dependency recipes
    continue_exec = True
    for rec in recipes:
        if rec in new_recipe:  # add recipe only once
            continue
        if not filter_.match(rec.name):
            continue
        missing = []
        found = []
        for dep in rec.dependencies:
            if _find_recipe(new_recipe, dep) and not find_package(dep):
                found.append(dep["name"])
            else:
                missing.append(dep["name"])
        if len(missing) == 0:
            new_recipe.append(rec)
            continue
        if strict_dep:
            print(
                f"ERROR: Target {rec.to_str()} has missing dependency: {missing} but found: {found}.",
                file=stderr,
            )
            continue_exec = False
        else:
            if parameters.verbosity > 1:
                print(
                    f"WARNING: inserting {rec.to_str()} with missing dependency: {missing} but found: {found}."
                )
            new_recipe.append(rec)
    if not continue_exec:
        exit(1)
    # replace the list
    return new_recipe


def classify_recipe(package_manager, recipe):
    """
    Query the remote only to decide if a recipe needs rebuilding.

    Returns (recipe, is_on_remote). Local cache is NOT consulted here: the
    remote is the source of truth for 'what should end up in the remote'.
    """
    qr = query_from_recipe(recipe)
    remote_result = package_manager.query(qr, remote_name="default")
    return recipe, len(remote_result) > 0


def remove_stale_local(package_manager, recipe):
    """
    If a recipe is missing from remote but a local copy exists, wipe the local
    copy so the rebuild starts clean (and the push uploads a fresh artifact).
    """
    local_result = package_manager.query(query_from_recipe(recipe))
    for pkg in local_result:
        if parameters.verbosity > 0:
            print(
                f"Removing stale local package {pkg.properties.get_as_str()} "
                f"(missing from remote, will rebuild)."
            )
        package_manager.remove_package(pkg, remote_name="")


def pull_dep(package_manager, dep_query):
    """
    Ensure a dependency is available locally. Skips if already local.
    add_from_remote handles transitive sub-deps automatically.
    """
    if len(package_manager.query(dep_query)) > 0:
        return
    remote_result = package_manager.query(dep_query, remote_name="default")
    if len(remote_result) > 0:
        if parameters.verbosity > 0:
            print(f"Pulling {remote_result[0].properties.get_as_str()} from remote.")
        package_manager.add_from_remote(remote_result[0], "default")


def collect_build_deps(to_build, recipes):
    """
    Return the list of unique dep query dicts needed to build everything in
    to_build. Only immediate deps are collected; add_from_remote will pull
    sub-deps transitively when it fetches a package.
    """
    by_name_kind = {(r.name, r.kind): r for r in recipes}
    to_build_keys = {(r.name, r.kind) for r in to_build}
    seen = set()
    deps = []
    for recipe in to_build:
        for dep in recipe.dependencies:
            key = (dep["name"], dep.get("kind", recipe.kind))
            if key in seen or key in to_build_keys:
                continue
            seen.add(key)
            # Prefer a full query (matches current platform) when we know the recipe
            if key in by_name_kind:
                deps.append(query_from_recipe(by_name_kind[key]))
            else:
                deps.append(dep)
    return deps


def main():
    """
    Do all builds
    """
    parse_args()

    # list the recipes
    local_manager = LocalManager()
    package_manager = PackageManager(system=local_manager.get_sys())
    rem = package_manager.get_default_remote()
    if rem is None:
        print("ERROR: no default remote configured.", file=stderr)
        exit(1)
    #
    # find all recipes
    #
    err_code = 0
    recipes = find_recipes(lib_dir, 1)
    recipes = reorder_recipes(recipes, package_manager, True)

    #
    # Classification against the remote (parallel). Local cache is ignored here:
    # a recipe missing from the remote must be rebuilt even if present locally.
    #
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        classifications = list(
            ex.map(lambda r: classify_recipe(package_manager, r), recipes)
        )

    recipe_to_build = [r for r, on_remote in classifications if not on_remote]

    if parameters.verbosity > 0:
        on_remote_count = sum(1 for _, on_remote in classifications if on_remote)
        print(
            f"{on_remote_count} recipe(s) already on remote, "
            f"{len(recipe_to_build)} recipe(s) to build."
        )

    nb = len(recipe_to_build)
    if nb == 0:
        print("Remote is up-to-date, nothing to build.")
        exit(0)

    print(f"{nb} recipe{['', 's'][nb > 1]} needs to be build.")
    if parameters.verbosity > 0:
        for recipe in recipe_to_build:
            print(f" --- Building: {recipe.to_str()}...")

    #
    # Remove stale local copies of recipes we are about to rebuild.
    # (User rule: if missing from remote, wipe local and rebuild from scratch.)
    #
    for recipe in recipe_to_build:
        remove_stale_local(package_manager, recipe)
    local_manager.get_sys().local_database.dependencies.clear()
    local_manager.get_sys().local_database.reload()

    #
    # Pull only the build-time deps of the recipes we are going to build.
    # add_from_remote recursively pulls sub-deps when it fetches a package.
    # Pulls are serialised: depmanager's add_from_location uses a shared
    # temp dir (self.__sys.temp_path / "pack") that is not safe to share
    # across threads.
    #
    if parameters.do_pull:
        deps_to_pull = collect_build_deps(recipe_to_build, recipes)
        if deps_to_pull:
            if parameters.verbosity > 0:
                print(f"Ensuring {len(deps_to_pull)} dep(s) are available locally...")
            for dep_query in deps_to_pull:
                pull_dep(package_manager, dep_query)
            local_manager.get_sys().local_database.dependencies.clear()
            local_manager.get_sys().local_database.reload()

    #
    # do the build
    #
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
            toolset=parameters.machine.toolset,
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
