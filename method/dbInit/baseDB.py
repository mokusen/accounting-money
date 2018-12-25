import csv
from method.sqls import select
from method.utils import logger

logger = logger.set_operate_logger(__name__)


def create_init_list():
    """
    用途のデータベース登録用のデータリストを作成する

    Returns
    -------
    base_list : list型
        用途のデータリストを格納してあるcsvからlistを作成する
    """
    logger.info("DO insert db from base.csv")
    base_meta_name = "CsvIn/base.csv"
    # 対象ファイル名(実行ディレクトリはmain.pyである)
    with open(base_meta_name, newline='', encoding="utf-8") as before:
        reader = csv.reader(before)
        base_list = [[row[0]] for row in reader]
    return base_list


def csv_export():
    logger.info("DO export db from base.csv")
    base_meta_name = "CsvOut/base.csv"
    data_list = [[data] for data in select.select_base()]
    with open(base_meta_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data_list)
