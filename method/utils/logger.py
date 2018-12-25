from logging import Formatter, FileHandler, getLogger, DEBUG, INFO
import datetime


today = datetime.date.today().strftime('%Y%m%d')
fmt = Formatter('%(asctime)s %(levelname)s %(name)s %(funcName)s %(msg)s')


def set_operate_logger(file_name):
    handler = FileHandler(filename=f"./log/operate/{today}.log", encoding='utf-8')
    handler.setLevel(DEBUG)
    handler.setFormatter(fmt)
    logger = getLogger(file_name)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def set_sql_logger(file_name):
    handler = FileHandler(filename=f"./log/sql/{today}.log", encoding='utf-8')
    handler.setLevel(DEBUG)
    handler.setFormatter(fmt)
    logger = getLogger(file_name)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
