import sqlite3
import os
from contextlib import closing

path = os.getcwd()
print(path)
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

def create_base():
    with closing(sqlite3.connect(dbpath,detect_types=detect_types)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        sql = '''
        create table base
        (
        id integer primary key,
        name  text,
        create_ts TIMESTAMP,
        update_ts TIMESTAMP
        )
        '''
        c.execute(sql)
    print("===EXIT_CREATE_BASE===")

def create_accounting():
    with closing(sqlite3.connect(dbpath,detect_types=detect_types)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        sql = '''
        create table accounting
        (
        id integer primary key,
        money integer,
        use text,
        year integer,
        month integer,
        day integer,
        create_ts TIMESTAMP,
        update_ts TIMESTAMP
        )
        '''
        c.execute(sql)
    print("===EXIT_CREATE_ACCOUNTING===")
