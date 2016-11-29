#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.8.6
# In conjunction with Tcl version 8.6
#    Nov 26, 2016 10:09:34 PM
import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

from . import risks_support
# import risks_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = Risks (root)
    risks_support.init(root, top)
    root.mainloop()

w = None
def create_Risks(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = Risks (w)
    risks_support.init(w, top, *args, **kwargs)
    top.render_choices()

    return (w, top)

def destroy_Risks():
    global w
    w.destroy()
    w = None


class Risks:
    model = None
    callback = None

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        self._bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        self._fgcolor = '#000000'  # X11 color: 'black'
        self._compcolor = '#d9d9d9' # X11 color: 'gray85'
        self._ana1color = '#d9d9d9' # X11 color: 'gray85'
        self._ana2color = '#d9d9d9' # X11 color: 'gray85'

        top.geometry("600x366+355+130")
        top.title("Risks")

        self.Labelframe1 = LabelFrame(top)
        self.Labelframe1.place(relx=0.02, rely=0.03, relheight=0.86
                , relwidth=0.97)
        self.Labelframe1.configure(relief=GROOVE)
        self.Labelframe1.configure(text='''Risks''')
        self.Labelframe1.configure(width=580)

        self.Frame1 = Frame(self.Labelframe1)
        self.Frame1.place(relx=0.02, rely=0.06, relheight=0.9, relwidth=0.96)
        self.Frame1.configure(relief=SUNKEN)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=SUNKEN)
        self.Frame1.configure(width=555)

        self.btn_quit = Button(top)
        self.btn_quit.place(relx=0.83, rely=0.9, height=26, width=87)
        self.btn_quit.configure(activebackground="#d9d9d9")
        self.btn_quit.configure(command=risks_support.cmd_quit)
        self.btn_quit.configure(text='''Quit''')
        self.btn_quit.configure(width=87)

    def render_choices(self):
        master = self.Frame1

        durations = [act.duration_model for act in self.model.nodes]
        index=0
        for duration in durations:
            for element in duration.elements:
                for node in element.nodes:
                    if node.can_pre_choice():
                        self.create_choice_ui(master, node, index)
                        index+=1



    def create_choice_ui(self, master, nodeCpd, index):
        lb = Label(master,text=nodeCpd.name)
        # lb.configure(width=100)
        lb.grid(row=index, column=0)
        lb.configure(anchor='e')

        labels = [l for l in nodeCpd.labels]
        labels.append('manual')

        combobox = ttk.Combobox(master)
        combobox.grid(row=index, column=1)
        combobox.configure(values=labels)
        # combobox.configure(width=220)
        combobox.bind("<<ComboboxSelected>>",
                      lambda event: risks_support.on_choice(nodeCpd, combobox))
        if nodeCpd.choice_index == nodeCpd.MANUAL:
            combobox.set('manual')
        else:
            combobox.set(nodeCpd.labels[nodeCpd.choice_index])


if __name__ == '__main__':
    vp_start_gui()
