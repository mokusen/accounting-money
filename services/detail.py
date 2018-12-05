from sqls import update, delete
from utils import adjustAccounting

def update_accounting(after_list):
    # TODO update
    after_list = adjustAccounting.adjustAccounting(after_list)
    update.update_accounting(after_list)

def delete():
    # TODO update
    print("TEST")