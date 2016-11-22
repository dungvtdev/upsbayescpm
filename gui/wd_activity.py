import tkinter as tk
# import mybayes as bayes
import matplotlib.pyplot as plt

class Wd_Activity(object):

    def __init__(self, master, node, callback):
        self.master = master
        self.node = node
        self.callback = callback
        self.frame = tk.Frame(self.master)
        top_frame = tk.Frame(self.frame)
        top_frame.pack(side='top', fill=tk.X)
        # Loc
        tk.Label(top_frame, text='Loc').pack(side=tk.LEFT)
        self.loc = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.loc).pack(side=tk.LEFT)
        self.loc.set(self.node.data['normal'][0])
        # Scale
        tk.Label(top_frame, text='Scale').pack(side=tk.LEFT)
        self.scale = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.scale).pack(side=tk.LEFT)
        self.scale.set(self.node.data['normal'][1])

        bottom_frame = tk.Frame(self.frame)
        bottom_frame.pack(
            side='bottom', fill='both', expand=True)

        ls_a_b = tk.Button(
            bottom_frame, text='LS', command=lambda: self.show_histogram('ls'))
        lf_a_b = tk.Button(
            bottom_frame, text='LF', command=lambda: self.show_histogram('lf'))
        es_a_b = tk.Button(
            bottom_frame, text='ES', command=lambda: self.show_histogram('es'))
        ef_a_b = tk.Button(
            bottom_frame, text='EF', command=lambda: self.show_histogram('ef'))
        duration_a_b = tk.Button(
            bottom_frame, text='Duration', command=lambda: self.show_histogram('duration'))
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

    def show_histogram(self, name_hist):
        print('Show Hist %s' % name_hist)
        bayes_nodes = self.node.bayes_nodes
        if bayes_nodes and len(bayes_nodes) == 5:
            bayes_node = self.node.get_bayes_node(name_hist)
            bayes_node.get_histogram()
            bayes_node.draw_bar()
            plt.show()
        else:
            print('Chua update')

    def close_windows(self):
        self.callback(False, self.node, None)
        self.master.destroy()

    def ok_input(self):
        self.callback(True, self.node, {
                      'normal': (self.loc.get(), self.scale.get())})
        self.master.destroy()
