from sqls import create, drop, insert, select
from utils import useListCreate, accountingListCreate
from datetime import datetime

drop.drop_base()
drop.drop_accounting()
create.create_base()
create.create_accounting()

# 初期メタデータ取得
use_list = useListCreate.create_init_list()

# 初期メタデータ挿入
for item in use_list:
    # item = [(item, datetime.now(), datetime.now())]
    insert.insert_base(item)

# 挿入されているメタデータを検索
meta_list = select.select_base()

# 出力
for item in meta_list:
    print(item)

# 初期課金履歴取得
accounting_list = accountingListCreate.create_list()

# 初期課金履歴挿入
for item in accounting_list:
    # item.append(datetime.now())
    # item.append(datetime.now())
    # item = [tuple(item)]
    insert.insert_accounting(item)

# 挿入されている課金履歴を検索
accountinged_list = select.select_accounting()

# 出力
for item in accountinged_list:
    print(item)
