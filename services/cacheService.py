from sqls import *
from utils import adjustAccounting
from utils import logger

logger = logger.set_operate_logger(__name__)


def insert_cache(insert_list):
    """
    検索条件を登録する

    Parameters
    ----------
    insert_list : 1次元配列
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    """
    # money、year、month、dayをint型に変換する
    for index in range(1, len(insert_list)):
        if insert_list[index] != '':
            try:
                insert_list[index] = int(insert_list[index])
            except:
                logger.error(f"金額、年、月、日の入力値の型不正。プログラムの修正が必要です。 {insert_list}")
                return "金額、年、月、日は選択肢からのみ選択してください"

    # インサートする
    insert.insert_cache(insert_list)


def delete_cache(delete_id):
    """
    検索条件を削除する

    Parameters
    ----------
    delete_id : int
        id

    """
    delete.delete_cache(delete_id)


def select_cache():
    """Summary line.
    検索条件を全件検索結果を取得する

    Returns
    -------
    all_cache_infodata : list
        検索条件を格納したリスト。全要素が含まれる
    """
    # 全件検索結果を取得する
    cache_info = select.select_cache()
    return cache_info


def update_cache(update_list):
    """
    課金履歴を更新する

    Parameters
    ----------
    update_list : list型
        [id, use, money, year, month, day]

    """
    update.update_cache(update_list)


def init_cache():
    """
    課金履歴を初期化する
    """
    update.update_cache(['', '', '', '', '', '', '', '', ''])
