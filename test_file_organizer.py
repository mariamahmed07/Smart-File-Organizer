
import tempfile
import unittest
from pathlib import Path

from main import (
    get_category,
    plan_organization,
    organize_files,
)


class TestSmartFileOrganizer(unittest.TestCase):

    def test_file_categories(self):
        self.assertEqual(get_category(Path("photo.JPG")), "Images")
        self.assertEqual(get_category(Path("report.pdf")), "Documents")
        self.assertEqual(get_category(Path("video.mp4")), "Videos")
        self.assertEqual(get_category(Path("script.py")), "Code")
        self.assertEqual(get_category(Path("archive.zip")), "Archives")
        self.assertEqual(get_category(Path("unknown.xyz")), "Other")

    def test_preview_does_not_move_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            sample = folder / "photo.jpg"
            sample.write_text("test image", encoding="utf-8")

            plan = plan_organization(folder)

            self.assertEqual(len(plan), 1)
            self.assertTrue(sample.exists())
            self.assertFalse((folder / "Images").exists())

    def test_actual_organization(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            sample = folder / "report.pdf"
            sample.write_text("test document", encoding="utf-8")

            completed = organize_files(folder, preview=False)

            destination = folder / "Documents" / "report.pdf"

            self.assertEqual(len(completed), 1)
            self.assertFalse(sample.exists())
            self.assertTrue(destination.exists())
            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                "test document"
            )

    def test_existing_file_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            source = folder / "photo.jpg"
            source.write_text("new content", encoding="utf-8")

            images = folder / "Images"
            images.mkdir()
            existing = images / "photo.jpg"
            existing.write_text("existing content", encoding="utf-8")

            plan = plan_organization(folder)

            self.assertEqual(len(plan), 1)
            self.assertEqual(plan[0][1].name, "photo_1.jpg")

            completed = organize_files(folder, preview=False)

            self.assertEqual(len(completed), 1)
            self.assertEqual(
                existing.read_text(encoding="utf-8"),
                "existing content"
            )
            self.assertTrue((images / "photo_1.jpg").exists())

    def test_invalid_folder_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing"

            with self.assertRaises(FileNotFoundError):
                plan_organization(missing)

    def test_subfolders_are_not_processed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            nested = folder / "nested"
            nested.mkdir()
            (nested / "photo.jpg").write_text(
                "test image",
                encoding="utf-8"
            )

            plan = plan_organization(folder)

            self.assertEqual(plan, [])

    def test_unknown_files_go_to_other(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            sample = folder / "data.xyz"
            sample.write_text("sample", encoding="utf-8")

            completed = organize_files(folder, preview=False)

            self.assertTrue((folder / "Other" / "data.xyz").exists())
            self.assertEqual(len(completed), 1)


if __name__ == "__main__":
    unittest.main()
