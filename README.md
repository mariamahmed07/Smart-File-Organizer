# 📁 Smart File Organizer

A safe, command-line file organizer built with Python. It sorts files into folders based on their extensions, with a preview mode and explicit confirmation before moving anything.

## ✨ Features

- **Preview First:** See the planned file moves before making changes.
- **Confirmation Required:** Files are moved only after entering `YES`.
- **Automatic Categorization:** Organize images, documents, videos, audio, code, archives, and other files.
- **Collision Protection:** Existing files are not intentionally overwritten; alternative filenames are generated when needed.
- **Safe Testing:** Automated tests use temporary directories and generated sample files.
- **No External Dependencies:** Uses Python's standard library.

## 🛠️ Technologies

- Python 3
- `pathlib`
- `shutil`
- `unittest`
- `tempfile`

## 📂 Project Structure

```text
smart-file-organizer/
├── main.py
├── test_file_organizer.py
├── README.md
└── .gitignore
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mariamahmed07/smart-file-organizer.git
cd smart-file-organizer
```

### 2. Run the application

```bash
python main.py
```

### 3. Run automated tests

```bash
python -m unittest -v test_file_organizer.py
```

## 📖 How to Use

1. Enter the path to the folder you want to organize.
2. Review the preview of planned file moves.
3. Type `YES` to confirm, or enter anything else to cancel.
4. Review the resulting category folders.

## 🗂️ File Categories

| Category | Examples |
|---|---|
| Images | `.jpg`, `.png`, `.webp` |
| Documents | `.pdf`, `.docx`, `.txt`, `.csv` |
| Videos | `.mp4`, `.mkv`, `.mov` |
| Audio | `.mp3`, `.wav`, `.flac` |
| Code | `.py`, `.js`, `.html`, `.css` |
| Archives | `.zip`, `.rar`, `.7z` |
| Other | Unrecognized extensions |

## 🧪 Automated Testing

The test suite checks file categorization, preview behavior, actual organization, filename collisions, invalid folder paths, subfolder handling, and unknown file types.

Tests create temporary files and directories and do not use personal folders.

## 🔐 Safety Notes

- Always review the preview before confirming.
- Start with a test folder containing non-important files.
- The organizer processes regular files directly inside the selected folder; it does not recursively process subfolders.
- No file deletion feature is included.
- The application does not provide a full transaction or automatic rollback if a move fails partway through.
- Keep backups of important files before organizing them.

## 🔮 Future Improvements

- Recursive organization with safeguards
- Undo and restore operations
- Custom file categories
- A graphical user interface
- Organization logs and reports

## 👩‍💻 Author

**Mariam Ahmed**

GitHub: [@mariamahmed07](https://github.com/mariamahmed07)

---

*Project 4 of the 30 Projects in 30 Days challenge.*
