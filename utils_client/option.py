"""
DISAMBIGUATION: This has no relation with the functional programming concept of
"Options" or anything of that nature.
"""

from tkinter import END
from enum import Enum, IntEnum
from collections import ChainMap
from importlib import import_module
class OptionType(Enum):
    BUTTON = 1
    TEXTINPUT = 2

# To hold metadata regarding the option, inputs, etc.
class Option():
    """
    Holds metadata to be used by the GUI, such as the name, function, number of
    arguments, type, parent option, and ordering.
    """
    def __call__(self, gui, *args, **kwargs):
        args = list(args)
        # Acquire values from children
        # for child in self.children:
        #     args.append(gui.masterlist[child]())
        # print(f'passing {self.name}')
        args.append(0)
        return self.fun(*args, **kwargs)
    def __init__(self, name, fun, argsn = None, t=OptionType.BUTTON, parent = None, ordering=[]):
        self.name = name
        self.fun = fun
        self.argsn = argsn
        self.type = t
        self.parent = parent
        self.children = []
        self.ordering = ordering
        self._validated = False
        self.quirk = Quirk.NONE
    def __str__(self):
        tab = ' '*4
        return (
            f'Option: {self.name}\n'
            f'{tab}function: {self.fun.__name__}\n'
            f'{tab}argument count: {self.argsn}\n'
            f'{tab}option type: {self.type}\n'
            f'{tab}parent: {self.parent}\n'
            f'{tab}ordering: {self.ordering}\n'
        )
    def __repr__(self):
        return (
            f'[Option] name={self.name}, fun={self.fun.__name__}, '
            f'argsn={self.argsn}, t={self.type}, parent={self.parent}, '
            f'ordering={self.ordering}'
        )
def input_(text_input, line=1, column=0):
    """
    Returns content of line 1 in the input.
    """
    return text_input.get(f'{line}.{column}', END)

def Input(name, fun=input_, argsn = None, t=OptionType.TEXTINPUT, parent = None, ordering=[]):
    """
    Functionally equivelant to Option(..., fun=input_, t=OptionType.TEXTINPUT, ...)
    """
    return Option(name, fun, argsn, t, parent, ordering)

def get_options(*args, **kwargs):
    print(f'args={args}', f'kwargs={kwargs}')
    # Dyanmically import modules from args
    modules = [import_module(arg).__options__ for arg in args]
    options = ChainMap(*modules, kwargs)
    return options

class Quirk(IntEnum):
    NONE = 0
    TOO_FEW_ARGS = 1
    TOO_MANY_ARGS = 2

def recalculate_hierarchy(options):
    """
    Caluclates children based off of arguments/parents, and notes inconsistencies
    in the option's quirks.
    """
    # Remove any preexisting downstream hierarchies
    for optionid, option in options.items():
        option.children = []
        option.quirk = Quirk.NONE
    # Build downstream hierarchies
    for optionid, option in options.items():
        if option.parent:
            options[option.parent].children.append(optionid)
    # Validation step: check to see if arguments match up
    invalid_options = set()
    for optionid, option in options.items():
        valid = True
        if option.argsn != None:
            if len(option.children)<option.argsn:
                valid = False
                option.quirk |= Quirk.TOO_FEW_ARGS
            if len(option.children)>option.argsn:
                option.quirk |= Quirk.TOO_MANY_ARGS
            if not valid:
                invalid_options.add(optionid)
    return invalid_options
