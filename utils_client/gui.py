from tkinter import Tk, Frame, Button, Text, END
from collections import ChainMap
from option import get_options, recalculate_hierarchy, OptionType

class GUI(Frame):
    """
    Container for the buttons that will be returned by [get_gui].
    [*args] are paths to modules to load functions from.
    [**kwargs] are specific functions with button names as keys, and functions
    as values to load.
    """

    def __init__(self, *args, frame=None, **kwargs):
        """
        [*args] are paths to modules to load functions from.
        [**kwargs] are specific functions with button names as keys, and functions
        as values to load.
        """
        super().__init__(frame)
        self.frame = frame
        self.load_options(*args, **kwargs)
        self.pack()
        self.create_widgets()

    def load_options(self, *args, **kwargs):
        """
        Calls [option.get_options(*args, **kwargs)] and sets the self.options
        attribute to the result. It then calculates the hierarchies.
        """
        self.options = get_options(*args, **kwargs)
        print(recalculate_hierarchy(self.options))

    def create_widgets(self):
        """
        Initializes the buttons and inputs according to self.options.
        """
        for name, option in self.options.items():
            if option.type == OptionType.BUTTON:
                button = Button(self)
                button['text'] = name
                # Messy, refactor
                print(name, option.fun.__name__, option.name)
                print('\n\n\n')
                button['command'] = lambda: option(self)
                button.pack()
                setattr(self, f'{name}_button', button)
            # elif option.type == OptionType.TEXTINPUT:
                # text_input = Text(self)
                # text_input.insert(END, '')
                # text_input.pack()
                # setattr(self, f'{name}_input', text_input)
            else:
                print(f'Unexpected option: {option.name} of type {option.type}')

        # for name, option in self.options.items():
        #     print(name, option.type, option.fun)
        #     if option.type == OptionType.BUTTON:
        #         comp = getattr(self, f'{name}_button')['command']
        #         print(comp.option.name, comp.option.type, comp.option.fun)
        #     # elif option.type == OptionType.TEXTINPUT:
        #     #     comp = getattr(self, f'{name}_input')
        #     #     print(comp.option.name, comp.option.type, comp.option.fun)
        #     print('\n\n\n\n')
        print(dir(self))

    # Not sure if I will use this
    def execute_option(self, option, *args, **kwargs):
        # Doubly link the parent/child, and order them
        self.options[option](*args, **kwargs)

def get_app(*args, **kwargs):
    """
    Returns an instance of Tk, initializing the GUI given [*args] and [**kwargs].
    """
    root = Tk()
    gui = GUI(*args, frame = root, **kwargs)
    return root
