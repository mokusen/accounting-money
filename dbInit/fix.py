import csv
"""
meta.csvをソートするための機能
"""

# 対象ファイル名
base_meta_name = "dbInit/base.csv"

# 元データをリスト化する
with open(base_meta_name, newline='', encoding="utf-8") as before:
    reader = csv.reader(before)
    before_list = [row for row in reader]

# 元データをソートする
before_list.sort()

# 元データのcsvに加工したデータを登録する
with open(base_meta_name, "w", newline='', encoding="utf-8") as after:
    writer = csv.writer(after)
    for row in before_list:
        writer.writerow(row)
