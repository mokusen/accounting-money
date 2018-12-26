import pathlib
import os


def exist_csv_log_directory():
    """
    ログディレクトリが存在確認処理を行う
    """
    csvin_path = os.getcwd() + "/CsvIn"
    csvout_path = os.getcwd() + "/CsvOut"
    operate_path = os.getcwd() + "/log/operate"
    sql_path = os.getcwd() + "/log/sql"
    __exist_csv_log_directory(csvin_path)
    __exist_csv_log_directory(csvout_path)
    __exist_csv_log_directory(operate_path)
    __exist_csv_log_directory(sql_path)


def __exist_csv_log_directory(path):
    """
    保存先のディレクトリが存在するか確認し、存在しない場合は作成する
    Parameters
    ----------
    path : log directory path
    """
    log_directory = pathlib.Path(path)
    if log_directory.is_dir() is False:
        os.makedirs(path)
