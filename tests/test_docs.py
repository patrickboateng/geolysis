import pathlib

from mktestdocs import check_md_file

fpath = pathlib.Path("docs")

check_md_file(fpath=fpath / "dev_guide" / "style_guide.md")

# @pytest.mark.parametrize('fpath',
#                          pathlib.Path("docs"),
#                          ids=str)
# def test_check_md_file(fpath):
#     check_md_file(fpath=fpath / "style_guide.md", memory=True)
