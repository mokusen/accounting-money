from sqls import update, delete
from utils import adjustAccounting

def update_accounting(after_list):
    after_list = adjustAccounting.adjustAccounting(after_list)
    update.update_accounting(after_list)

def delete_accounting(delete_id):
    delete.delete_accounting(delete_id)