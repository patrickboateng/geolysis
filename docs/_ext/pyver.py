import re
from docutils import nodes, utils


def pyver_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Link to a python version."""
    semver_rgx = re.compile(r'^'
                            r'(3)'  # major
                            r'(?:\.(0|[1-9]\d*))?'  # optional minor
                            r'(?:\.(0|[1-9]\d*))?'  # optional patch
                            r'$'
                            )
    mtch = semver_rgx.match(text)

    if not mtch:
        msg = inliner.reporter.error(f"Invalid python version: {text!r}",
                                     line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    pyver = mtch.group(0)
    pyver_docs_page = "https://docs.python.org/3/whatsnew"
    refuri = f"{pyver_docs_page}/{pyver}.html"
    node = nodes.reference(rawtext,
                           utils.unescape(pyver),
                           refuri=refuri,
                           classes=["external-link"],
                           **options)
    return [node], []


def setup(app):
    app.add_role('pyver', pyver_role)
    # app.add_config_value('python_docs_url', None, 'env')
