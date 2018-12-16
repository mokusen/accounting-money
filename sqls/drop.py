import sqlite3
import os
from contextlib import closing

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def drop_base():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = '''
        drop table base
        '''
        try:
            c.execute(sql)
        except:
            pass
    print("===EXIT_DROP_BASE===")


def drop_accounting():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = '''
        drop table accounting
        '''
        try:
            c.execute(sql)
        except:
            pass
    print("===EXIT_DROP_ACCOUNTING===")


def drop_cache():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = '''
        drop table cache
        '''
        try:
            c.execute(sql)
        except:
            pass
    print("===EXIT_DROP_CACHE===")
