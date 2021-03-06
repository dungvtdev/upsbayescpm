#! /usr/bin/env python
#
# Support module generated by PAGE version 4.8.6
# In conjunction with Tcl version 8.6
#    Nov 26, 2016 10:10:24 PM


import sys
from .model import NodeCpdModel

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


def cmd_quit():
    print('risks_support.cmd_quit')
    sys.stdout.flush()
    w.callback()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

    if kwargs:
        w.model = kwargs['model']
        w.callback = kwargs['callback']

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


def on_choice(nodeCpd, combobox):
    select_str = combobox.get()
    index = next((i for i in range(len(nodeCpd.labels)) if nodeCpd.labels[i]==select_str),-1)
    index = NodeCpdModel.MANUAL if index == -1 else index
    nodeCpd.choice_index = index

def on_choice_value(event, node, entry):
    # print('Choice_value %s' %event.__dict__)
    try:
        entry_str = entry.get()
        if not entry_str:
            value = node.try_set_choice(None)
        else:
            # print('Entry str %s' % entry_str)
            value = float(entry_str)
            value = node.try_set_choice(value)
            # if event.keycode == 36:
        entry.delete(0,'end')
        entry.insert(0,str(value))
    except Exception as e:
        pass

if __name__ == '__main__':
    import risks
    risks.vp_start_gui()
