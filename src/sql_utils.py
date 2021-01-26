import io
import sqlite3

import numpy as np


def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)


def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect("sqlite.db")
        cur = sqliteConnection.cursor()

        sqlite_select_query = "select * from users"
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("Id: ", row[0])
            print("mfcc: ", type(row[1]))
            print("\n")

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)


def create_db_table(table, id, mfcc):
    cur.execute(f"create table {table}(id integer primary key, arr array)")


def remove_db_row(table, id):
    try:
        with sqlite3.connect("sqlite.db", detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute(f"delete from {table} where id={id}")

    except Exception as err:
        print(f"Database row doesn't exist for id ({id}) in table ({table}): ", err)


def select_db_row(table, id):
    try:
        with sqlite3.connect("sqlite.db", detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()

            rows = cur.execute(f"select * from {table} where id={id}")
            for row in rows:
                print("Id: ", row[0])
                print("mfcc: ", row[1])
                print("\n")
                return row
    except Exception as err:
        print("Database doesn't exist: ", err)


def insert_db_row(table, id, mfcc):
    try:
        with sqlite3.connect("sqlite.db", detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute(f"insert into {table}(id, mfcc) values (?, ?)", (id, mfcc,))
    except Exception as err:
        print("Database doesn't exist: ", err)
