from tkinter import *
from gui.mainapp import *
from gui import utils


def main():
    root = Tk()
    utils.load_icon()
    app = MainApplication(root, 'Bayesian Network')
    root.mainloop()

if __name__ == '__main__':
    main()
