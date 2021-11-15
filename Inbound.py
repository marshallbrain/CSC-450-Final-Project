import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

from tkcalendar import Calendar

import utility


class Inbound:

    def __init__(self, main_frame, db):
        self.tab = ttk.Frame(main_frame)
        self.col = "id"
        self.ascending = False
        self.db = db
        self.search = ""

        self.tab.bind("<Visibility>", self.update)

        columns = ('id', 'name', 'item', 'amount', 'timestamp', 'tracking')
        table = ttk.Treeview(self.tab, columns=columns, show='headings')
        self.table = table

        new_item = ttk.Button(self.tab, text="New Item", command=lambda: self.create_item())
        new_item.pack()

        frame = ttk.Frame(self.tab)
        search_var = tk.StringVar()
        search_input = tk.Entry(frame, textvariable=search_var, width=30)
        search_input.pack(side=tk.LEFT)
        search = ttk.Button(frame, text="Search", command=lambda: self.search_table(search_var.get()))
        search.pack(side=tk.LEFT)
        frame.pack()

        table.heading('id', text='Id', anchor='w', command=lambda: self.sort_table("id", False))
        table.column('id', anchor="w", width=50)
        table.heading('name', text='Product Name', command=lambda: self.sort_table("name", False))
        table.column('name', anchor='center', width=200)
        table.heading('item', text='Product Id', command=lambda: self.sort_table("item", False))
        table.column('item', anchor='center', width=100)
        table.heading('amount', text='Amount', command=lambda: self.sort_table("amount", False))
        table.column('amount', anchor='center', width=100)
        table.heading('timestamp', text='Arrival Date', command=lambda: self.sort_table("timestamp", False))
        table.column('timestamp', anchor='center', width=100)
        table.heading('tracking', text='Tracking Number', command=lambda: self.sort_table("tracking", False))
        table.column('tracking', anchor='center', width=100)
        table.bind('<ButtonRelease-1>', self.select_item)

        table.pack()

        self.update_table()

    def sort_table(self, col, ascending):
        self.col = col
        self.ascending = ascending
        self.update_table()

        self.table.heading(col, command=lambda: self.sort_table(col, not ascending))

    def create_item(self):
        new_item = tk.Toplevel()
        new_item.wm_title("New Item")

        frame = ttk.Frame(new_item)

        name_var = tk.StringVar()
        name = tk.Label(frame, text="Product Name")
        name.grid(row=0, column=0)
        name_input = tk.Entry(frame, textvariable=name_var, width=30)
        name_input.grid(row=0, column=1, pady=5)

        item_var = tk.StringVar()
        item = tk.Label(frame, text="Product Id")
        item.grid(row=1, column=0)
        item_input = tk.Entry(frame, textvariable=item_var, width=30)
        item_input.grid(row=1, column=1, pady=5)

        amount_var = tk.StringVar()
        amount = tk.Label(frame, text="Amount")
        amount.grid(row=2, column=0)
        amount_input = tk.Entry(frame, textvariable=amount_var, width=30)
        amount_input.grid(row=2, column=1, pady=5)

        tracking_var = tk.StringVar()
        tracking = tk.Label(frame, text="Tracking Number")
        tracking.grid(row=3, column=0)
        tracking_input = tk.Entry(frame, textvariable=tracking_var, width=30)
        tracking_input.grid(row=3, column=1, pady=5)

        frame.pack(pady=5)

        cal = Calendar(new_item, selectmode='day')
        cal.pack(pady=10, padx=20)

        submit = ttk.Button(new_item, text="New Item",
                            command=lambda: self.add_item(new_item,
                                                          name_var.get(),
                                                          item_var.get(),
                                                          amount_var.get(),
                                                          cal.get_date(),
                                                          tracking_var.get()
                                                          ))
        submit.pack(pady=10)

    def add_item(self, window, name, item, amount, date, tracking):
        timestamp = datetime.strptime(date, "%m/%d/%y").timestamp()
        self.db.put_inbound(name, amount, item, timestamp, tracking)
        self.update_table()
        window.destroy()

    def update_table(self):
        rows = utility.update_table(self.db, "inbound", self.col, self.ascending, self.search)
        for i in self.table.get_children():
            self.table.delete(i)
        for row in rows:
            row = list(row)
            if row[2] == "":
                row[2] = "None"
            row[4] = datetime.fromtimestamp(row[4]).date()
            self.table.insert('', 'end', values=row)

    def search_table(self, search):
        self.search = search
        self.update_table()

    def select_item(self, event):
        item = self.table.identify_row(event.y)

        if item != "":
            item = self.table.item(item)["values"]
            info = tk.Toplevel()
            info.wm_title(item[1])

            print(item)

            name = tk.Label(info, text="Product Name: " + item[1])
            name.pack(pady=10, padx=10)
            track = tk.Label(info, text="Tracking number: " + str(item[5]))
            track.pack(padx=10)
            date = tk.Label(info, text="Arrival date: " + item[4])
            date.pack(pady=10, padx=10)
            amount = tk.Label(info, text="Amount: " + str(item[3]))
            amount.pack(padx=10)
            # ???????????????
            # item = tk.Label(info, text="Product Id: " + str(item[2]))
            # item.pack(pady=10, padx=10)

            submit = ttk.Button(info, text="Shipment Arrived", command=lambda: self.arrived(info, item[0]))
            submit.pack(pady=10)

    def arrived(self, window, prod_id):
        self.db.arrived(prod_id)
        window.destroy()
        self.update_table()

    def update(self, event):
        self.update_table()
