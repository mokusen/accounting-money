from sqls import create, drop, insert, select
from dbInit import useListCreate, accountingListCreate
from datetime import datetime

drop.drop_base()
drop.drop_accounting()
drop.drop_cache()
create.create_base()
create.create_accounting()
create.create_cache()

# 初期メタデータ取得
use_list = useListCreate.create_init_list()

# 初期メタデータ挿入
for item in use_list:
    insert.insert_base(item)

# 初期cache情報挿入
insert.insert_cache([('', '', '', '', '', '', '', '', '')])

# 挿入されているメタデータを検索
meta_list = select.select_base()

# 初期課金履歴取得
accounting_list = accountingListCreate.create_list()

# 初期課金履歴挿入
for item in accounting_list:
    insert.insert_accounting(item)
