import tkinter as tk


class Wd_Activity(object):

    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.frame = tk.Frame(self.master)
        top_frame = tk.Frame(self.frame)
        top_frame.pack(side='top', fill=tk.X)
        # Loc
        tk.Label(top_frame, text='Loc').pack(side=tk.LEFT)
        self.loc = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.loc).pack(side=tk.LEFT)
        self.loc.set('0')
        # Scale
        tk.Label(top_frame, text='Scale').pack(side=tk.LEFT)
        self.scale = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.scale).pack(side=tk.LEFT)
        self.scale.set('0')

        bottom_frame = tk.Frame(self.frame)
        bottom_frame.pack(
            side='bottom', fill='both', expand=True)

        ls_a_b = tk.Button(
            bottom_frame, text='LS', command=lambda: self.show_histogram(1))
        lf_a_b = tk.Button(
            bottom_frame, text='LF', command=lambda: self.show_histogram(2))
        es_a_b = tk.Button(
            bottom_frame, text='ES', command=lambda: self.show_histogram(3))
        ef_a_b = tk.Button(
            bottom_frame, text='EF', command=lambda: self.show_histogram(4))
        duration_a_b = tk.Button(
            bottom_frame, text='Duration', command=lambda: self.show_histogram(0))
        ls_a_b.grid(row=0, column=0)
        lf_a_b.grid(row=1, column=0)
        es_a_b.grid(row=0, column=3)
        ef_a_b.grid(row=1, column=3)
        duration_a_b.grid(row=0, column=1, columnspan=2, rowspan=2)

        ok_b = tk.Button(
            bottom_frame, text='OK', command=self.ok_input)
        cancel_b = tk.Button(
            bottom_frame, text='Cancel', command=self.close_windows)
        ok_b.grid(row=0, column=4, sticky='e')
        cancel_b.grid(row=1, column=4, sticky='e')

        self.frame.pack()

    def show_histogram(self, index):
        pass

    def close_windows(self):
        self.callback(False, None)
        self.master.destroy()

    def ok_input(self):
        self.callback(True, {'normal': (self.loc.get(), self.scale.get())})
        self.close_windows()
