import sqlite3
import os
from contextlib import closing
from . import common

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def insert_base(insert_list):
    """
    baseテーブルに情報を保存する
    Parameters
    ----------
    insert_list : list
        [name]
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        insert_list = common._insert_add_time(insert_list)
        insert_list = common.__type_change_sqlValue(insert_list)
        sql = 'insert into base (name, create_ts, update_ts) values (?,?,?)'
        c.executemany(sql, insert_list)
        conn.commit()
    print("===EXIT_INSERT_BASE===")


def insert_accounting(insert_list):
    """
    accountingテーブルに情報を登録する
    Parameters
    ----------
    insert_list : list
        [use, money, year, month, day]
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        insert_list = common._insert_add_time(insert_list)
        insert_list = common.__type_change_sqlValue(insert_list)
        sql = 'insert into accounting (use, money, year, month, day, create_ts, update_ts) values (?,?,?,?,?,?,?)'
        c.executemany(sql, insert_list)
        conn.commit()
    print("===EXIT_INSERT_ACCOUNTING===")


def insert_cache(insert_list):
    """
    cacheテーブルに情報を登録する
    Parameters
    ----------
    insert_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        insert_list = common.__type_change_sqlValue(insert_list)
        sql = 'insert into cache (use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day) values (?,?,?,?,?,?,?,?,?)'
        c.executemany(sql, insert_list)
        conn.commit()
    print("===EXIT_INSERT_CACHE===")
