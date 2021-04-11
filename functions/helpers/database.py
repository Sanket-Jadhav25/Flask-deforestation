import sqlite3 as sql
def db(db_path):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    rows = cur.execute('select * from prediction').fetchall()[-1]
    down1 = rows[0]
    email1 = rows[1]
    area1 = rows[2]
    region1 = rows[3]