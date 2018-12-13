from sqls import *


def insert_base(use):
    """
    用途を登録する
    Parameters
    ----------
    use : string
        新規の用途
    """
    insert.insert_base([use])


def select_base():
    """
    用途を検索し、一次リスト型で返却する

    Returns
    -------
    list型
        [use]
    """
    return select.select_base()


def insert_base(use):
    """
    用途を登録する
    Parameters
    ----------
    use : string
        新規の用途
    """
    insert.insert_base([use])
