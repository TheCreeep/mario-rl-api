import psycopg2 as pg

def connect_db():
    con = pg.connect(
        database="mariorl", user="postgres", password="", host="localhost", port="5432"
    )

    return con
