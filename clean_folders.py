import os
import shutil
import json
import filecmp
from pathlib import Path

# ==================================================
# CONFIGURATION
# ==================================================

home = Path.home()
config_file = Path(__file__).parent / "config.json"

# Default folder mappings
default_folders = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".pub", ".odt"],
    "Music": [".mp3", ".wav", ".ogg", ".m4a", ".flac"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".xz", ".7z", ".deb"],
    "Scripts": [".py", ".sh", ".bat", ".ps1"],
    "Others": []
}

TARGET_DIRS = [
    home / "Desktop",
    home / "Downloads",
    home / "Documents",
    home / "Pictures",
    home / "Music",
    home / "Videos"
]

# ==================================================
# LOAD CONFIG
# ==================================================
def load_config():
    """Load config from file or use defaults."""
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except Exception:
            print("⚠️  Error reading config.json, using defaults.")
    return default_folders


folders = load_config()

# Ensure category folders exist
for folder in folders:
    (home / folder).mkdir(exist_ok=True)


# ==================================================
# HELPER FUNCTIONS
# ==================================================
def get_expected_folder(file_suffix: str) -> str:
    """Return the correct folder name for a file extension."""
    for folder, extensions in folders.items():
        if file_suffix.lower() in extensions:
            return folder
    return "Others"


def resolve_conflict(destination: Path, source: Path) -> Path:
    """
    Handle duplicate files:
    - If contents are same, skip move
    - Else, rename with (1), (2), etc.
    """
    if destination.exists():
        try:
            if filecmp.cmp(str(source), str(destination), shallow=False):
                print(f"⚠️  Skipped {source}, identical file exists in {destination.parent.name}")
                return None
        except Exception:
            pass  # fallback to renaming

        # Rename
        counter = 1
        new_dest = destination
        while new_dest.exists():
            new_dest = destination.with_name(f"{destination.stem}({counter}){destination.suffix}")
            counter += 1
        return new_dest
    return destination


def clean_directory(target: Path, stats: dict):
    """Clean misplaced files inside a directory and its subdirectories."""
    for root, _, files in os.walk(target, topdown=False):
        root_path = Path(root)

        for file in files:
            file_path = root_path / file
            ext = file_path.suffix.lower()
            correct_folder = get_expected_folder(ext)

            # Skip if file already inside correct folder
            if (home / correct_folder) in file_path.parents:
                stats["skipped"] += 1
                continue

            # Destination handling
            destination = home / correct_folder / file
            destination = resolve_conflict(destination, file_path)

            if destination:
                shutil.move(str(file_path), str(destination))
                print(f"✅ Moved {file_path} → {correct_folder}")
                stats["moved"] += 1
            else:
                stats["skipped"] += 1

        # Delete empty folders (but not main categories or home)
        if root_path != home and root_path not in [home / f for f in folders]:
            try:
                root_path.rmdir()
                print(f"🗑️ Deleted empty folder: {root_path}")
                stats["folders_removed"] += 1
            except OSError:
                pass  # not empty


# ==================================================
# MAIN
# ==================================================
def main():
    stats = {"moved": 0, "skipped": 0, "folders_removed": 0}

    for target_dir in TARGET_DIRS:
        if target_dir.exists():
            print(f"\n🔹 Cleaning {target_dir} ...")
            clean_directory(target_dir, stats)

    # Final summary
    print("\n📊 Cleanup Summary:")
    print(f"   ✅ Files moved: {stats['moved']}")
    print(f"   ⚠️ Files skipped: {stats['skipped']}")
    print(f"   🗑️ Folders removed: {stats['folders_removed']}")


if __name__ == "__main__":
    main()
