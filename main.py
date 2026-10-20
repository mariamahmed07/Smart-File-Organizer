
from pathlib import Path
import shutil


FILE_CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".webp", ".svg", ".ico", ".tiff"
    },
    "Documents": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf",
        ".odt", ".xls", ".xlsx", ".ppt", ".pptx",
        ".csv", ".md"
    },
    "Videos": {
        ".mp4", ".mkv", ".mov", ".avi", ".webm"
    },
    "Audio": {
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"
    },
    "Code": {
        ".py", ".js", ".ts", ".html", ".css", ".java",
        ".cpp", ".c", ".h", ".cs", ".php", ".json",
        ".sql", ".sh"
    },
    "Archives": {
        ".zip", ".rar", ".7z", ".tar", ".gz"
    },
}


def get_category(file_path):
    """Return the category for a file based on its extension."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Other"


def get_unique_destination(destination):
    """Choose a destination that does not overwrite an existing file."""
    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"

        if not candidate.exists():
            return candidate

        counter += 1


def plan_organization(folder_path):
    """
    Preview file moves without creating folders or moving files.
    Only direct, regular files are considered.
    """
    folder = Path(folder_path).expanduser().resolve()

    if not folder.exists():
        raise FileNotFoundError("The selected folder does not exist.")

    if not folder.is_dir():
        raise NotADirectoryError("The selected path is not a folder.")

    plan = []

    for file_path in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if not file_path.is_file() or file_path.is_symlink():
            continue

        category = get_category(file_path)
        destination_folder = folder / category
        destination = get_unique_destination(
            destination_folder / file_path.name
        )

        plan.append((file_path, destination))

    return plan


def organize_files(folder_path, preview=True):
    """
    Return a list of planned moves.
    In preview mode, make no changes.
    In execution mode, move files without overwriting existing files.
    """
    plan = plan_organization(folder_path)

    if preview:
        return plan

    completed = []

    for source, planned_destination in plan:
        planned_destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Recheck immediately before moving to avoid overwriting
        # a file that appeared after the preview.
        destination = get_unique_destination(planned_destination)

        try:
            shutil.move(str(source), str(destination))
        except OSError as error:
            print(f"Could not move {source.name}: {error}")
            continue

        completed.append((source, destination))

    return completed


def main():
    print("=" * 45)
    print("          SMART FILE ORGANIZER")
    print("=" * 45)
    print("Preview first. No files move until you confirm.")

    folder_input = input(
        "\nEnter the folder path to organize: "
    ).strip().strip('"')

    try:
        plan = organize_files(folder_input, preview=True)
    except (OSError, ValueError) as error:
        print(f"\nError: {error}")
        return

    if not plan:
        print("\nNo regular files found directly inside this folder.")
        return

    print("\n--- PREVIEW: Planned Moves ---")

    for source, destination in plan:
        print(f"{source.name}  ->  {destination.parent.name}/{destination.name}")

    print(f"\nFiles to organize: {len(plan)}")
    print("No changes have been made yet.")

    confirmation = input(
        "\nType YES to move these files, or anything else to cancel: "
    ).strip()

    if confirmation != "YES":
        print("Cancelled. Your files were not moved.")
        return

    try:
        completed = organize_files(folder_input, preview=False)
    except (OSError, ValueError) as error:
        print(f"\nError: {error}")
        return

    print(f"\nOrganization finished: {len(completed)} file(s) moved.")


if __name__ == "__main__":
    main()
