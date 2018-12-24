import sqlite3
import os
from contextlib import closing
from method.utils import logger
import re

sql_logger = logger.set_sql_logger(__name__)

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def drop_base():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'drop table base'
        try:
            c.execute(sql)
            sql_logger.info(sql)
        except:
            pass


def drop_accounting():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'drop table accounting'
        try:
            c.execute(sql)
            sql_logger.info(sql)
        except:
            pass


def drop_cache():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'drop table cache'
        try:
            c.execute(sql)
            sql_logger.info(sql)
        except:
            pass
