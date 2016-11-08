from tkinter import *

"""Load icon image"""

icon = None


def load_icon():
    class Icon(object):
        new_file_icon = PhotoImage(file='gui/icons/new_file.gif')
        open_file_icon = PhotoImage(file='gui/icons/open_file.gif')
        save_file_icon = PhotoImage(file='gui/icons/save.gif')
        cut_icon = PhotoImage(file='gui/icons/cut.gif')
        copy_icon = PhotoImage(file='gui/icons/copy.gif')
        paste_icon = PhotoImage(file='gui/icons/paste.gif')
        undo_icon = PhotoImage(file='gui/icons/undo.gif')
        redo_icon = PhotoImage(file='gui/icons/redo.gif')
        node_icon = PhotoImage(file='gui/icons/node.gif')
        # duration_icon = PhotoImage(file='gui/icons/duration.gif')
        activity_icon = PhotoImage(file='gui/icons/activity.gif')
        line_icon = PhotoImage(file='gui/icons/line.gif')
        hand_icon = PhotoImage(file='gui/icons/hand.gif')
        delete_icon = PhotoImage(file='gui/icons/delete.gif')

    global icon
    icon = Icon()


def draw_checkered(canvas, line_distance, fill=None):
    # vertical lines at an interval of "line_distance" pixel
    canvas_width = 1500
    canvas_height = 1500
    if not fill:
        fill = "#DDDDDD"
    for x in range(line_distance, canvas_width, line_distance):
        canvas.create_line(x, 0, x, canvas_height, fill=fill, width=0.5)
    # horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance, canvas_height, line_distance):
        canvas.create_line(0, y, canvas_width, y, fill=fill, width=0.5)


def calc_decorate_arrow(start, end, radius):
    vec = {'x': (end[0] - start[0]), 'y': (end[1] - start[1])}
    dist = math.sqrt(vec.x * vec.x + vec.y * vec.y)
    vec = {'x': vec.x / dist, 'y': vec.y / dist}
    start = (start.x + vec.x * radius, start.y + vec.y * radius)
    dist = dist - radius
    end = (start.x + vec.x * dist, start.y + vec.y * dist)
    return (start, end)
