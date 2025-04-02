"""Define operations related to jinga2 templating ."""

from jinja2 import FileSystemLoader, Environment


def render_template(template, *args, **kwargs):
    """
    This method accepts the same arguments as the `dict` constructor:
    A dict, a dict subclass or some keyword arguments.  If no arguments
    are given the context will be empty.  These two calls do the same::

            template.render(knights='that say nih')
            template.render({'knights': 'that say nih'})

    This will return the rendered template as unicode string.
    :param template: sql template direction
    """
    template_loader = FileSystemLoader(searchpath=get_search_path())
    template_env = Environment(loader=template_loader, autoescape=True)
    t = template_env.get_template(template)
    return t.render(*args, **kwargs)


def get_search_path():
    """
    Get the search path of the jinga2 templates

    :return: dict
    """
    return {
            'include/template/',
            '/include/template/',
            './include/template/',
            "../include/template/",
            "../../include/template/"
            "../../../include/template/"
            "../../../../include/template/"
            "../../../../../include/template/"
            "../../../../../../include/template/"
            "../../../../../../../include/template/"
        }
