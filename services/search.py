from sqls import select

def all_search():
    """
    課金履歴を全件検索結果を取得する
    Return
    ------
    all_data : ２次元配列
        課金履歴の時間まで含めた全件取得データ
    """
    # TODO log処理追加

    # 全件検索結果を取得する
    all_data = select.select_accounting()
    return all_data