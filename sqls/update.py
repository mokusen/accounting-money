import sqlite3
import os
from contextlib import closing
from datetime import datetime

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


def _add_time(update_list):
    """
    変更情報に更新時間を追加し、リスト内を整備する

    Parameters
    ----------
    update_list : list型
        [id, ...]

    Returns
    -------
    [update_list] : tuple型
        (.., id)
    """

    update_list.append(datetime.now())
    update_list = _change_list(update_list)
    update_list = [tuple(update_list)]
    return update_list


def update_base(update_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()

        # 作成時間と更新時間を追加する
        update_list = _add_time(update_list)

        # executeメソッドでSQL文を実行する
        sql = 'update base set name = ?, update_ts = ? where id = ?'
        c.executemany(sql, update_list)
        conn.commit()
    print("===EXIT_UPDATE_BASE===")


def update_accounting(update_list):
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()

        # 作成時間と更新時間を追加する
        update_list = _add_time(update_list)
        print(update_list)

        # executeメソッドでSQL文を実行する
        sql = 'update accounting set use = ?, money = ?, year = ?, month = ?, day = ?, update_ts = ? where id = ?'
        c.executemany(sql, update_list)
        conn.commit()
    print("===EXIT_UPDATE_ACCOUNTING===")
