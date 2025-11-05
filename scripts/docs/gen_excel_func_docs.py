import json

import requests
import mkdocs_gen_files


def _get_function_metadata():
    functions_metadata_link = "https://excel.geolysis.io/functions.json"
    response = requests.get(functions_metadata_link)
    return json.loads(response.text)


excel_functions_index_page = "excel/functions/index.md"

with mkdocs_gen_files.open(excel_functions_index_page, "w") as fp:
    fp.write("# GEOLYSIS Microsoft Excel Functions\n\n")
    # for func in functions_metadata:
    #     func_name = func["name"]
    #     fp.write(f"- [{func_name}]({func_name.lower().replace('_', '-')}.md)\n\n")


def generate_excel_func_pages():
    try:
        functions_metadata = _get_function_metadata().get("functions", [])
    except Exception as ex:
        print(str(ex))
        raise Exception("Failed to get function metadata")

    for function_metadata in functions_metadata:
        func_name = function_metadata["name"]
        func_desc = function_metadata["description"]
        mod_filename = func_name.lower().replace("_", "-")
        filename = f"excel/functions/{mod_filename}.md"

        func_params = function_metadata["parameters"]
        func_params_names = ", ".join(
            [
                f"[{param['name']}]" if param.get("optional") else param[
                    "name"]
                for param in func_params
            ]
        )

        with (
            mkdocs_gen_files.open(filename, "w") as fp,
            mkdocs_gen_files.open(excel_functions_index_page, "a") as idx_file,
        ):
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

            idx_file.write(
                f"- [{func_name}]({mod_filename}.md): {func_desc}\n")


generate_excel_func_pages()
