import glob
import os
import re
from method.utils import logger

logger = logger.set_operate_logger(__name__)


def check_logfile():
    operate_path = os.getcwd() + "\log\operate"
    sql_path = os.getcwd() + "\log\sql"
    __check_logfile_limit(operate_path)
    __check_logfile_limit(sql_path)


def __check_logfile_limit(path):
    logger.info("START")
    file_list = sorted([os.path.basename(p) for p in glob.glob(path+"\**")])
    file_len = len(file_list)
    # ファイル数を7個制限にする
    if file_len >= 7:
        logger.info("DO by 7")
        for index in range(file_len-7):
            os.remove(f"{path}\{file_list[index]}")
    # ディレクトリ容量を10MB制限にする
    directory_size_list = __get_directory_size_list(path)
    while sum(directory_size_list) >= 1024 * 1024 * 10:
        logger.info("DO by 10MB")
        os.remove(f"{path}\{file_list[0]}")
        file_list.pop(0)
        directory_size_list.pop(0)
    logger.info("END")


def __get_directory_size_list(path):
    directory_size_list = [size.stat().st_size for size in os.scandir(path) if size.is_file()]
    return directory_size_list
