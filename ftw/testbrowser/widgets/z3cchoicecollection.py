from ftw.testbrowser.exceptions import OptionsNotFound
from ftw.testbrowser.widgets.base import PloneWidget
from ftw.testbrowser.widgets.base import widget
from lxml import etree


@widget
class Z3cChoiceCollection(PloneWidget):
    """Represents the default z3cform Choice Collection widget.
    This widget is used when having a ``schema.List`` field with
    the value_type of a ``schema.Choice``.
    It works like an in-and-out widget.
    """

    @staticmethod
    def match(node):
        if not PloneWidget.match(node):
            return False

        return len(node.css('table.ordered-selection-field')) > 0


    def fill(self, values):
        """Fill the widget with the values in this order.
        Values may be key or labels.

        :param values: value to fill the field with.
        :type values: string or list of strings
        """
        values = list(self._normalize_values(values))

        # move all options form "to" to "from"
        for option_node in self._to_select.css('option'):
            self._from_select.append(option_node.node)

        # move selected options from "from" to "to" in order
        for value in values:
            option_node = self._from_select.css(
                'option[value={0}]'.format(value)).first
            self._to_select.append(option_node.node)

        # select the options (adding selected="selected")
        self._to_select.value = values

    def _normalize_values(self, values):
        if not isinstance(values, (list, tuple)):
            values = [values]

        labels_to_values = dict(zip(*reversed(zip(*self.options))))
        available_values = self.options_values
        not_found = []

        for value in values:
            if value in available_values:
                yield value
            elif value in labels_to_values:
                yield labels_to_values[value]
            else:
                not_found.append(value)

        if not_found:
            raise OptionsNotFound(self.label.text, not_found)

    @property
    def options(self):
        """Returns a list of value/label pairs of all available options
        of this field.

        :returns: list of tuples, each a value/label per of an option
        :rtype: list of tuples
        """
        return self.unselected + self.selected

    @property
    def options_labels(self):
        """Returns a list of labels of available options.

        :returns: list of labels
        :rtype: list of strings
        """
        return self.unselected_labels + self.selected_labels

    @property
    def options_values(self):
        """Returns a list of values of available options.

        :returns: list of values
        :rtype: list of strings
        """
        return self.unselected_values + self.selected_values

    @property
    def selected(self):
        """Returns a list of value/label pairs of all selected options
        of this field.

        :returns: list of tuples, each a value/label per of an option
        :rtype: list of tuples
        """
        return self._to_select.options

    @property
    def selected_labels(self):
        """Returns a list of labels of selected options.

        :returns: list of labels
        :rtype: list of strings
        """
        return self._to_select.options_labels

    @property
    def selected_values(self):
        """Returns a list of values of selected options.

        :returns: list of values
        :rtype: list of strings
        """
        return self._to_select.options_values

    @property
    def unselected(self):
        """Returns a list of value/label pairs of all unselected options
        of this field.

        :returns: list of tuples, each a value/label per of an option
        :rtype: list of tuples
        """
        return self._from_select.options

    @property
    def unselected_labels(self):
        """Returns a list of labels of unselected options.

        :returns: list of labels
        :rtype: list of strings
        """
        return self._from_select.options_labels

    @property
    def unselected_values(self):
        """Returns a list of values of unselected options.

        :returns: list of values
        :rtype: list of strings
        """
        return self._from_select.options_values

    @property
    def _from_select(self):
        return self.xpath(
            './/select[substring(@id, string-length(@id) - 4) = "-from"]').first

    @property
    def _to_select(self):
        return self.xpath(
            './/select[substring(@id, string-length(@id) - 2) = "-to"]').first