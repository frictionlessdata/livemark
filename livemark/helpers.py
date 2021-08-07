import io
import os
import sys
import shutil
import tempfile
import contextlib
from urllib.parse import urlparse
from _thread import RLock  # type: ignore
from . import settings


# General


def list_setdefault(list, index, default):
    if len(list) == index:
        list.append(default)
    return list[index]


def read_file(source, *, default=None):
    if default and not os.path.isfile(source):
        return default
    with open(source, encoding="utf-8") as file:
        return file.read()


def move_file(source, target):
    ensure_dir(target)
    shutil.move(source, target)


def copy_file(source, target):
    if isinstance(source, (tuple, list)):
        source = os.path.join(*source)
    if isinstance(target, (tuple, list)):
        target = os.path.join(*target)
    ensure_dir(target)
    shutil.copy(source, target)


def write_file(path, text=""):
    with tempfile.NamedTemporaryFile("wt", delete=False, encoding="utf-8") as file:
        file.write(text)
        file.flush()
    move_file(file.name, path)


def write_stdout(text):
    sys.stdout.write(text)
    sys.stdout.write("\n")
    sys.stdout.flush()


def ensure_dir(path):
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)


def is_remote_path(path):
    path = path[0] if path and isinstance(path, list) else path
    scheme = urlparse(path).scheme
    if not scheme:
        return False
    if path.lower().startswith(f"{scheme}:\\"):
        return False
    return True


@contextlib.contextmanager
def capture_stdout(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


# Backports


class cached_property:
    # It can be removed after dropping support for Python 3.6 and Python 3.7

    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__
        self.lock = RLock()

    def __set_name__(self, owner, name):
        if self.attrname is None:
            self.attrname = name
        elif name != self.attrname:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                f"({self.attrname!r} and {name!r})."
            )

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.attrname is None:
            raise TypeError(
                "Cannot use cached_property instance without calling __set_name__ on it."
            )
        try:
            cache = instance.__dict__
        except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to cache {self.attrname!r} property."
            )
            raise TypeError(msg) from None
        val = cache.get(self.attrname, settings.UNDEFINED)
        if val is settings.UNDEFINED:
            with self.lock:
                # check if another thread filled cache while we awaited lock
                val = cache.get(self.attrname, settings.UNDEFINED)
                if val is settings.UNDEFINED:
                    val = self.func(instance)
                    try:
                        cache[self.attrname] = val
                    except TypeError:
                        msg = (
                            f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                            f"does not support item assignment for caching {self.attrname!r} property."
                        )
                        raise TypeError(msg) from None
        return val
