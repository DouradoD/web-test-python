from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import walk_packages

PAGE_FOCUS_METHOD = 'is_on_focus'


class PageStructureException(Exception):
    """ Exception raised when errors are found on a page declaration.

    """


class PageNotFoundException(Exception):
    """ Exception raised when the destination page of an action method was not reached within a timeout.

    """


def mapping_wrapper(name):
    def cls_modifier(cls):
        """
            Injecting page identification data, e.g: name, environment, is_component, ...
            if the page not contains is_on_focus, raise error, but the page is not a component!
        """
        # Injecting page identification data
        cls.mapping_name = name
        return cls

    return cls_modifier


def page_wrapper(name):
    def cls_modifier(cls):
        """
            Injecting page identification data, e.g: name, environment, is_component, ...
            if the page not contains is_on_focus, raise error, but the page is not a component!
        """
        # Injecting page identification data
        cls.page_name = name
        return cls

    return cls_modifier


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def _filter(members):
    dict_ = {}
    for m in members:
        name = getattr(m, 'page_name', None) or getattr(m, 'mapping_name')
        if name not in dict_:
            dict_[name] = m
    return dict_


@singleton
class Pages:

    def __init__(self, **injection_objects):
        self._pages = []
        self.load_pages(**injection_objects)

    def load_pages(self, **injection_objects):
        pages = []
        mappings = []
        package = import_module('tests')
        folders = walk_packages(path=package.__path__, prefix=f'{package.__name__}.')
        for module_info in folders:
            # Checking if the module is non-leaf
            if not module_info.ispkg:
                module = import_module(module_info.name)  # Retrieve the module namespace

                # Check if the module has class implementations and if they are not from other scope
                for _, member in getmembers(module, lambda m: (isclass(m) and m.__module__ == module_info.name)
                                                              and (hasattr(m, 'page_name')
                                                                   or hasattr(m, 'mapping_name'))):
                    if hasattr(member, 'page_name'):
                        pages.append(member)
                    if hasattr(member, 'mapping_name'):
                        mappings.append(member)
        pages = _filter(pages)
        mappings = _filter(mappings)
        for page_name, page_cls in pages.items():
            page = page_cls()  # Instantiating the page

            for obj_name, obj in injection_objects.items():
                setattr(page, obj_name, obj)

            # Injecting mappings on pages
            mapping_cls = mappings.get(page_name)
            if mapping_cls:
                mapping = mapping_cls()
                setattr(page, 'mapping', mapping)
            setattr(self, page_name, page)  # Injecting the modified page
            self._pages.append(page)
        return self._pages
