import io
import os
import sys
import shutil
import tempfile
import importlib
import contextlib
from pathlib import Path
from urllib.parse import urlparse


# General


def path_asset(*paths):
    return os.path.join(os.path.dirname(__file__), "assets", *paths)


def read_asset(*paths):
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "assets", *paths)) as file:
        return file.read().strip()


def get_relpath(path, current):
    return os.path.relpath(path, os.path.dirname(current))


def with_format(path, format):
    suffix = f".{format}" if format else ""
    return Path(path).with_suffix(suffix).as_posix()


def list_setdefault(list, index, default):
    if len(list) == index:
        list.append(default)
    return list[index]


def read_file(source, *, default=None):
    if default and not os.path.isfile(source):
        return default
    with open(source, encoding="utf-8") as file:
        return file.read()


def copy_file(source, target):
    if isinstance(source, (tuple, list)):
        source = os.path.join(*source)
    if isinstance(target, (tuple, list)):
        target = os.path.join(*target)
    ensure_dir(target)
    shutil.copy(source, target)


def move_file(source, target):
    ensure_dir(target)
    shutil.move(source, target)


def remove_dir(path):
    shutil.rmtree(path, ignore_errors=True)


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


def flatten_items(items, prop):
    flatten_items = []
    for item in items:
        subitems = item.get(prop, [])
        for subitem in subitems:
            flatten_items.append(subitem)
        if not subitems:
            flatten_items.append(item)
    return flatten_items


def extract_classes(module, Parent):
    Classes = []
    for item in vars(module or {}).values():
        if isinstance(item, type) and issubclass(item, Parent) and item is not Parent:
            Classes.append(item)
    return Classes


def unique_objects(objects, property):
    result = []
    values = []
    for object in objects:
        value = getattr(object, property)
        if value not in values:
            result.append(object)
            values.append(value)
    return result


def load_object(path):
    try:
        path, name = path.rsplit(".", 1)
        module = importlib.import_module(path)
        return getattr(module, name)
    except Exception:
        return None


def order_objects(objects, property):
    return list(sorted(objects, key=lambda obj: -getattr(obj, property)))
