from sqls import select


def search_base():
    return select.select_base()


def search_accounting(use_value=None, money_value_1=None, money_value_2=None,
                      year_value_1=None, year_value_2=None, month_value_1=None, month_value_2=None,
                      day_value_1=None, day_value_2=None):
    """Summary line.
    課金履歴を全件検索結果を取得し、対象期間の累計金額を返却する

    Parameters
    ----------
    use_value : string
        用途 (the default is None)
    money_value_1 : int
        下限金額 (the default is None)
    money_value_2 : int
        上限金額 (the default is None)
    year_value_1 : int
        下限年 (the default is None)
    year_value_2 : int
        上限年 (the default is None)
    month_value_1 : int
        下限月 (the default is None)
    month_value_2 : int
        上限月 (the default is None)
    day_value_1 : int
        下限日 (the default is None)
    day_value_2 : int
        上限日 (the default is None)

    Returns
    -------
    all_data : list
        検索結果を格納したリスト。全要素が含まれる
    all_money : int
        対象期間内の累計金額
    """

    # TODO log処理追加

    # 全件検索結果を取得する
    all_data = select.select_accounting(use_value, money_value_1, money_value_2, year_value_1, year_value_2, month_value_1, month_value_2, day_value_1, day_value_2)

    # 累計金額を算出する
    all_money = 0
    all_use = []
    for data in all_data:
        all_money += int(data[2])

    return all_data, all_money
