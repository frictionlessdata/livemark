import os
import shutil
import tempfile


def ensure_dir(path):
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)


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


def write_file(path, text):
    with tempfile.NamedTemporaryFile("wt", delete=False, encoding="utf-8") as file:
        file.write(text)
        file.flush()
    move_file(file.name, path)
