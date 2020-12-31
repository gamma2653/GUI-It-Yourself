from gui import get_app
import argparse
from collections import ChainMap



def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    # add arguments here
    parser.add_argument('-m', '--modules', default=[], nargs='*')
    args = parser.parse_args()




    def_modules = ['default_options.options']
    # def_modules = Option.build_dict([SimpleOption('example', lambda: print)])

    # Create the gui, pass arguments so it can construct buttons
    gui = get_app(*(args.modules+def_modules))

    # Run it.
    gui.mainloop()


if __name__ == '__main__':
    main()
