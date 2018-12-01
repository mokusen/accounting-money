import csv

def create_list():
    """
    用途のデータリストを作成する

    Returns
    -------
    base_list : list型
        用途のデータリストを格納してあるcsvからlistを作成する
    """

    # 対象ファイル名(実行ディレクトリはmain.pyである)
    base_meta_name = "meta.csv"
    with open(base_meta_name, newline='', encoding="utf-8") as before:
        reader = csv.reader(before)
        base_list = [row[0] for row in reader]
    return base_list