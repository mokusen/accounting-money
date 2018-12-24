import sqlite3
import os
from contextlib import closing
from method.utils import logger
import re

sql_logger = logger.set_sql_logger(__name__)

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def create_base():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = '''
        create table if not exists base
        (
        id integer primary key,
        name  text,
        create_ts TIMESTAMP,
        update_ts TIMESTAMP
        )
        '''
        c.execute(sql)
        sql_logger.info(re.sub('\n|    ', '', sql))


def create_accounting():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = '''
        create table if not exists accounting
        (
        id integer primary key,
        use text,
        money integer,
        year integer,
        month integer,
        day integer,
        create_ts TIMESTAMP,
        update_ts TIMESTAMP
        )
        '''
        c.execute(sql)
        sql_logger.info(re.sub('\n|    ', '', sql))


def create_cache():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = '''
        create table if not exists cache
        (
        id integer primary key,
        use text,
        min_money integer,
        max_money integer,
        min_year integer,
        max_year integer,
        min_month integer,
        max_month integer,
        min_day integer,
        max_day integer
        )
        '''
        c.execute(sql)
        sql_logger.info(re.sub('\n|    ', '', sql))
