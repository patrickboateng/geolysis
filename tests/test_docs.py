import pathlib

from mktestdocs import check_md_file

file_1 = pathlib.Path("docs") / "index.md"

_test_files = [file_1]

for file_path in _test_files:
    check_md_file(fpath=file_path)
