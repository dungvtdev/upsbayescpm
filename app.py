from tkinter import *
import tkinter.messagebox
from gui.tkinter_tab import *

PROGRAM_NAME = "Bayesian Network"

root = Tk()
root.geometry('350x350')
root.title(PROGRAM_NAME)

""" Define constants"""
NODE_CONSTANT = 0

"""Load icon image"""
new_file_icon = PhotoImage(file='gui/icons/new_file.gif')
open_file_icon = PhotoImage(file='gui/icons/open_file.gif')
save_file_icon = PhotoImage(file='gui/icons/save.gif')
cut_icon = PhotoImage(file='gui/icons/cut.gif')
copy_icon = PhotoImage(file='gui/icons/copy.gif')
paste_icon = PhotoImage(file='gui/icons/paste.gif')
undo_icon = PhotoImage(file='gui/icons/undo.gif')
redo_icon = PhotoImage(file='gui/icons/redo.gif')

"""Define commands"""


def new_file(event=None):
    pass


def open_file(event=None):
    pass


def save_file(event=None):
    pass


def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
        root.destroy()


def new_template(event=None):
    pass


def new_prototype(event=None):
    pass


def new_node(node_type=None):
    def command(event=None):
        print('Create node %d' % node_type)

    return command


def run(event=None):
    pass


""" Create menu"""
menu_bar = Menu(root)

""" File menu"""
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left',
                      image=new_file_icon, underline=0, command=new_file)
file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left',
                      image=open_file_icon, underline=0, command=open_file)
file_menu.add_command(label='Save', accelerator='Ctrl+S',
                      compound='left', image=save_file_icon, underline=0, command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt+F4', command=exit_editor)
menu_bar.add_cascade(label='File', menu=file_menu)

""" Nodes menu"""
nodes_menu = Menu(menu_bar, tearoff=0)
dist_menu = Menu(menu_bar, tearoff=0)
calc_menu = Menu(menu_bar, tearoff=0)

nodes_menu.add_command(label='Template', compound='left', underline=0, command=new_template)
nodes_menu.add_command(label='Prototype', compound='left', underline=0, command=new_prototype)
nodes_menu.add_separator()
nodes_menu.add_cascade(label='Distribution', menu=dist_menu)
nodes_menu.add_cascade(label='Calc', menu=calc_menu)
nodes_menu.add_separator()
nodes_menu.add_command(label='Constant', compound='left', underline=0, command=new_node(NODE_CONSTANT))

menu_bar.add_cascade(label='Nodes', menu=nodes_menu)

""" Run menu """
run_menu = Menu(menu_bar, tearoff=0)
run_menu.add_command(label='Run', compound='left', underline=0, command=run)

menu_bar.add_cascade(label='Run', menu=run_menu)

root.config(menu=menu_bar)

""" Create Utils Panel"""
util_panel = TabBar(root, "Nodes")  # .grid(row=0, column=0, sticky='N'+'S')

""" Node tab """
nodes_tab = Tab(root, "Nodes")
nodes_lb = Listbox(nodes_tab)
nodes_lb.insert(1, "Python")
nodes_lb.insert(2, "Perl")
nodes_lb.insert(3, "C")
nodes_lb.insert(4, "PHP")
nodes_lb.pack(side=TOP, fill=Y)

""" Template tab """
temps_tab = Tab(root, "Templates")
temp_lb = Listbox(temps_tab)
temp_lb.insert(1, "fas")
temp_lb.insert(2, "Perasdl")
temp_lb.insert(3, "asdf")
temp_lb.pack(side=TOP, fill=Y)

util_panel.add(nodes_tab)
util_panel.add(temps_tab)
util_panel.show()

root.mainloop()
