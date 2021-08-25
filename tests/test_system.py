import pytest
from livemark import system, Plugin, LivemarkException


# General


def test_system():
    assert len(system.Plugins) > 20


def test_system_register():
    system.register(Plugin)
    assert system.Plugins[""]
    system.deregister(Plugin)


def test_system_deregister_not_registered():
    with pytest.raises(LivemarkException) as excinfo:
        system.deregister(Plugin)
    assert str(excinfo.value).count("Not registered plugin")
