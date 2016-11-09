from tkinter import *
import tkinter.messagebox
import math
from . model import *
from . wd_activity import Wd_Activity

from . import utils
from . import model


class MainApplication(object):
    node_half_size = (40, 30)
    node_fill = "#00FF00"
    outline = "#000000"
    choosen_outline = "#FF0000"
    border_width = 1

    activity_half_size = (40, 30)
    activity_fill = "#FFFF00"

    line_fill = "#000000"
    line_width = 1

    def __init__(self, master, name):
        self.master = master
        self.wd_name = name
        self.model = model.Model()
        self.create_gui()
        self.bind_mouse()

    def create_gui(self):
        self.create_menu()
        self.create_bottom_bar()
        self.create_top_bar()
        self.create_side_panel()
        self.create_canvas()
        self.bind_menu_accelrator_keys()

    def create_menu(self):
        icon = utils.icon
        menu_bar = Menu(self.master)
        """ File menu"""
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New', accelerator='Ctrl+N',
                              compound='left', image=icon.new_file_icon,
                              underline=0, command=self.new_file)
        file_menu.add_command(label='New Network', accelerator='Ctrl+Alt+N',
                              compound='left', image=icon.new_file_icon,
                              underline=0, command=self.new_network)
        file_menu.add_separator()
        file_menu.add_command(
            label='Exit', accelerator='Alt+F4', command=self.exit_editor)
        menu_bar.add_cascade(label='File', menu=file_menu)

        """ Nodes menu"""
        nodes_menu = Menu(menu_bar, tearoff=0)

        nodes_menu.add_command(
            label='Node', compound='left', underline=0, command=self.new_node)
        # nodes_menu.add_command(
        # label='Duration', compound='left', underline=0,
        # command=self.new_duration)
        nodes_menu.add_command(
            label='Activity', compound='left', underline=0, command=self.new_activity)
        menu_bar.add_cascade(label='Nodes', menu=nodes_menu)

        """ Run menu """
        run_menu = Menu(menu_bar, tearoff=0)
        run_menu.add_command(label='Update', compound='left',
                             underline=0, command=self.run)

        menu_bar.add_cascade(label='Run', menu=run_menu)

        self.menu_bar = menu_bar
        self.master.config(menu=menu_bar)

    def create_top_bar(self):
        self.top_bar = Frame(self.master, height=25, relief="raised")
        self.tool_functions = (
            'hand_tool',
            'create_activity_tool', 'create_arc_tool', 'delete_tool')
        self.tool_name = ('No Tool',
                          'Create Activity', 'Create Arc', 'Delete')
        ic = utils.icon
        icons = (ic.hand_icon, ic.activity_icon,
                 ic.line_icon, ic.delete_icon)
        self.selected_tool_function = self.tool_functions[0]
        for index, name in enumerate(self.tool_functions):
            icon = icons[index]
            self.button = Button(self.top_bar, image=icon,
                                 command=lambda index=index: self.on_tool_button_clicked(index))
            self.button.pack(side="left", padx=2)
            self.button.image = icon
        self.top_bar.pack(fill="x", side="top", pady=2)

    def create_bottom_bar(self):
        self.bottom_bar = Frame(self.master, height=25, relief="raised")
        self.bottom_bar.pack(fill="x", side="bottom", pady=2)
        self.current_tool_label = Label(self.bottom_bar, text="test")
        self.current_tool_label.pack(side="right", fill="both", expand="yes")

    def create_side_panel(self):
        self.tool_bar = Frame(self.master, relief="raised", width=120)
        Label(self.tool_bar, text="Networks").pack(side="top")
        self.list_network = Listbox(self.tool_bar)
        self.list_network.pack(fill="both", expand="yes",
                               side="top", padx=5, pady=5)
        self.tool_bar.pack(fill="y", side="left", pady=3)

    def create_canvas(self):
        self.canvas_frame = Frame(self.master, width=900, height=900)
        self.canvas_frame.pack(side="right", expand="yes", fill="both")
        Label(self.canvas_frame, text="Graph").pack(side="top")
        self.canvas = Canvas(self.canvas_frame, background="white",
                             width=500, height=500, scrollregion=(0, 0, 800, 800))
        self.create_scroll_bar()
        self.canvas.pack(side="right", expand=YES, fill=BOTH)
        utils.draw_checkered(self.canvas, 80)

    def create_scroll_bar(self):
        x_scroll = Scrollbar(self.canvas_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        x_scroll.config(command=self.canvas.xview)
        y_scroll = Scrollbar(self.canvas_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
        y_scroll.config(command=self.canvas.yview)
        self.canvas.config(
            xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

    def bind_menu_accelrator_keys(self):
        pass

    """ Command """

    def new_file(self):
        pass

    def new_network(self):
        pass

    def exit_editor(self):
        if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
            root.destroy()

    def new_node(self):
        pass

    def new_duration(self):
        pass

    def new_activity(self):
        pass

    def run(self):
        print('run')

    """ Actions"""

    def function_not_defined(self, *argv):
        pass

    def execute_selected_method(self, state):
        # self.current_item = None
        func = getattr(
            self, self.selected_tool_function, self.function_not_defined)
        func(state)

    def on_tool_button_clicked(self, index):
        self.selected_tool_function = self.tool_functions[index]
        # hien thi ten vao bottom
        self.current_tool_label.config(
            text='Tool: %s' % self.tool_name[index])
        # self.bind_mouse()

    # def create_node_tool(self, state):
    #     # print('Create_node_tool')
    #     if state == 0:
    #         if self.canvas.find_withtag("current"):
    #             self.selecting_item = self.canvas.find_withtag("current")
    #             self.draw_choosen()
    #             # return
    #         else:
    #             w = self.node_half_size[0]
    #             h = self.node_half_size[1]
    #             self.current_item = self.canvas.create_oval(
    #                 self.end_x - w, self.end_y - h, self.end_x + w, self.end_y + h,
    #                 outline=self.outline, fill=self.node_fill, width=self.border_width)
    #     if state == 1:
    #         pass

    #     if state == 2:
    #         # apply change
    #         self.selecting_item = self.current_item
    #         self.current_item = None
    #         self.draw_choosen()

    def get_current_node(self):
        cur = self.canvas.find_withtag("current")
        if cur:
            if self.model.is_node(cur[0]):
                return cur[0]

    def create_activity_tool(self, state):
        # print('Create_node_tool')
        if state == 0:
            cur = self.get_current_node()
            print('create activity cur %s' % str(cur))
            if cur:
                self.selecting_item = cur
                self.draw_choosen()
                # return
            else:
                w = self.activity_half_size[0]
                h = self.activity_half_size[1]
                self.current_item = self.canvas.create_oval(
                    self.end_x - w, self.end_y - h, self.end_x + w, self.end_y + h,
                    outline=self.outline, fill=self.activity_fill, width=self.border_width)
        if state == 1:
            pass

        if state == 2:
            # apply change
            node = NodeModel('test')
            node.node_id = self.current_item
            self.model.add_node(node)

            self.selecting_item = self.current_item
            self.current_item = None
            self.draw_choosen()

    def hand_tool(self, state):
        if state == 0:
            self.selecting_item = None
            cur = self.get_current_node()
            if cur:
                self.selecting_item = cur
                self.canvas.move(
                    "current", self.end_x - self.start_x, self.end_y - self.start_y)
                self.canvas.bind("<B1-Motion>", self.drag_item_update_x_y)
                self.draw_choosen()
        if state == 2:
            # move arc
            if self.selecting_item:
                arcs = self.model.get_arcs_attach_node(self.selecting_item)
                item = self.selecting_item
                for a in arcs:
                    start = self.get_node_pos(a.start_id)
                    end = self.get_node_pos(a.end_id)
                    self.canvas.delete(a.arc_id)
                    a_id, start, end = self.draw_arrow(
                        start, end, self.node_half_size[0])
                    a.arc_id = a_id
                    a.start_pos = start
                    a.end_pos = end

    def drag_item_update_x_y(self, event):
        self.start_x, self.start_y = self.end_x, self.end_y
        self.end_x, self.end_y = event.x, event.y
        self.hand_tool(0)

    def get_node_pos(self, node_id):
        coords = self.canvas.coords(node_id)
        pos = ((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2)
        return pos

    def delete_tool(self, state):
        current = self.get_current_node()
        if not current:
            return
        if state == 0:
            self.selecting_item = current
            self.draw_choosen()
            if tkinter.messagebox.askokcancel("Delete?", "Really delete?"):
                self.canvas.delete(current)
                self.canvas.delete(self.choose_view)
                # delete model
                self.model.remove_node(current)
                arcs = self.model.get_arcs_attach_node(current)
                if arcs:
                    for a in arcs:
                        self.canvas.delete(a.arc_id)
                        self.model.remove_arc(a)

    def create_arc_tool(self, state):
        # print("Draw arc")
        if state == 0:
            cur = self.get_current_node()
            if cur:
                self.selecting_item = cur
                self.draw_choosen()

        if state == 1 and self.selecting_item:
            self.canvas.delete(self.current_item)
            # self.current_item = self.canvas.create_line(
            #     self.start_x, self.start_y, self.end_x, self.end_y, fill=self.line_fill,
            #     width=self.line_width, arrow="last")
            # self.current_item = self.canvas.create_line(
            # self.start_x, self.start_y, self.end_x, self.end_y,
            # fill=self.line_fill, width=self.line_width, arrow="last")
            self.current_item, _, _ = self.draw_arrow((self.start_x, self.start_y),
                                                      (self.end_x, self.end_y), self.node_half_size[0])

        if state == 2 and self.selecting_item:
            cur = self.get_current_node()
            # if cur == self.current_item:
            #     cur = self.canvas.find_below(cur)
            self.canvas.delete(self.current_item)
            self.current_item = None
            # print(cur)
            # print(self.selecting_item)
            if cur and cur != self.selecting_item:
                # apply
                start = self.canvas.coords(self.selecting_item)
                start = ((start[0] + start[2]) / 2, (start[1] + start[3]) / 2)
                end = self.canvas.coords(cur)
                end = ((end[0] + end[2]) / 2, (end[1] + end[3]) / 2)

                # print('start, end %s, %s' % (str(start), str(end)))
                # self.draw_arrow(start, end, self.node_half_size[0])
                radius = self.node_half_size[0]
                line_item, start, end = self.draw_arrow(
                    start, end, self.node_half_size[0])
                arc = ArcModel()
                arc.start_id = self.selecting_item
                arc.end_id = cur
                arc.start_pos = start
                arc.end_pos = end
                arc.arc_id = line_item
                self.model.add_arc(arc)

    def wd_activity_callback(self, is_ok, dict):
        if is_ok:
            print(dict)

    """ Mouse """

    def bind_mouse(self):
        self.canvas.bind("<Button-1>", self.on_mouse_button_pressed)
        self.canvas.bind(
            "<Button1-Motion>", self.on_mouse_button_pressed_motion)
        self.canvas.bind(
            "<Button1-ButtonRelease>", self.on_mouse_button_released)
        # self.canvas.bind("<Motion>", self.on_mouse_unpressed_motion)
        self.canvas.bind("<Double-Button-1>", self.on_mouse_button_dbclick)

    def on_mouse_button_pressed(self, event):
        self.start_x = self.end_x = self.canvas.canvasx(event.x)
        self.start_y = self.end_y = self.canvas.canvasy(event.y)
        self.execute_selected_method(0)

    def on_mouse_button_pressed_motion(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.execute_selected_method(1)

    def on_mouse_button_released(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.execute_selected_method(2)

    # def on_mouse_unpressed_motion(self, event):
    #     self.show_current_coordinates(event)

    def on_mouse_button_dbclick(self, event):
        print('Double click')
        cur = self.get_current_node()
        if cur:
            self.selecting_item = cur
            self.draw_choosen()
            utils.show_window(self.master, Wd_Activity, self.wd_activity_callback)

    """ Draw """

    def draw_choosen(self):
        item = self.selecting_item
        # print('Select %d' % item)
        if not item:
            return
        coords = self.canvas.coords(item)
        if hasattr(self, 'choose_view'):
            self.canvas.delete(self.choose_view)
        self.choose_view = self.canvas.create_oval(
            coords[0] - 10, coords[1] - 10, coords[2] + 10, coords[3] + 10,
            outline=self.choosen_outline, fill=None, width=self.border_width * 2)

    def draw_arrow(self, start, end, radius):
        start, end = utils.calc_decorate_arrow(start, end, radius)
        # print('start, e %s %s' %(str(start), str(end)))
        line_item = self.canvas.create_line(
            start[0], start[1], end[0], end[1], fill=self.line_fill, width=self.line_width, arrow="last")
        return line_item, start, end


