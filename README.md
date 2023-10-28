# Duplicates Remover

Application with tiny UI for removing duplicates. Class `DuplicatesRemover` from `duplicates_remover.py` can be used without UI.
No external libraries needed.


Example of usage:
```python
from duplicates_remover import DuplicatesRemover

d = DuplicatesRemover()
result = d.delete_duplicate_files("c:/source_folder", "c:/target_folder")
```
Format of output for `delete_duplicate_files()` method:

dictionary: `{"compared": number_of_compared, "deleted": number_of_deleted}`
