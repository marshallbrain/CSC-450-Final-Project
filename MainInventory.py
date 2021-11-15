import tkinter as tk
import tkinter.ttk as ttk

import utility


class MainInventory:

    def __init__(self, main_frame, db):
        self.tab = ttk.Frame(main_frame)
        self.col = "id"
        self.ascending = False
        self.db = db
        self.search = ""

        self.tab.bind("<Visibility>", self.update)

        columns = ('id', 'name', 'amount')
        table = ttk.Treeview(self.tab, columns=columns, show='headings')
        self.table = table

        frame = ttk.Frame(self.tab)
        search_var = tk.StringVar()
        search_input = tk.Entry(frame, textvariable=search_var, width=30)
        search_input.pack(side=tk.LEFT)
        search = ttk.Button(frame, text="Search", command=lambda: self.search_table(search_var.get()))
        search.pack(side=tk.LEFT)
        frame.pack()

        table.heading('id', text='ID', anchor='w', command=lambda: self.sort_table("id", False))
        table.column('id', anchor="w", width=50)
        table.heading('name', text='Product Name', command=lambda: self.sort_table("name", False))
        table.column('name', anchor='center', width=200)
        table.heading('amount', text='Amount', command=lambda: self.sort_table("amount", False))
        table.column('amount', anchor='center', width=100)
        table.pack()

        self.update_table()

    def sort_table(self, col, ascending):
        self.col = col
        self.ascending = ascending
        self.update_table()

        self.table.heading(col, command=lambda: self.sort_table(col, not ascending))

    def update_table(self):
        rows = utility.update_table(self.db, "inventory", self.col, self.ascending, self.search)
        for i in self.table.get_children():
            self.table.delete(i)
        for row in rows:
            self.table.insert('', 'end', values=row)

    def search_table(self, search):
        self.search = search
        self.update_table()

    def update(self, event):
        self.update_table()
