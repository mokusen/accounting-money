import sqlite3
import os
from contextlib import closing

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def select_base():
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
    search_dict : list in dict型
        {
            検索ワード：[検索値1,　検索値2],
        }

    Returns
    -------
    result : list型
        money, use, year, month, day情報を有するリスト型
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'select * from accounting '
        add_sql = 'where '
        add_item = []

        if select_condition_list[0] != '' and select_condition_list[0] != '選択':
            add_sql += 'use = ? and '
            add_item.append(select_condition_list[0])
        if select_condition_list[1] != '':
            add_sql += 'money >= ? and '
            add_item.append(select_condition_list[1])
        if select_condition_list[2] != '':
            add_sql += 'money <= ? and '
            add_item.append(select_condition_list[2])
        if select_condition_list[3] != '':
            add_sql += 'year >= ? and '
            add_item.append(select_condition_list[3])
        if select_condition_list[4] != '':
            add_sql += 'year <= ? and '
            add_item.append(select_condition_list[4])
        if select_condition_list[5] != '':
            add_sql += 'month >= ? and '
            add_item.append(select_condition_list[5])
        if select_condition_list[6] != '':
            add_sql += 'month <= ? and '
            add_item.append(select_condition_list[6])
        if select_condition_list[7] != '':
            add_sql += 'day >= ? and '
            add_item.append(select_condition_list[7])
        if select_condition_list[8] != '':
            add_sql += 'day <= ? and '
            add_item.append(select_condition_list[8])
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
                result.append(i)
        else:
            for i in c.execute(sql, add_item):
                result.append(i)
        print("===EXIT_SELECT_ACCOUNTING===")
    return result
