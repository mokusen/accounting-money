import sqlite3
from datetime import datetime


def __type_change_sqlValue(change_list):
    """
    sqlのvalue指定に対応するためにlist in tuple型を作成する

    Parameters
    ----------
    change_list : list
        list型であればよい

    Returns
    -------
    change_list : list in tuple
    """
    return [tuple(change_list)]


def _insert_add_time(change_list):
    """
    変更情報に作成、更新時間を追加する

    Parameters
    ----------
    change_list : list型
        [id, ...]

    Returns
    -------
    change_list : list型
        [.., id]
    """
    change_list.append(datetime.now())
    change_list.append(datetime.now())
    return change_list


def _update_add_time(change_list):
    """
    変更情報に更新時間を追加する

    Parameters
    ----------
    change_list : list型
        [id, ...]

    Returns
    -------
    change_list : list型
        [.., id]
    """

    change_list.append(datetime.now())
    return change_list


def _add_general_search_confition(select_condition_list):
    """
    検索画面に存在する検索条件をsql発行する

    Parameters
    ----------
    select_condition_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]

    Returns
    -------
    add_sql : sql
    add_item : list
        上記の検索条件に一致するアイテムを所持する
    """

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
    return add_sql, add_item


def multiple_condition_sql_execution(c, sql, add_item):
    """
    複数条件

    Parameters
    ----------
    c: [type]
        [description]
    sql: [type]
        [description]
    add_item: [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
    result = []
    if len(add_item) == 0:
        for i in c.execute(sql):
            result.append(i)
    else:
        for i in c.execute(sql, add_item):
            result.append(i)
    return result
