def update_table(db, target, sort, order, search):
    rows = db.get_data(target, sort, order, search)
    return rows
