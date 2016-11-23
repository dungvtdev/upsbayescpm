import tkinter as tk


class TableInput(object):
    def __init__(self, master, rows, columns, data):
        """
        :param master: TK object
        :param rows: list-liked: label rows
        :param columns: like rows
        """
        self.master = master
        self.rows = rows
        self.columns = columns
        self.data = data

        self.items = [[0 for c in range(len(columns))] for r in range(len(rows))]

        self.create_gui()

    def create_gui(self):
        if not (self.rows and self.columns):
            return

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
                entry.delete(0, "end")
                if self.data:
                    entry.insert(0, self.data[r][c])


    def export_data(self):
        data = [[self.items[r][c].get() for c in range(len(self.columns))] for r in range(len(self.rows))]
        return data

""" Test
"""
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     frame = tk.Frame(root)
#     frame.pack()
#     app = TableInput(frame,['A', 'B', 'C'], ['True', 'False'], None, lambda _,__,data: print(data))
#     root.mainloop()