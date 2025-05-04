import re
from docutils import nodes, utils


# from docutils.parsers.rst.roles import set_classes


def pyver_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Link to a python version."""
    semver_rgx = re.compile(r'^'
                            r'(3)'  # major
                            r'(?:\.(0|[1-9]\d*))?'  # optional minor
                            r'(?:\.(0|[1-9]\d*))?'  # optional patch
                            r'$'
                            )
    mtch = semver_rgx.match(text)

    if mtch:
        pyver = mtch.group(0)
    else:
        msg = inliner.reporter.error(f"Invalid python version: {text:r}",
                                     line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    app = inliner.document.settings.env.app
    node = make_link_node(rawtext, app, pyver, options)
    return [node], []


def make_link_node(rawtext, app, slug, options):
    try:
        py_docs_url = app.config.python_docs_url
        if not py_docs_url:
            raise AttributeError
    except AttributeError:
        raise ValueError("python_docs_url not set")

    refuri = py_docs_url + '/' + f"{slug}.html"
    node = nodes.reference(rawtext, utils.unescape(slug),
                           refuri=refuri, classes=["external-link"], **options)
    return node


def setup(app):
    app.add_role('pyver', pyver_role)
    app.add_config_value('python_docs_url', None, 'env')
    return
