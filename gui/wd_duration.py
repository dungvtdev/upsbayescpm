import tkinter as tk
from gui.utils.gui_component import ToggleGroup
from gui.utils.table_input import TableInput

class WdDuration(object):
    toggle_buttons = ('Impact', 'Control', 'Risk Event', 'Response')
    node_names = ('impact', 'control', 'risk_event', 'response')

    def __init__(self, master, duration_node, callback):
        self.master = master
        self.duration_node = duration_node

        self.table_input = None

        # master
        master.title = "Duration Model"

        frame = tk.Frame(self.master)
        self.frame = frame
        frame.pack(fill=tk.BOTH, expand=True)

        # control frame
        controlFrame = tk.Frame(frame)
        controlFrame.pack()

        # button ok, cancel
        btn_ok = tk.Button(controlFrame, text='OK')
        btn_ok.pack(side=tk.BOTTOM)
        btn_cancel = tk.Button(controlFrame, text='Cancel')
        btn_cancel.pack(side=tk.BOTTOM)

        # button show plot
        btn_pre_delay = tk.Button(controlFrame, text='Pre-Mitigation Delay')
        btn_pre_delay.pack(side=tk.BOTTOM)

        btn_delay = tk.Button(controlFrame, text='Delay')
        btn_delay.pack(side=tk.BOTTOM)

        # setting frame
        set_frame = tk.Frame(controlFrame)

        lb_setting_name = tk.Label(set_frame, text="Name", width=30)
        lb_setting_name.grid(row=0, column=0, columnspan=2)

        tk.Label(set_frame, text="Labels").grid(row=1,column=0)
        txt_labels = tk.Text(set_frame, width=20)
        txt_labels.grid(row=2, column=0)

        self.txt_node_labels = txt_labels

        tk.Label(set_frame, text="Data").grid(row=1, column=1)
        data_frame = tk.Frame(set_frame)
        data_frame.grid(row=2, column=1)

        self.data_frame = data_frame

        btn_apply_label = tk.Button(set_frame, text=">>", command=self.on_apply_label_setting_node)
        btn_apply_label.grid(row=3, column=0, stick='e')

        btn_apply_setting = tk.Button(set_frame, text="Apply", command=self.on_apply_setting_node)
        btn_apply_setting.grid(row=3, column=1, stick='e')


        # toggle
        toggle_group = ToggleGroup()
        self.toggle_group = toggle_group

        def on_toggle_click(index):
            toggle_group.click(index)
            lb_setting_name.config(text='Setting for: %s' % self.toggle_buttons[index])
            self.on_select_node()

        for i, tb in enumerate(self.toggle_buttons):
            btn = tk.Button(controlFrame, text=tb, command=lambda index=i: on_toggle_click(index))
            btn.pack(side=tk.TOP)
            toggle_group.add(btn)

        toggle_group.set_default(0)
        on_toggle_click(0) # set label for lb_setting_name

        set_frame.pack(side=tk.LEFT, expand=True)

    def get_current_setting_node_index(self):
        return self.toggle_group.index

    def get_current_setting_node(self):
        index = self.toggle_group.index
        return self.duration_node.get_node(self.node_names[index])

    def on_select_node(self):
        node = self.get_current_setting_node()

        # render setting
        str_labels = '\n'.join(node.labels)
        self.txt_node_labels.delete('0.0','end')
        self.txt_node_labels.insert('insert', str_labels)

        self.table_input = self.render_node_table(node, node.labels)

    def on_apply_label_setting_node(self):
        print('Show table')
        node = self.get_current_setting_node()
        str_labels = self.txt_node_labels.get('1.0','end')
        labels = str_labels.split('\n')
        labels = [x for x in labels if x]

        print('Node labels %s' % labels)

        self.table_input = self.render_node_table(node, labels)

    def on_apply_setting_node(self):
        print('Apply')
        node = self.get_current_setting_node()
        str_labels = self.txt_node_labels.get('1.0','end')
        labels = str_labels.split('\n')
        labels = [x for x in labels if x]
        node.set_labels(labels)
        node.set_data(self.table_input.export_data())

    def render_node_table(self, node, labels):
        for child in self.data_frame.winfo_children():
            child.destroy()

        print('node data %s' % node.get_data())
        return TableInput(self.data_frame, labels, node.get_table_labels(), node.get_data())


""" Test
"""

if __name__ == '__main__':
    root = tk.Tk()
    frame = tk.Frame(root)
    WdDuration(frame, None)
    frame.pack()
    root.mainloop()