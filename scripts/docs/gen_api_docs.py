import sys
from pathlib import Path

import mkdocs_gen_files

sys.path.insert(0, str(Path(__file__).parent))

from api_reference import API_REFERENCE

api_reference_root = "reference"
api_reference_idx_page = f"{api_reference_root}/index.md"

with mkdocs_gen_files.open(api_reference_idx_page, "w") as idx_file:
    idx_file.write("# Reference\n\n")
    idx_file.write(
        """This reference manual serves as a complete guide to the 
        modules, classes, and functions provided by the `geolysis` Python 
        package, offering clear explanations of their purpose, usage, and 
        behavior.\n\n
        """
    )
    idx_file.write("\n")
    idx_file.write(
        """**For learning how to use `geolysis`, check the 
        [usage documentation](../user_guide/index.md)**\n\n
        """
    )
    idx_file.write("\n")

for module_name in API_REFERENCE:
    module_output = f"{api_reference_root}/{module_name}.md"
    module_summary = API_REFERENCE[module_name]["short_summary"]

    with (
        mkdocs_gen_files.open(module_output, "w") as f,
        mkdocs_gen_files.open(api_reference_idx_page, "a") as idx_file,
    ):
        f.write(f"# {module_name}\n\n")
        f.write(f"::: {module_name}\n")
        f.write(f"    options:\n")
        f.write(f"       summary: true\n")
        # f.write(f"          classes: true\n")
        # f.write(f"          functions: true\n")
        # f.write(f"       members: true\n")
        # f.write(f"       members_order: __all__\n")

        idx_file.write(
            f"- [{module_name}]({module_name}.md): {module_summary}\n")
