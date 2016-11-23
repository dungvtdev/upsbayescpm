from tkinter import *
from gui.mainapp import *
from gui.utils import utils
from mybayes import *
from mybayes.cache import Cache

from gui.duration.wd_duration import *

def main():
    set_cache(Cache())

    root = Tk()
    utils.load_icon()
    app = MainApplication(root, 'Bayesian Network')
    root.mainloop()

if __name__ == '__main__':
    main()
    # test
    # root = Tk()
    # root.config()
    # app = WdDuration(root, None)
    # root.mainloop()
