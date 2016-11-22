import tkinter as tk
from gui.utils.gui_component import ToggleGroup

class WdDuration(object):

    def __init__(self, master, duration_node):
        self.master = master
        self.duration_node = duration_node

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

        tk.Label(set_frame, text="Data").grid(row=1, column=1)
        data_frame = tk.Frame(set_frame)
        data_frame.grid(row=2, column=1)

        btn_apply_label = tk.Button(set_frame, text=">>")
        btn_apply_label.grid(row=3, column=0, stick='e')

        # toggle

        toggle_buttons = ('Impact', 'Control', 'Risk Event', 'Response')
        toggle_group = ToggleGroup()

        def on_toggle_click(index):
            toggle_group.click(index)
            lb_setting_name.config(text='Setting for: %s' % toggle_buttons[index])

        for i, tb in enumerate(toggle_buttons):
            btn = tk.Button(controlFrame, text=tb, command=lambda index=i: on_toggle_click(index))
            btn.pack(side=tk.TOP)
            toggle_group.add(btn)

        toggle_group.set_default(0)
        on_toggle_click(0) # set label for lb_setting_name

        set_frame.pack(side=tk.LEFT, expand=True)


        # tk.Label(controlFrame, text="Impact", width=10).grid(row=0, column=0, sticky='w')
        # btn_Impact = tk.Text(controlFrame)
        # in_impact.grid(row=0, column=1,sticky='w')
        #
        # tk.Label(controlFrame, text="Control", width=10).grid(row=1, column=0, sticky='w')
        # in_control = tk.Text(controlFrame)
        # in_control.grid(row=1, column=1,sticky='w')
        #
        # tk.Label(controlFrame, text="RiskEvent", width=10).grid(row=2, column=0, sticky='w')
        # in_riskEvent = tk.Text(controlFrame)
        # in_riskEvent.grid(row=2, column=1,sticky='w')
        #
        # tk.Label(controlFrame, text="Response", width=10).grid(row=3, column=0, sticky='w')
        # im_response = tk.Text(controlFrame)
        # im_response.grid(row=3, column=1,sticky='w')
        #
        # btn_pre_delay = tk.Button(controlFrame, text="Pre Delay")
        # btn_pre_delay.grid(row=4, column=0)
        #
        # btn_delay = tk.Button(controlFrame, text="Delay")
        # btn_delay.grid(row=5, column=0)


""" Test
"""

if __name__ == '__main__':
    root = tk.Tk()
    frame = tk.Frame(root)
    WdDuration(frame, None)
    frame.pack()
    root.mainloop()