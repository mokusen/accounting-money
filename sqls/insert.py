import sqlite3
import os
from contextlib import closing

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

def insert_base(insert_list):
    with closing(sqlite3.connect(dbpath,detect_types=detect_types)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        sql = 'insert into base (name, create_ts, update_ts) values (?,?,?)'
        c.executemany(sql, insert_list)
        conn.commit()
    print("===EXIT_INSERT_BASE===")

def insert_accounting(insert_list):
    with closing(sqlite3.connect(dbpath,detect_types=detect_types)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        sql = 'insert into accounting (money, use, year, month, day, create_ts, update_ts) values (?,?,?,?,?,?,?)'
        c.executemany(sql, insert_list)
        conn.commit()
    print("===EXIT_INSERT_ACCOUNTING===")
