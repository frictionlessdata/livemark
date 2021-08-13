import pytest
from livemark import Markup, LivemarkException


# General


def test_markup():
    input = "<html></html>"
    markup = Markup(input)
    assert markup.input == input
    assert markup.output == input
    assert markup.query.outer_html() == input


# Bind


def test_markup_get_plugin_not_bound():
    input = "<html></html>"
    markup = Markup(input)
    with pytest.raises(LivemarkException) as excinfo:
        markup.get_plugin()
    assert str(excinfo.value).count("Markup is not bound")
