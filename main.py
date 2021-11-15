import tkinter as tk
import tkinter.ttk as ttk

import Inbound
import MainInventory
import Outbound
from Database import Database

database = Database()


def main():
    window = tk.Tk()
    window.title("UNCW Football!")
    tab_control = ttk.Notebook(window)

    inventory = MainInventory.MainInventory(tab_control, database)
    tab_control.add(inventory.tab, text="Main Inventory")

    inbound = Inbound.Inbound(tab_control, database)
    tab_control.add(inbound.tab, text="Inbound Shipments")

    outbound = Outbound.Outbound(tab_control, database)
    tab_control.add(outbound.tab, text="Outbound Shipments")

    tab_control.pack(expand=1, fill="both")

    # # TAB2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # tab2 = ttk.Frame((tabControl))
    # tabControl.add(tab2, text="Outbound")
    # tabControl.pack(expand=1, fill="both")
    # columns = ('id', 'name', 'amount', 'shipdate', 'destination')
    # table = ttk.Treeview(tab2, columns=columns, show='headings')
    #
    # new_item = ttk.Button(tab2, text="Outbound", command=lambda: create_item(table))
    # new_item.pack()
    #
    # table.heading('id', text='ID', anchor='w', command=lambda: sort_table(table, "id", False))
    # table.column('id', anchor="w", width=50)
    # table.heading('name', text='Product Name', command=lambda: sort_table(table, "name", False))
    # table.column('name', anchor='center', width=200)
    # table.heading('shipdate', text='Shipping Date', command=lambda: sort_table(table, "shipdate", False))
    # table.column('shipdate', anchor='center', width=100)
    # table.heading('destination', text='Destination', command=lambda: sort_table(table, "destination", False))
    # table.column('destination', anchor='center', width=100)
    # update_table(table)
    # table.pack()
    # # TAB3~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # tab3 = ttk.Frame((tabControl))
    # tabControl.add(tab3, text="Inbound")
    # tabControl.pack(expand=1, fill="both")
    # columns = ('id', 'name', 'amount', 'arrivaldate','tracking')
    # table = ttk.Treeview(tab3, columns=columns, show='headings')
    #
    # new_item = ttk.Button(tab3, text="Inbound", command=lambda: create_item(table))
    # new_item.pack()
    #
    # table.heading('id', text='ID', anchor='w', command=lambda: sort_table(table, "id", False))
    # table.column('id', anchor="w", width=50)
    # table.heading('name', text='Product Name', command=lambda: sort_table(table, "name", False))
    # table.column('name', anchor='center', width=200)
    # table.heading('arrivaldate', text='Arrival Date', command=lambda: sort_table(table, "arrivaldate", False))
    # table.column('arrivaldate', anchor='center', width=100)
    # table.heading('tracking', text='Tracking Number', command=lambda: sort_table(table, "tracking", False))
    # table.column('tracking', anchor='center', width=100)
    # update_table(table)
    # table.pack()
    #
    # # TAB4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # tab4 = ttk.Frame((tabControl))
    # tabControl.add(tab4, text="Users")
    # tabControl.pack(expand=1, fill="both")
    # columns = ('id', 'name', 'email', 'shift')
    # table = ttk.Treeview(tab4, columns=columns, show='headings')
    #
    # new_item = ttk.Button(tab4, text="New Item", command=lambda: create_item(table))
    # new_item.pack()
    #
    # table.heading('id', text='ID', anchor='w', command=lambda: sort_table(table, "id", False))
    # table.column('id', anchor="w", width=50)
    # table.heading('name', text='Employee Name', command=lambda: sort_table(table, "name", False))
    # table.column('name', anchor='center', width=200)
    # table.heading('email', text='Email', command=lambda: sort_table(table, "email", False))
    # table.column('email', anchor='center', width=100)
    # table.heading('shift', text='Shift', command=lambda: sort_table(table, "shift", False))
    # table.column('shift', anchor='center', width=100)
    # update_table(table)
    # table.pack()

    window.mainloop()


if __name__ == '__main__':
    main()