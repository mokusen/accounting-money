import sqlite3
import os
from contextlib import closing
from . import common

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def select_base():
    """
    baseテーブルから用途一覧を取得する
    Returns
    -------
    result : tuple
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'select name from base order by name'
        result = []
        for i in c.execute(sql):
            result.append(i[0])
        print("===EXIT_SELECT_BASE===")
    return result


def select_accounting(select_condition_list):
    """
    課金履歴をAND検索する
    Parameters
    ----------
    select_condition_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    Returns
    -------
    result : list型
        [id, use, money, year, month, day, create_ts, update_ts]
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'select * from accounting '
        add_sql, add_item = common._add_general_search_confition(select_condition_list)
        sql += add_sql
        print(sql)
        result = common.multiple_condition_sql_execution(c, sql, add_item)
        print("===EXIT_SELECT_ACCOUNTING===")
    return result


def select_accounting_year(select_condition_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'select year, sum(money) from accounting '
        add_sql, add_item = common._add_general_search_confition(select_condition_list)
        sql += add_sql
        sql += 'group by year order by year'
        result = common.multiple_condition_sql_execution(c, sql, add_item)
        print("===EXIT_SELECT_ACCOUNTING_YEAR===")
        print(result)
    return result


def select_accounting_use(select_condition_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'select use, sum(money) from accounting '
        add_sql, add_item = common._add_general_search_confition(select_condition_list)
        sql += add_sql
        sql += 'group by use order by use'
        result = common.multiple_condition_sql_execution(c, sql, add_item)
        print("===EXIT_SELECT_ACCOUNTING_USE===")
        print(result)
    return result


def select_accounting_transaction(select_condition_list, search_money_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'select'
        add_item = []
        for index in range(len(search_money_list)-1):
            sql += ' count(? < money and money <= ? or Null),'
            add_item.append(search_money_list[index])
            add_item.append(search_money_list[index + 1])
        sql = sql[:-1]
        sql += ' from accounting '
        add_sql, r_add_item = common._add_general_search_confition(select_condition_list)
        sql += add_sql
        add_item.extend(r_add_item)
        print(sql)
        print(add_item)
        result = common.multiple_condition_sql_execution(c, sql, add_item)
        print("===EXIT_SELECT_ACCOUNTING_TRANSACTION===")
        print(result)
    return result


def select_accounting_money():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'select max(money) from accounting '
        result = []
        for i in c.execute(sql):
            result.append(i)
        print("===EXIT_SELECT_ACCOUNTING_MONEY===")
        print(result)
    return result


def select_cache():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'select * from cache order by id desc'
        result = []
        for i in c.execute(sql):
            result.append(i)
        print("===EXIT_SELECT_CACHE===")
    return result
