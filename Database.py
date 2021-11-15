import sqlite3
from datetime import datetime


class Database:

    def __init__(self):
        self.database = sqlite3.connect("database.db")
        self.init_tables()

    def init_tables(self):
        cursor = self.database.cursor()
        cursor.execute("""create table if not exists inventory (
        id integer primary KEY,
        name text not null,
        amount integer default 1);""")
        cursor.execute("""create table if not exists inbound (
        id integer primary key,
        name text not null,
        item integer default -1,
        amount integer default 1,
        timestamp integer not null,
        traking integer default 0);""")
        cursor.execute("""create table if not exists outbound (
        id integer primary key,
        name text not null,
        item integer not null,
        amount integer default 1,
        timestamp integer not null);""")

    def put_data(self, name, amount):
        cursor = self.database.cursor()
        cursor.execute("INSERT INTO inventory(name,amount) VALUES(?,?)",
                       (name, amount))
        self.database.commit()

    def put_inbound(self, name, amount, item, timestamp, tracking):
        cursor = self.database.cursor()
        cursor.execute("INSERT INTO inbound(name,item,amount,timestamp,traking) VALUES(?,?,?,?,?)",
                       (name, item, amount, timestamp, tracking))
        self.database.commit()

    def put_outbound(self, name, amount, item, timestamp):
        cursor = self.database.cursor()
        cursor.execute("INSERT INTO outbound(name,item,amount,timestamp) VALUES(?,?,?,?)",
                       (name, item, amount, timestamp))
        self.database.commit()

    def get_data(self, table, sort="", reverse=False, search=""):
        cursor = self.database.cursor()
        order = "desc" if reverse else "asc"
        queue = "SELECT * FROM {0}".format(table)
        if search != "":
            queue += " where name LIKE '%" + search + "%'"
        queue += " order by {0} {1}".format(sort, order)
        cursor.execute(queue)
        return cursor.fetchall()

    def arrived(self, prod_id):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM inbound where id=?", (prod_id,))
        item = cursor.fetchall()[0]
        if item[2] == "":
            cursor.execute("INSERT INTO inventory(name,amount) VALUES(?,?)", (item[1], item[3]))
        else:
            cursor.execute("SELECT * FROM inventory where id=?", (item[2],))
            amount = cursor.fetchall()[0][2]

            cursor.execute(""" UPDATE inventory
                SET amount = ?
                WHERE id = ?""", (amount+item[3], item[2]))

        cursor.execute("DELETE FROM inbound WHERE id=?", (prod_id,))
        self.database.commit()

    def shipped(self, prod_id):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM outbound where id=?", (prod_id,))
        item = list(cursor.fetchall()[0])

        cursor.execute("SELECT * FROM inventory where id=?", (item[2],))
        amount = cursor.fetchall()[0][2]-item[3]

        if amount < 1:
            cursor.execute("DELETE FROM inventory WHERE id=?", (item[2],))
        else:
            cursor.execute(""" UPDATE inventory
                SET amount = ?
                WHERE id = ?""", (amount, item[2]))

        cursor.execute("DELETE FROM outbound WHERE id=?", (prod_id,))
        self.database.commit()
