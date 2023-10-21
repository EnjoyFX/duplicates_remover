import os
import filecmp

from logger import logger


__version__ = '1.0.1'


class DuplicatesRemover:
    """
    Class for removing duplicates
    """
    empty_passed = 'Folder names should not be empty!'
    empty_real = 'Folder(s) should not be empty!'
    folders_same = 'Folders should be different!'
    files_found = '{} files found: {} inside {}"'
    removed_ok = 'File {} removed OK...'
    removed_bad = 'File {} not removed! Details: {}'
    version = f'{__version__}'

    def delete_duplicate_files(self,
                               source_dir: str,
                               target_dir: str,
                               deep_check=True):

        result = {"compared": 0, "deleted": 0}

        if source_dir and target_dir:
            source_dir = os.path.abspath(source_dir)
            target_dir = os.path.abspath(target_dir)
        else:
            logger.warning(self.empty_passed)
            return result

        if source_dir == target_dir:
            logger.warning(self.folders_same)
            return result

        logger.info(f"Deep scan mode: {'ON' if deep_check else 'OFF'}")

        source_files = os.listdir(source_dir)
        target_files = os.listdir(target_dir)
        src_count = len(source_files)
        trg_count = len(target_files)
        logger.info(self.files_found.format("Source", src_count, source_dir))
        logger.info(self.files_found.format("Target", trg_count, target_dir))
        if src_count == 0 or trg_count == 0:
            logger.warning(self.empty_real)
            return result

        # Compare and delete files
        for source_file in source_files:
            result["compared"] += 1
            source_file_path = os.path.join(source_dir, source_file)
            for target_file in target_files:
                target_file_path = os.path.join(target_dir, target_file)
                if filecmp.cmp(source_file_path,
                               target_file_path,
                               shallow=not deep_check):
                    try:
                        os.remove(target_file_path)  # remove from OS
                        logger.info(self.removed_ok.format(target_file_path))
                        target_files.remove(target_file)  # remove from list
                        result["deleted"] += 1
                    except OSError as e:
                        logger.warning(
                            self.removed_bad.format(target_file_path, e))
        return result
