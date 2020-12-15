from enum import Enum
from abc import ABC, abstractmethod
from collections import ChainMap
from importlib import import_module

class OptionType(Enum):
    BUTTON = 1


# To hold metadata regarding the option, inputs, etc.
class Option(ABC):
    BUTTON = OptionType.BUTTON

    # Builds dict from list of options
    @staticmethod
    def build_dict(options):
        return {option.__name__:option for option in options}
    @abstractmethod
    def __call__(self, *args, **kwargs):
        return self.__fun__(*args, **kwargs)
    @abstractmethod
    def __str__(self):
        return super().__str__()
    def __init__(self, name, fun, t=OptionType.BUTTON):
        self.__name__ = name
        self.__fun__ = fun
        self.__type__ = t

# Simple option to use, runs function given in the constructor.
class SimpleOption(Option):
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)
    def __str__(self):
        return super().__str__()

def fun_2_option(d, o=SimpleOption):
    return {k:o(k, v) for k,v in d.items()}



def get_options(*args, o=SimpleOption, **kwargs):
    print(f'args={args}', f'kwargs={kwargs}')
    # Dyanmically import modules from args
    modules = [import_module(arg).__functions__ for arg in args]
    # Expose function names and package into list of dictionaries
    options = [{fun.__name__:fun for fun in item} for item in modules]
    # Combine into single dicitonary
    options = ChainMap(*options)
    # Now convert function name : function pairs to option name: options pairs
    # Note, [o] is the class of option, SimpleOption by default.
    # We also combien this with the step of combining it with the kwargs.
    options = ChainMap(fun_2_option(kwargs, o=o), fun_2_option(options, o=o))
    return options
