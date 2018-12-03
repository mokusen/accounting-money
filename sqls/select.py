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

def select_accounting(use_value=None,money_value_1=None,money_value_2=None,
                        year_value_1=None,year_value_2=None,month_value_1=None,month_value_2=None,
                        day_value_1=None,day_value_2=None):
    """
    課金履歴をAND検索する

    Parameters
    ----------
    search_dict : list in dict型
        {
            検索ワード：[検索値1,　検索値2],
        }

    Returns
    -------
    result : list型
        money, use, year, month, day情報を有するリスト型
    """
    with closing(sqlite3.connect(dbpath,detect_types=detect_types)) as conn:
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'select money, use, year, month, day, create_ts, update_ts from accounting '
        add_sql = 'where '
        add_item = []

        if use_value != '' and use_value !='選択':
            add_sql += 'use = ? and '
            add_item.append(use_value)
        if money_value_1 != '':
            add_sql += 'money >= ? and '
            add_item.append(money_value_1)
        if money_value_2 != '':
            add_sql += 'money <= ? and '
            add_item.append(money_value_2)
        if year_value_1 != '':
            add_sql += 'year >= ? and '
            add_item.append(year_value_1)
        if year_value_2 != '':
            add_sql += 'year <= ? and '
            add_item.append(year_value_2)
        if month_value_1 != '':
            add_sql += 'month >= ? and '
            add_item.append(month_value_1)
        if month_value_2 != '':
            add_sql += 'month <= ? and '
            add_item.append(month_value_2)
        if day_value_1 != '':
            add_sql += 'day >= ? and '
            add_item.append(day_value_1)
        if day_value_2 != '':
            add_sql += 'day <= ? and '
            add_item.append(day_value_2)
        if len(add_item) == 0:
            add_sql = add_sql[6:]
        add_sql = add_sql[:-4]
        sql += add_sql
        add_item = tuple(add_item)
        print(add_sql)
        print(add_item)
        print(sql)
        result = []
        if len(add_item) == 0:
            for i in c.execute(sql):
                print(i)
                result.append(i)
        else:
            for i in c.execute(sql, add_item):
                print(i)
                result.append(i)
        print("===EXIT_SELECT_ACCOUNTING===")
    return result
