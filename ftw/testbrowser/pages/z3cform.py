from ftw.testbrowser import browser as default_browser
from ftw.testbrowser.utils import normalize_spaces


def erroneous_fields(form, browser=default_browser):
    """Returns a mapping of erroneous fields (key is label or name of
    the field) to a list of error messages for the fields on the form
    passed as argument.

    :param form: The form node to check for errors.
    :type form: :py:class:`ftw.testbrowser.form.Form`
    :param browser: A browser instance. (Default: global browser)
    :type browser: :py:class:`ftw.testbrowser.core.Browser`
    :returns: A dict of erroneous fields with error messages.
    :rtype: dict
    """

    result = {}
    for input in form.inputs:
        if not input.parent('.field.error'):
            continue

        label = None
        if input.label is not None:
            label = input.label.text_content()
        if not label:
            label = input.name

        errors = input.parent('.field').css('.fieldErrorBox').normalized_text()
        result[normalize_spaces(label)] = errors
    return result
