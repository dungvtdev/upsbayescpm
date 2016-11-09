from tkinter import *
from gui.mainapp import *
from gui import utils
from mybayes import *
from mybayes.cache import Cache


def main():
    set_cache(Cache())

    root = Tk()
    utils.load_icon()
    app = MainApplication(root, 'Bayesian Network')
    root.mainloop()

if __name__ == '__main__':
    main()
