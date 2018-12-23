# chms
課金履歴管理システム（Charge history management system）<br>
課金履歴を登録、参照、更新、削除するGUIアプリケーション

## 出来ること
- 課金履歴を登録、参照、更新、削除する
- 課金履歴を検索して、グラフで表すことが出来る
    - 年度別課金額
    - 用途別課金額
    - 期間別課金額
    - 課金額別回数

## Requirements
My environment is as follows.

|  | Version |
| :--- | :--- |
| Python | 3.7.1 |
| wxPython | 4.0.3 |
| matplotlib | 3.0.2 |
| pandas | 0.23.4 |

## Quick start
### 1. init setting

```PowerShell
# Windows
> mkdir (Clone destination directory)
> cd (Clone destination directory)
> python -m (any environment name) venv
> `\(any environment name)\scripts\activate.ps1
```

```bash
# Linux
$ mkdir (Clone destination directory)
$ cd (Clone destination directory)
$ python -m (any environment name) venv
$ source (any environment name)/bin/activate
```

### 2. Clone application

```bash
# if current_directory then
git clone https://github.com/mokusen/chms.git
# else then
cd (Clone destination directory)
git clone https://github.com/mokusen/chms.git
```

### 3. install requirement:

```bash
pip install -r requirement.txt
```

### 4. init data
if you want to insert data into the db, please prepare base.csv and accounting.csv in dbInit.<br>


#### File structure of base.csv
to save use name.<br>
encoding type is utf-8.<br>
Here is an example!

```
music,
test,
other,
```

#### File structure of accounting.csv
to save use, use money, year(YYYY), month(MM) ,day(DD).<br>
encoding type is utf-8.<br>
Here is an example!

```
music,1250,2012,11,19
other,1700,2012,12,15
test,5200,2012,12,29
music,850,2012,12,31
test,5200,2013,1,2
test,450,2013,1,6
```

### 5. init db
In the case of 4. init data, please remove `#` from datebase_init.py.<br>
After, Please execute the following code

```bash
python datebase_init.py
```

### 6. start main
Please execute the following code

```bash
python main.py
```