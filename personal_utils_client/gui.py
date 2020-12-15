from tkinter import Tk, Frame, Button
from collections import ChainMap
from action import get_options, Option
class GUI(Frame):
    def __init__(self, *args, frame=None, **kwargs):
        super().__init__(frame)
        self.frame = frame
        self.load_options(*args, **kwargs)
        self.pack()
        self.create_widgets()
    def load_options(self, *args, **kwargs):
        self.options = get_options(*args, **kwargs)
    def create_widgets(self):
        print(f'Creating widgets from {self.options}')
        for name, option in self.options.items():
            if option.__type__ == Option.BUTTON:
                button = Button(self)
                button['text'] = name
                button['command'] = option
                button.pack()
                setattr(self, f'{name}_button', button)
            else:
                print(f'This is something else: {option.__name__} of type {option.__type__}')
    def execute_option(self, option, *args, **kwargs):
        self.options[option](*args, **kwargs)
def get_app(*args, **kwargs):
    root = Tk()
    gui = GUI(*args, frame = root, **kwargs)
    return root
