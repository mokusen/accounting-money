import sqlite3
import os
from contextlib import closing

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def delete_base(delete_id):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        sql = 'delete from base where id = ?'
        c.executemany(sql, delete_id)
        conn.commit()
    print("===EXIT_DELETE_BASE===")


def delete_accounting(delete_id):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        sql = 'delete from accounting where id = ?'
        c.executemany(sql, [delete_id])
        conn.commit()
    print("===EXIT_DELETE_ACCOUNTING===")


def delete_cache(delete_id):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        sql = 'delete from cache where id = ?'
        c.executemany(sql, [delete_id])
        conn.commit()
    print("===EXIT_DELETE_CACHE===")
