import sqlite3
import os
from contextlib import closing

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

def select_base():
    with closing(sqlite3.connect(dbpath,detect_types=detect_types)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        sql = 'select name from base'
        result = []
        for i in c.execute(sql):
            result.append(i[0])
    print("===EXIT_SELECT_BASE===")
    return result

def select_accounting():
    with closing(sqlite3.connect(dbpath,detect_types=detect_types)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        sql = 'select * from accounting'
        result = []
        for i in c.execute(sql):
            result.append(i)
    print("===EXIT_SELECT_ACCOUNTING===")
    return result