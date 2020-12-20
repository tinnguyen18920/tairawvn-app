from os.path import dirname, basename, isfile, join
import glob

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
# print(BASE_DIR)
# print("baseDIR")
# print(glob.glob(str(BASE_DIR / "*")))
modules = glob.glob(join(dirname(__file__), "*.py"))
# print(modules)
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

# __all__ = ["bilibili"]
# RAWS = ["bilibili"]
# from importlib import import_module

# for raw in RAWS:
#     import_module("raws.{}".format(raw))
