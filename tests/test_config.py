from livemark import Config


# General


def test_config():
    config = Config({"a": [1, 2]})
    config.merge({"a": [3, 4]})
    assert config["a"] == [1, 2, 3, 4]
