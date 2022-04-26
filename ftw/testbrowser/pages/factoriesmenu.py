from ftw.testbrowser import browser as default_browser


def menu(browser=default_browser):
    """Returns the factories menu container node or ``None`` if it is
    not visible.
    """
    nodes = browser.css('#plone-contentmenu-factories')

    # plone 6  - remove svg icon from menu
    for svg_element in browser.css('#collapse-plone-contentmenu-factories > ul svg'):
        svg_element.node.drop_tree()

    if len(nodes) == 0:
        return None
    else:
        return nodes.first


def visible(browser=default_browser):
    """Returns ``True`` when the factories menu is visible on the current page.
    """
    if menu(browser=browser) is not None:
        return True
    else:
        return False


def add(type_name, browser=default_browser):
    """Clicks on the add-link in the factories menu for the passed type name.
    The type name is the literal link label.
    This opens the add form for this type.

    :param type_name: The name (label) of the type to add.
    :type type_name: string
    """
    if not visible(browser=browser):
        raise ValueError('Cannot add "%s": no factories menu visible.' % (
            type_name))

    # Plone 4: .actionMenuContent
    # Plone 5: >ul
    # Plone 6: #collapse-plone-contentmenu-factories > ul
    selector = '.actionMenuContent, >ul, #collapse-plone-contentmenu-factories > ul'

    links = menu(browser=browser).css(selector).find(type_name)
    if len(links) == 0:
        raise ValueError('The type "%s" is not addable. Addable types: %s' % (
            type_name,
            ', '.join(addable_types(browser=browser))))

    links.first.click()


def addable_types(browser=default_browser):
    """Returns a list of addable types. Each addable types is the link label
    in the factories menu.
    """

    if not visible(browser=browser):
        raise ValueError('Factories menu is not visible.')

    # Plone 4: .actionMenuContent
    # Plone 5: >ul
    # Plone 6: #collapse-plone-contentmenu-factories > ul
    selector = '.actionMenuContent a, >ul a, #collapse-plone-contentmenu-factories > ul a'
    return menu(browser=browser).css(selector).text
