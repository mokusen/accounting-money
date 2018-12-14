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
