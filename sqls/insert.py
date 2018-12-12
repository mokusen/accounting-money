import sqlite3
import os
from contextlib import closing
from datetime import datetime

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def _add_time(insert_list):
    insert_list.append(datetime.now())
    insert_list.append(datetime.now())
    insert_list = [tuple(insert_list)]
    return insert_list


def insert_base(insert_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()

        # 作成時間と更新時間を追加する
        insert_list = _add_time(insert_list)

        # executeメソッドでSQL文を実行する
        sql = 'insert into base (name, create_ts, update_ts) values (?,?,?)'
        c.executemany(sql, insert_list)
        conn.commit()
    print("===EXIT_INSERT_BASE===")


def insert_accounting(insert_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()

        # 作成時間と更新時間を追加する
        insert_list = _add_time(insert_list)

        # executeメソッドでSQL文を実行する
        sql = 'insert into accounting (use, money, year, month, day, create_ts, update_ts) values (?,?,?,?,?,?,?)'
        c.executemany(sql, insert_list)
        conn.commit()
    print("===EXIT_INSERT_ACCOUNTING===")
