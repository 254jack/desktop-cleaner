import os
import shutil
from pathlib import Path

home = Path.home()

folders = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".pub"],
    "Music": [".mp3", ".wav", ".rg", ".md", ".m4a"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".xz", ".deb"],
    "Scripts": [".py", ".sh", ".bat"],
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

# Ensure base folders exist
for folder in folders:
    folder_path = home / folder
    folder_path.mkdir(exist_ok=True)

def get_expected_folder(file_suffix: str) -> str:
    """Return the correct folder name for a file extension"""
    for folder, extensions in folders.items():
        if file_suffix.lower() in extensions:
            return folder
    return "Others"

def clean_directory(target: Path):
    """Clean misplaced files inside a directory and its subdirectories"""
    for root, _, files in os.walk(target, topdown=False):
        root_path = Path(root)

        for file in files:
            file_path = root_path / file
            ext = file_path.suffix.lower()
            correct_folder = get_expected_folder(ext)

            # Skip if file is already inside the correct main folder (or its subfolder)
            if (home / correct_folder) in file_path.parents:
                continue  # ✅ Correct place, leave it there

            # Otherwise → move to correct place
            destination = home / correct_folder / file
            if not destination.exists():
                shutil.move(str(file_path), str(destination))
                print(f"Moved {file_path} → {correct_folder}")
            else:
                print(f"Skipped {file_path}, already exists in {correct_folder}")

        # ✅ Delete empty folders (but not main categories or home)
        if root_path != home and root_path not in [home / f for f in folders]:
            try:
                root_path.rmdir()
                print(f"Deleted empty folder: {root_path}")
            except OSError:
                pass  # not empty

# 🚀 Run cleanup only for selected TARGET_DIRS
for target_dir in TARGET_DIRS:
    if target_dir.exists():
        print(f"\n🔹 Cleaning {target_dir} ...")
        clean_directory(target_dir)

