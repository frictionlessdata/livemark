from livemark import Config


# General


def test_config():
    config1 = Config({"a": [1, 2]})
    config2 = config1.merge({"a": [3, 4]})
    assert config1["a"] == [1, 2]
    assert config2["a"] == [1, 2, 3, 4]
