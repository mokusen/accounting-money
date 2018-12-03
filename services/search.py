from sqls import select

def search_accounting(use_value=None,money_value_1=None,money_value_2=None,
                        year_value_1=None,year_value_2=None,month_value_1=None,month_value_2=None,
                        day_value_1=None,day_value_2=None):
    """
    課金履歴を全件検索結果を取得する
    Return
    ------
    all_data : ２次元配列
        課金履歴の時間まで含めた全件取得データ
    """
    # TODO log処理追加

    # 全件検索結果を取得する
    all_data = select.select_accounting(use_value,money_value_1,money_value_2,year_value_1,year_value_2,month_value_1,month_value_2,day_value_1,day_value_2)
    print(use_value,money_value_1,money_value_2,year_value_1,year_value_2,month_value_1,month_value_2,day_value_1,day_value_2)
    return all_data