import tkinter as tk


class TableInput(object):
    def __init__(self, master, rows, columns, callback_flag, callback):
        """
        :param master: TK object
        :param rows: list-liked: label rows
        :param columns: like rows
        :param callback_flag: thong tin them de tra lai ham callback
        :param callback:
        """
        self.master = master
        self.rows = rows
        self.columns = columns
        self.callback_flag = callback_flag
        self.callback = callback

        self.items = [[0 for c in range(len(columns))] for r in range(len(rows))]

        self.create_gui()

    def create_gui(self):
        width = 12
        frame = tk.Frame(self.master)
        frame.pack(expand='yes')

        # label x
        for i, col in enumerate(self.columns):
            tk.Label(frame, text=col, width=width).grid(row=0, column=i+1)

        # label y
        for i, row in enumerate(self.rows):
            tk.Label(frame, text=row, width=width).grid(row=i+1, column=0)

        # label body
        for r in range(len(self.rows)):
            for c in range(len(self.columns)):
                entry = tk.Entry(frame, width=width)
                entry.grid(row=r+1, column=c+1)
                self.items[r][c] = entry

        # button OK, cancel
        r = r +1
        c = c +1
        btn_OK = tk.Button(frame, text="OK", command=self.on_ok_click)
        btn_OK.grid(row=r+1, column=c-1)
        btn_Cancel = tk.Button(frame, text="Cancel", command=self.on_cancel_click)
        btn_Cancel.grid(row=r+1, column=c)

    def export_data(self):
        data = [[self.items[r][c].get() for c in range(len(self.columns))] for r in range(len(self.rows))]
        return data

    def on_ok_click(self):
        if self.callback:
            self.callback(True, self.callback_flag, self.export_data())
        self.master.destroy()

    def on_cancel_click(self):
        self.callback(False, self.callback_flag, None)
        self.master.destroy

""" Test
"""

if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    app = TableInput(frame,['A', 'B', 'C'], ['True', 'False'], None, lambda _,__,data: print(data))
    root.mainloop()