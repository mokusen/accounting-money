import sqlite3
import os
from contextlib import closing
from . import common
from utils import logger
import re

sql_logger = logger.set_sql_logger(__name__)

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def _change_list(update_list):
    """
    変更情報リストの先頭情報(ID)を末尾に移動する

    Parameters
    ----------
    update_list : list型
        [id, ...]

    Returns
    -------
    update_list : list型
        [..., id]
    """

    id = update_list.pop(0)
    update_list.append(id)
    return update_list


def update_base(update_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # 更新時間を追加し、IDを後ろへ回す
        update_list = common._update_add_time(update_list)
        update_list = _change_list(update_list)
        update_list = common.__type_change_sqlValue(update_list)
        sql = 'update base set name = ?, update_ts = ? where id = ?'
        c.executemany(sql, update_list)
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {update_list}")
        conn.commit()


def update_accounting(update_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # 更新時間を追加し、IDを後ろへ回す
        update_list = common._update_add_time(update_list)
        update_list = _change_list(update_list)
        update_list = common.__type_change_sqlValue(update_list)
        sql = 'update accounting set use = ?, money = ?, year = ?, month = ?, day = ?, update_ts = ? where id = ?'
        c.executemany(sql, update_list)
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {update_list}")
        conn.commit()


def update_cache(update_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        update_list = common.__type_change_sqlValue(update_list)
        sql = 'update cache set use=?, min_money=?, max_money=?, min_year=?, max_year=?, min_month=?, max_month=?, min_day=?, max_day=? where id = 1'
        c.executemany(sql, update_list)
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {update_list}")
        conn.commit()
