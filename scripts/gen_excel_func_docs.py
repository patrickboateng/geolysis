import json
import os

import mkdocs_gen_files

script_dir = os.path.dirname(__file__)
functions_metadata_filepath = os.path.join(script_dir, "functions.json")

with open(functions_metadata_filepath, "r") as f:
    function_metadatas = json.load(f).get("functions", [])

    for function_metadata in function_metadatas:
        func_name = function_metadata["name"]
        func_desc = function_metadata["description"]
        filename = f"excel/functions/{func_name.lower().replace('_', '-')}.md"

        func_params = function_metadata["parameters"]
        func_params_names = ", ".join(
            [
                f"[{param['name']}]" if param.get("optional") else param[
                    "name"]
                for param in func_params
            ]
        )

        with mkdocs_gen_files.open(filename, "w") as fp:
            func_fullname = f"GEOLYSIS.{func_name}"
            fp.write(f"# {func_fullname} function\n\n")
            fp.write(f"{func_desc}\n\n")
            fp.write("## Syntax\n\n")
            fp.write(f"{func_fullname}({func_params_names})\n\n")
            fp.write(
                f"The {func_fullname} function syntax has the following arguments:\n\n"
            )

            for param in func_params:
                param_name = param["name"]
                param_type = param["type"]
                param_desc = param["description"]
                required = ", _Required_" if param.get("optional") else ""
                fp.write(
                    f"- **{param_name}** (_{param_type}_ {required}) {param_desc}\n"
                )

    with mkdocs_gen_files.open("excel/functions/index.md", "w") as fp:
        fp.write("# GEOLYSIS Microsoft Excel Functions\n\n")
        for func in function_metadatas:
            func_name = func["name"]
            fp.write(
                f"- [{func_name}]({func_name.lower().replace('_', '-')}.md)\n\n")
