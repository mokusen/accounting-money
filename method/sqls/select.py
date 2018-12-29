import sqlite3
import os
from contextlib import closing
from . import common
from method.utils import chms_logger
import re

sql_logger = chms_logger.set_sql_logger(__name__)

path = os.getcwd()
dbpath = path + '\data.db'
detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES


def select_base():
    """
    baseテーブルから用途一覧を取得する
    Returns
    -------
    result : tuple
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'select name from base order by name'
        result = [i[0] for i in c.execute(sql)]
        sql_logger.info(sql)
    return result


def select_accounting_export():
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'select use, money, year, month, day from accounting'
        result = [i for i in c.execute(sql)]
        sql_logger.info(sql)
    return result


def select_accounting(select_condition_list):
    """
    課金履歴をAND検索する
    Parameters
    ----------
    select_condition_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    Returns
    -------
    result : list型
        [id, use, money, year, month, day, create_ts, update_ts]
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'select * from accounting '
        add_sql, add_item = common._add_general_search_confition(select_condition_list)
        sql += add_sql
        result = common.multiple_condition_sql_execution(c, sql, add_item)
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {add_item}")
    return result


def select_accounting_year(select_condition_list):
    """
    年度別課金額を検索する
    Parameters
    ----------
    select_condition_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    Returns
    -------
    result : tuple
        [year , sum(money)]
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'select year, sum(money), month from accounting '
        add_sql, add_item = common._add_general_search_confition(select_condition_list)
        sql += add_sql
        sql += 'group by year, month order by year'
        result = common.multiple_condition_sql_execution(c, sql, add_item)
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {add_item}")
    return result


def select_accounting_use(select_condition_list):
    """
    用途別課金額を検索する
    Parameters
    ----------
    select_condition_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    Returns
    -------
    result : tuple
        [use, sum(money)]
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'select use, sum(money) from accounting '
        add_sql, add_item = common._add_general_search_confition(select_condition_list)
        sql += add_sql
        sql += 'group by use order by sum(money) desc'
        result = common.multiple_condition_sql_execution(c, sql, add_item)
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {add_item}")
    return result


def select_accounting_amount(select_condition_list, search_money_list):
    """
    ヒストグラムの金額に対する課金回数を検索する
    Parameters
    ----------
    select_condition_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    search_money_list : list
        0から課金額の全体最大まで、1000円ずつの刻みで登録されたリスト
    Returns
    -------
    result : tuple
        0から課金額の全体最大まで、1000円ずつの刻みに対する、課金回数
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'select'
        add_item = []
        for index in range(len(search_money_list)-1):
            sql += ' count(? < money and money <= ? or Null),'
            add_item.append(search_money_list[index])
            add_item.append(search_money_list[index + 1])
        sql = sql[:-1]
        sql += ' from accounting '
        add_sql, general_add_item = common._add_general_search_confition(select_condition_list)
        sql += add_sql
        add_item.extend(general_add_item)
        result = common.multiple_condition_sql_execution(c, sql, add_item)
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {add_item}")
    return result


def select_accounting_money():
    """
    全体の課金金額の最大値を取得する
    Returns
    -------
    result : max(money)
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'select max(money) from accounting '
        result = [i for i in c.execute(sql)]
        sql_logger.info(sql)
    return result


def select_accounting_period(select_condition_list):
    """
    期間別課金額を検索する
    Parameters
    ----------
    select_condition_list : list
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    Returns
    -------
    result : tuple
        [use, sum(money)]
    """
    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'select use, sum(money), year, month from accounting '
        add_sql, add_item = common._add_general_search_confition(select_condition_list)
        sql += add_sql
        sql += 'group by year, month, use '
        result = common.multiple_condition_sql_execution(c, sql, add_item)
        re_sql = re.sub('\n|    ', '', sql)
        sql_logger.info(f"{re_sql} {add_item}")
    return result


def select_cache():
    """
    キャッシュ情報を取得する
    Returns
    -------
    result : tuple
        [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
    """

    with closing(sqlite3.connect(dbpath, detect_types=detect_types)) as conn:
        c = conn.cursor()
        sql = 'select * from cache order by id desc'
        result = [i for i in c.execute(sql)]
        sql_logger.info(sql)
    return result
