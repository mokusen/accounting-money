import glob
import os
import re
from . import chms_logger, handleYaml

logger = chms_logger.set_operate_logger(__name__)


def check_logfile():
    """
    ログディレクトリの制限処理を行う
    """
    operate_path = os.getcwd() + "/log/operate"
    sql_path = os.getcwd() + "/log/sql"
    __check_logfile_limit(operate_path)
    __check_logfile_limit(sql_path)


def __check_logfile_limit(path):
    """
    ログディレクトリの保存ファイル数、容量の制限処理を行う
    Parameters
    ----------
    path : log directory path
    """
    logger.info("START")
    # 設定ファイルから、設定情報を取得する
    file_limit = handleYaml.get_config_file_limit()
    directory_capacity = handleYaml.get_config_directory_capacity()
    # ディレクトリ情報を取得する
    file_list = sorted([os.path.basename(p) for p in glob.glob(path+"\**")])
    file_len = len(file_list)
    # ファイル数を7個制限にする
    if file_len >= file_limit:
        logger.info(f"DO by {file_limit}")
        for index in range(file_len-file_limit):
            os.remove(f"{path}\{file_list[index]}")
    # ファイル数が0の時は、容量チェックを行わない
    if file_len != 0:
        # 設定容量調整
        directory_size_list = __get_directory_size_list(path)
        directory_capacity = __compare_directory_size_today_file(directory_capacity, directory_size_list)
        # ディレクトリ容量を10MB制限にする
        while sum(directory_size_list) > directory_capacity:
            logger.info(f"DO by {directory_capacity}[Bytes]")
            os.remove(f"{path}\{file_list[0]}")
            file_list.pop(0)
            directory_size_list.pop(0)
    logger.info("END")


def __get_directory_size_list(path):
    """
    指定されたPathのディレクトリに含まれるファイルの容量をリスト形式で取得する
    Parameters
    ----------
    path : log directory path
    Returns
    -------
    directory_size_list : list
    """
    directory_size_list = [size.stat().st_size for size in os.scandir(path) if size.is_file()]
    return directory_size_list


def __compare_directory_size_today_file(directory_capacity, directory_size_list):
    """
    設定された制限容量が、今日使用するログファイルの容量より小さい時、制限容量を今日のログファイルと同値にする
    Parameters
    ----------
    directory_capacity : int
        制限容量
    directory_size_list : list
    Returns
    -------
    directory_capacity : int
        制限容量
    """
    if directory_capacity < directory_size_list[-1]:
        directory_capacity = directory_size_list[-1]
    return directory_capacity
