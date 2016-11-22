import tkinter as tk

class ToggleGroup(object):

    def __init__(self, *argv):
        self.buttons = []
        self.actions = []
        self.index = 0
        self.add(*argv)
        if argv:
            self.click(0)

    def add(self, *argv):
        if not argv:
            return

        for a in argv:
            if a not in self.buttons:
                self.buttons.append(a)

    def click(self, index):
        self.index = index
        # index = next((x for x in self.buttons if x == button), None)
        # if not index:
        #     return
        # format lai button
        for b in self.buttons:
            b.config(relief=tk.RAISED)
        self.buttons[index].config(relief=tk.SUNKEN)

        for a in self.actions:
            a(index)

    def add_listener(self, action):
        self.actions.append(action)

    def set_default(self, index):
        self.click(self.index)
