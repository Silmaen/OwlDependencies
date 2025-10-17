import re
import subprocess
from argparse import ArgumentParser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, Optional

global_verbosity = 0


def parse_version(tag: str) -> Optional[Tuple[int, ...]]:
    """Parse version numbers from tag (e.g., 'v1.2.3' -> (1, 2, 3))."""
    # Extract numbers from tag
    numbers = re.findall(r"\d+", tag)
    if not numbers:
        return None
    return tuple(int(n) for n in numbers)


def get_tag_date(submodule_path, tag: str) -> Optional[datetime]:
    """Get the creation date of a tag."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cI", tag],
        cwd=submodule_path,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return datetime.fromisoformat(result.stdout.strip())
        except ValueError:
            return None
    return None


def get_submodules():
    """Get the list of submodules."""
    result = subprocess.run(
        ["git", "submodule", "status"], capture_output=True, text=True, check=True
    )
    submodules = []
    for line in result.stdout.strip().split("\n"):
        if line:
            parts = line.split()
            commit = parts[0].lstrip("-+")
            path = parts[1]
            submodules.append((commit, path))
    return submodules


def is_valid_tag(tag):
    """Check if tag contains a number and doesn't contain excluded terms."""
    if not tag:
        return False
    tag_lower = tag.lower()
    exclude = [
        "rc",
        "bcr",
        "beta",
        "preview",
        "freetype2",
        "tiny-curl",
        "openal-soft",
        "windows",
        "yaml-cpp",
        "png2uri",
        "pngmeta",
        "snapshot",
    ]
    for term in exclude:
        if term in tag_lower:
            return False
    return bool(re.search(r"\d", tag))


def get_current_tag(submodule_path):
    """Get the current tag of the submodule."""
    result = subprocess.run(
        ["git", "describe", "--tags", "--exact-match"],
        cwd=submodule_path,
        capture_output=True,
        text=True,
    )
    tag = result.stdout.strip() if result.returncode == 0 else None
    return tag


def get_latest_remote_tag(submodule_path, current_tag: Optional[str]):
    """Get the most recent tag from the server."""
    subprocess.run(["git", "fetch", "--tags"], cwd=submodule_path, capture_output=True)
    result = subprocess.run(
        ["git", "tag"],
        cwd=submodule_path,
        capture_output=True,
        text=True,
        check=True,
    )

    all_tags = result.stdout.strip().split("\n")
    valid_tags = [tag for tag in all_tags if is_valid_tag(tag)]

    if not valid_tags:
        return None

    # Filter tags by date if current tag exists
    if current_tag:
        current_date = get_tag_date(submodule_path, current_tag)
        if current_date:
            cutoff_date = current_date - timedelta(days=365)
            filtered_tags = []
            for tag in valid_tags:
                tag_date = get_tag_date(submodule_path, tag)
                if tag_date and tag_date >= cutoff_date:
                    filtered_tags.append(tag)
            valid_tags = filtered_tags

    if not valid_tags:
        return None

    # Sort by parsed version numbers
    def version_key(tag):
        version = parse_version(tag)
        return version if version else (0,)

    sorted_tags = sorted(valid_tags, key=version_key, reverse=True)
    return sorted_tags[0] if sorted_tags else None


def main():
    global global_verbosity
    print("Checking submodules...\n")
    parser = ArgumentParser(description="Check for submodule updates")
    parser.add_argument(
        "--verbose", "-v", action="count", default=0, help="Increase verbosity level"
    )
    args = parser.parse_args()

    global_verbosity = args.verbose

    submodules = get_submodules()

    for commit, path in submodules:
        if global_verbosity > 0:
            print(f"Submodule: {path}")
        else:
            print(f"Submodule: {path}", end="")
        submodule_path = Path(path)

        if not submodule_path.exists():
            print(f"  ⚠️  Path not found")
            continue

        current_tag = get_current_tag(submodule_path)
        latest_tag = get_latest_remote_tag(submodule_path, current_tag)

        if global_verbosity > 0:
            print(f"  Current tag: {current_tag or 'No tag'}")
            print(f"  Latest tag: {latest_tag or 'No tag'}")

        if current_tag and latest_tag and current_tag != latest_tag:
            print(f"  ✨ Update available: {current_tag} → {latest_tag}")
        elif not current_tag and latest_tag:
            print(f"  ℹ️  Tag available: {latest_tag}")
        else:
            print(f"  ✓ Up to date")
        if global_verbosity > 0:
            print()


if __name__ == "__main__":
    main()
