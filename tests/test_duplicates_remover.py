import unittest
import os

from unittest.mock import patch
from tempfile import TemporaryDirectory as temp_dir
from duplicates_remover import DuplicatesRemover


class TestDuplicatesRemover(unittest.TestCase):

    def setUp(self):
        self.duplicates_remover = DuplicatesRemover()

    def test_delete_duplicate_files(self):
        # test with 1) empty passed & 2) the same passed
        with patch('duplicates_remover.logger') as mock_logger:
            result = self.duplicates_remover.delete_duplicate_files(
                "", "", deep_check=True)
            self.assertEqual(result, {"compared": 0, "deleted": 0})
            mock_logger.warning.assert_called_with(
                self.duplicates_remover.empty_passed)

            result = self.duplicates_remover.delete_duplicate_files(
                "the_same", "the_same", deep_check=True)
            self.assertEqual(result, {"compared": 0, "deleted": 0})
            mock_logger.warning.assert_called_with(
                self.duplicates_remover.folders_same)

        # Create temp dirs with test files
        with temp_dir() as source_dir, temp_dir() as target_dir:
            # Create test files in the source and target directories
            source_file1 = os.path.join(source_dir, "file1.txt")
            target_file1 = os.path.join(target_dir, "file1.txt")
            source_file2 = os.path.join(source_dir, "file2.txt")
            target_file2 = os.path.join(target_dir, "file2.txt")

            # Creating  a pair of files with same cintent
            # and another pair - with different content:
            content = "Same content"
            with open(source_file1, "w") as f:
                f.write(content)
            with open(target_file1, "w") as f:
                f.write(content)

            with open(source_file2, "w") as f:
                f.write(content+content)
            with open(target_file2, "w") as f:
                f.write(content+content+content)

            # Mock the logger to capture log messages
            with patch('duplicates_remover.logger') as mock_logger:
                result = self.duplicates_remover.delete_duplicate_files(
                    source_dir, target_dir, deep_check=True)

                # Checking the 'result' variable is correct
                self.assertEqual(result["compared"], 2)
                self.assertEqual(result["deleted"], 1)

                # Checking logs
                mock_logger.info.assert_called_with(
                    f"File {target_file1} removed OK..."
                    f"(same as {source_file1})")

                # Ensure that the duplicate file in target removed
                self.assertFalse(os.path.exists(target_file1))
                self.assertTrue(os.path.exists(target_file2))

                # Checking warnings if any
                self.assertFalse(mock_logger.warning.called)


if __name__ == '__main__':
    unittest.main()
