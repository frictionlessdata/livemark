from livemark import Markup


# General


def test_markup():
    input = "<html></html>"
    markup = Markup(input)
    assert markup.input == input
    assert markup.output == input
