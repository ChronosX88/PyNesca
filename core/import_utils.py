import importlib
from glob import glob
from os import extsep
from os.path import realpath, dirname, join, basename, splitext
import sys
from inspect import getmembers, isfunction, isclass


def module_paths_list(path):
    return glob(join(path, "*" + extsep + "py"))


def modulename(file_path):
    return splitext(basename(file_path))[0]


def module_name_list(path):
    return [modulename(module_path) for module_path in
    module_paths_list(path)]


def import_module(path):
    if dirname(path) not in sys.path:
        sys.path.insert(0, dirname(path))
    name = modulename(path)
    module_spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def import_class(path):
    return getattr(import_module(path), modulename(path))


def import_matching(path, matcher_function):
    matching = []
    for modulefile in module_paths_list(path):
        module = import_module(modulefile)
        for name, value in getmembers(module):
            if matcher_function(name, value):
                matching.append(value)
    return matching


def import_functions(path):
    def matcher(name, value):
        return isfunction(value)
    return import_matching(path, matcher)


def import_classes(path):
    def matcher(name, value):
        return isclass(value)
    return import_matching(path, matcher)
