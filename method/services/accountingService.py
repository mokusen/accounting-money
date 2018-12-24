import math
from method.sqls import *
from method.utils import adjustAccounting
from method.utils import logger

logger = logger.set_operate_logger(__name__)


def insert_accounting(insert_list):
    """
    課金履歴を登録する

    Parameters
    ----------
    insert_list : ２次元配列
        [[use, money, year, month, day],[use, money, year, month, day],...]
    """
    # monthとdayをint型に変換する
    for i in range(len(insert_list)):
        try:
            insert_list[i][3] = int(insert_list[i][3])
            insert_list[i][4] = int(insert_list[i][4])
        except:
            logger.error(f"月、日の入力値の型不正。プログラムの修正が必要です。 {insert_list}")
            return "月、日は選択肢からのみ選択してください"

    # インサートする
    for item in insert_list:
        insert.insert_accounting(item)
    return False


def update_accounting(update_list):
    """
    課金履歴を更新する

    Parameters
    ----------
    update_list : list型
        [id, use, money, year, month, day]

    """
    update_list = adjustAccounting.adjust_accounting(update_list)
    update.update_accounting(update_list)


def delete_accounting(delete_id):
    """
    課金履歴を削除する

    Parameters
    ----------
    delete_id : int
        id

    """
    delete.delete_accounting(delete_id)


def select_accounting(select_comdition_list):
    """Summary line.
    課金履歴を全件検索結果を取得し、対象期間の累計金額を返却する

    Parameters
    ----------
    select_comdition_list : list型
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]

    Returns
    -------
    all_data : list
        検索結果を格納したリスト。全要素が含まれる
    all_money : int
        対象期間内の累計金額
    """
    # 全件検索結果を取得する
    all_data = select.select_accounting(select_comdition_list)
    # 累計金額を算出する
    all_money = 0
    all_use = []
    for data in all_data:
        all_money += int(data[2])
    return all_data, all_money


def select_accounting_year(select_comdition_list):
    """
    年度別課金額を検索する
    Parameters
    ----------
    select_comdition_list : list型
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    Returns
    -------
    result : tuple
        [year , sum(money)]
    """
    return select.select_accounting_year(select_comdition_list)


def select_accounting_use(select_comdition_list):
    """
    用途別課金額を検索する
    Parameters
    ----------
    select_condition_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    Returns
    -------
    result : tuple
        [use, sum(money)]
    """
    return select.select_accounting_use(select_comdition_list)


def select_accounting_transaction(select_comdition_list):
    """
    ヒストグラムの金額に対する課金回数を検索する
    Parameters
    ----------
    select_condition_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    Returns
    -------
    search_money_list : list
        0から課金額の全体最大まで、1000円ずつの刻みで登録されたリスト
    result : tuple
        0から課金額の全体最大まで、1000円ずつの刻みに対する、課金回数
    """
    # FIXME: やばい
    max_money = select.select_accounting_money()[0][0]
    if max_money is None:
        max_money = 1000
    hist_lens = math.ceil(max_money/1000)
    search_money_list = [1000 * index for index in range(hist_lens + 1)]
    return search_money_list, select.select_accounting_transaction(select_comdition_list, search_money_list)


def test(select_comdition_list):
    return select.select_accounting_amount(select_comdition_list)
