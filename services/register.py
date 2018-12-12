from sqls import insert


def register_base(use):
    """
    用途を登録する
    Parameters
    ----------
    use : string
        新規の用途
    """
    insert.insert_base([use])


def register(duble_list):
    """
    課金履歴を登録する

    Parameters
    ----------
    duble_list : ２次元配列
        ２次元配列型で登録する情報を受け取る
    """
    # monthとdayをint型に変換する
    for i in range(len(duble_list)):
        try:
            duble_list[i][3] = int(duble_list[i][3])
            duble_list[i][4] = int(duble_list[i][4])
        except:
            return "月、日は選択肢からのみ選択してください"
    # TODO: log処理追加

    # インサートする
    for item in duble_list:
        insert.insert_accounting(item)
