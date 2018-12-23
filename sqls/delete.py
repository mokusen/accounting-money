import sqlite3
import os
from contextlib import closing
from utils import logger
import re

sql_logger = logger.set_sql_logger(__name__)

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def delete_base(delete_id):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'delete from base where id = ?'
        c.executemany(sql, delete_id)
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {delete_id}")
        conn.commit()
    print("===EXIT_DELETE_BASE===")


def delete_accounting(delete_id):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'delete from accounting where id = ?'
        c.executemany(sql, [delete_id])
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {delete_id}")
        conn.commit()
    print("===EXIT_DELETE_ACCOUNTING===")


def delete_cache(delete_id):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'delete from cache where id = ?'
        c.executemany(sql, [delete_id])
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {delete_id}")
        conn.commit()
    print("===EXIT_DELETE_CACHE===")
