from functions.connect_db import connect_db

def get_settings():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM settings")
    row = cur.fetchone()
    cur.close()
    con.close()
    return row
