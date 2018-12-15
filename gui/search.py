import wx
from . import mainGui, detail, common
from utils import dataListCreate
from services import accountingService, baseService, cacheService
from operator import itemgetter


class Search(wx.Frame):
    def __init__(self, parent, id, title):
        self.frame_size = (625, 600)
        wx.Frame.__init__(self, parent, id, title, size=self.frame_size)
        self.SetIcon(common.get_icon())
        self.CreateStatusBar()
        MainPanel(self)
        self.Bind(wx.EVT_CLOSE, self.frame_close)
        self.Centre()
        self.Show()

    def frame_close(self, event):
        self.Destroy()
        wx.Exit()
        mainGui.call_mainGui()


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.frame_size = (625, 600)
        self.__myinit()

        # 詳細ページ表示イベント
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.detail_open)

    def __myinit(self):
        # 初期設定
        self.input_defalut_text = "選択"
        use_list = baseService.select_base()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()

        # 検索結果格納リスト
        self.all_data = []

        # 初期値追加
        use_list.insert(0, '')

        # size設定
        form_size = (100, 25)
        text_size = (50, 25)

        # font設定
        self.font = common.defalut_font_size()

        # 検索フォームのラベル作成
        text_use = wx.StaticText(self, wx.ID_ANY, '用途', size=text_size, style=wx.TE_CENTER)
        text_money = wx.StaticText(self, wx.ID_ANY, '金額', size=text_size, style=wx.TE_CENTER)
        text_year = wx.StaticText(self, wx.ID_ANY, '年', size=text_size, style=wx.TE_CENTER)
        text_month = wx.StaticText(self, wx.ID_ANY, '月', size=text_size, style=wx.TE_CENTER)
        text_day = wx.StaticText(self, wx.ID_ANY, '日', size=text_size, style=wx.TE_CENTER)

        # 検索フォームのラベルフォント設定
        text_use.SetFont(self.font)
        text_money.SetFont(self.font)
        text_year.SetFont(self.font)
        text_month.SetFont(self.font)
        text_day.SetFont(self.font)

        # 検索フォーム作成
        self.search_use = wx.ComboBox(self, wx.ID_ANY, self.input_defalut_text, choices=use_list, style=wx.CB_READONLY, size=form_size)
        self.search_money_list = []
        self.search_year_list = []
        self.search_month_list = []
        self.search_day_list = []

        # タブの進行方向設定のため、分けて行う
        for i in range(2):
            self.search_money_list.append(wx.TextCtrl(self, wx.ID_ANY, size=form_size))
        for i in range(2):
            self.search_year_list.append(wx.TextCtrl(self, wx.ID_ANY, size=form_size))
        for i in range(2):
            self.search_month_list.append(wx.ComboBox(self, wx.ID_ANY, choices=month_list, style=wx.CB_READONLY, size=form_size))
        for i in range(2):
            self.search_day_list.append(wx.ComboBox(self, wx.ID_ANY, choices=day_list, style=wx.CB_READONLY, size=form_size))

        # ~を作成する
        text_tilde_list = []
        for i in range(4):
            text_tilde_list.append(wx.StaticText(self, wx.ID_ANY, '～', size=(25, 25), style=wx.TE_CENTER))

        # 検索ボタン
        search_button = wx.Button(self, wx.ID_ANY, '検索')

        # 検索ボタンにイベントを登録する
        search_button.Bind(wx.EVT_BUTTON, self.call_select)

        # notebook
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        self.__create_notebook()

        # Textの幅を個別設定する
        width_list = [30, 80, 60, 60, 50, 50, 125, 125]
        for index, width in enumerate(width_list):
            self.search_result_text.SetColumnWidth(index, width)

        # 検索フォームのレイアウト設定
        search_layout = wx.GridBagSizer(10, 5)
        search_layout.Add(text_use, (0, 0), (1, 1), flag=wx.EXPAND)
        search_layout.Add(self.search_use, (0, 1), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_money, (1, 0), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_year, (0, 4), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_month, (1, 4), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_day, (2, 4), (1, 1), flag=wx.EXPAND)
        for i in range(2):
            search_layout.Add(self.search_money_list[i], (1, 1 + i*2), (1, 1), flag=wx.EXPAND)
            search_layout.Add(self.search_year_list[i], (0, 5 + i*2), (1, 1), flag=wx.EXPAND)
            search_layout.Add(self.search_month_list[i], (1, 5 + i*2), (1, 1), flag=wx.EXPAND)
            search_layout.Add(self.search_day_list[i], (2, 5 + i*2), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_tilde_list[0], (1, 2), (1, 1), flag=wx.EXPAND)
        for i in range(3):
            search_layout.Add(text_tilde_list[i+1], (i, 6), (1, 1), flag=wx.EXPAND)
        search_layout.Add(search_button, (2, 1), (1, 3), flag=wx.EXPAND)

        # レイアウト設定
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(search_layout, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)
        layout.Add(self.notebook, flag=wx.EXPAND)

        # ソートイベントを登録する
        self.Bind(wx.EVT_LIST_COL_CLICK, self.call_sort)

        # cache情報を取得し、反映する
        test_date = cacheService.select_cache()
        self.search_use.SetValue(str(test_date[0][1]))
        self.search_money_list[0].SetValue(str(test_date[0][2]))
        self.search_money_list[1].SetValue(str(test_date[0][3]))
        self.search_year_list[0].SetValue(str(test_date[0][4]))
        self.search_year_list[1].SetValue(str(test_date[0][5]))
        self.search_month_list[0].SetValue(str(test_date[0][6]))
        self.search_month_list[1].SetValue(str(test_date[0][7]))
        self.search_day_list[0].SetValue(str(test_date[0][8]))
        self.search_day_list[1].SetValue(str(test_date[0][9]))

        self.SetSizer(layout)

    def __create_notebook(self):
        self.search_result_panel = wx.Panel(self.notebook, wx.ID_ANY)
        self.statistics_panel = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.InsertPage(0, self.search_result_panel, '検索結果')
        self.notebook.InsertPage(1, self.statistics_panel, '統計情報')
        self.__create_search_result()
        self.__create_statistics()

    def __create_search_result(self):
        Text = (u'ID', u'用途', u'金額', u'年', u'月', u'日', u'作成日', u'更新日')
        # 検索結果を表示するリストコントローラ
        self.frame_size = (600, 400)
        self.search_result_text = wx.ListCtrl(self.search_result_panel, wx.ID_ANY, size=self.frame_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_EDIT_LABELS)
        for i, text in enumerate(Text):
            self.search_result_text.InsertColumn(i, text)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.search_result_text, (0, 0), (1, 1), flag=wx.EXPAND)
        self.search_result_panel.SetSizer(layout)
        self.search_result_panel.Layout()

    def __create_statistics(self):
        self.fiscal_year_panel = wx.Panel(self.statistics_panel, wx.ID_ANY)
        self.by_title_panel = wx.Panel(self.statistics_panel, wx.ID_ANY)
        self.per_transaction_panel = wx.Panel(self.statistics_panel, wx.ID_ANY)
        self.__fiscal_year()
        self.__by_title()
        self.__per_transaction()
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.fiscal_year_panel, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.by_title_panel, (0, 1), (1, 1), flag=wx.EXPAND)
        layout.Add(self.per_transaction_panel, (0, 2), (1, 1), flag=wx.EXPAND)
        self.statistics_panel.SetSizer(layout)
        self.statistics_panel.Layout()

    def __fiscal_year(self):
        title = wx.StaticText(self.fiscal_year_panel, wx.ID_ANY, "年度別課金額")
        Text = (u'年', u'金額')
        # 検索結果を表示するリストコントローラ
        self.fiscal_year_text = wx.ListCtrl(self.fiscal_year_panel, wx.ID_ANY, size=(200, 400), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i, text in enumerate(Text):
            self.fiscal_year_text.InsertColumn(i, text)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(title, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.fiscal_year_text, (1, 0), (1, 1), flag=wx.EXPAND)
        self.fiscal_year_panel.SetSizer(layout)
        self.fiscal_year_panel.Layout()

    def __by_title(self):
        title = wx.StaticText(self.by_title_panel, wx.ID_ANY, "タイトル別課金額")
        Text = (u'用途', u'金額')
        # 検索結果を表示するリストコントローラ
        self.by_title_panel_text = wx.ListCtrl(self.by_title_panel, wx.ID_ANY, size=(200, 380), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i, text in enumerate(Text):
            self.by_title_panel_text.InsertColumn(i, text)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(title, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.by_title_panel_text, (1, 0), (1, 1), flag=wx.EXPAND)
        self.by_title_panel.SetSizer(layout)
        self.by_title_panel.Layout()

    def __per_transaction(self):
        title = wx.StaticText(self.per_transaction_panel, wx.ID_ANY, "一回あたりの課金額")
        Text = (u'金額幅', u'回数')
        # 検索結果を表示するリストコントローラ
        self.per_transaction_text = wx.ListCtrl(self.per_transaction_panel, wx.ID_ANY, size=(200, 400), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i, text in enumerate(Text):
            self.per_transaction_text.InsertColumn(i, text)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(title, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.per_transaction_text, (1, 0), (1, 1), flag=wx.EXPAND)
        self.per_transaction_panel.SetSizer(layout)
        self.per_transaction_panel.Layout()

    def __year_add_listctrl_item(self):
        year = ['2012', '2013', '2014', '2015', '2016', '2017', '2018']
        money = [9000, 60475, 120800, 177930, 325200, 355090, 510340]
        # 追加する行の指定
        Add_line = self.fiscal_year_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(year)):
            # 行の追加を行う
            self.fiscal_year_text.InsertItem(Add_line, year[index])
            self.fiscal_year_text.SetItem(Add_line, 1, str(money[index]))
            Add_line += 1

    def __title_add_listctrl_item(self):
        year = ['デレステ', 'ガルパ', 'パズドラ', 'グラブル', 'クリプト', '神撃', '戦国アスカ', '歌マクロス', 'ホウチ', 'ファンキル', 'ドールズ', 'ゴマ乙', 'ハチナイ', 'キンスレ', 'その他', '音楽', 'シノアリス', 'シャドバ', 'LINE', 'アスタ']
        money = [584240, 325240, 144475, 131880, 72440, 60640, 50400, 46400, 45060, 18000, 17600, 16440, 13130, 10560, 6340, 5750, 3000, 2840, 2800, 1600]
        # 追加する行の指定
        Add_line = self.by_title_panel_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(year)):
            # 行の追加を行う
            self.by_title_panel_text.InsertItem(Add_line, year[index])
            self.by_title_panel_text.SetItem(Add_line, 1, str(money[index]))
            Add_line += 1

    def __per_add_listctrl_item(self):
        year = ['1-1000', '1001-2000', '2001-3000', '3001-4000', '4001-5000', '5001-6000', '6001-7000', '7001-8000', '8001-9000', '9001-10000', '10001-11000', '11001-12000', '12001-13000']
        money = [68, 45, 12, 11, 28, 24, 12, 0, 2, 100, 3, 1, 1]
        # 追加する行の指定
        Add_line = self.per_transaction_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(year)):
            # 行の追加を行う
            self.per_transaction_text.InsertItem(Add_line, year[index])
            self.per_transaction_text.SetItem(Add_line, 1, str(money[index]))
            Add_line += 1

    def adjust_search_info(self):
        """
        検索条件を取得し、リスト化して返却する

        Returns
        -------
        select_condition_list : list
            [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
        """
        select_condition_list = []
        select_condition_list.append(self.search_use.GetValue())
        select_condition_list.append(self.search_money_list[0].GetValue())
        select_condition_list.append(self.search_money_list[1].GetValue())
        select_condition_list.append(self.search_year_list[0].GetValue())
        select_condition_list.append(self.search_year_list[1].GetValue())
        select_condition_list.append(self.search_month_list[0].GetValue())
        select_condition_list.append(self.search_month_list[1].GetValue())
        select_condition_list.append(self.search_day_list[0].GetValue())
        select_condition_list.append(self.search_day_list[1].GetValue())
        return select_condition_list

    def call_select(self, event):
        # listctrlを初期化する
        self.search_result_text.DeleteAllItems()
        select_condition_list = self.adjust_search_info()
        self.all_data, all_money = accountingService.select_accounting(select_condition_list)

        # 追加する行の指定
        Add_line = self.search_result_text.GetItemCount()

        # 検索結果を行に追加する
        for items in self.all_data:
            # 行の追加を行う
            self.search_result_text.InsertItem(Add_line, str(items[0]))
            for item in range(1, len(items)):
                if item == 6 or item == 7:
                    # 作成日と更新日をYY/MM/DD HH:MM:SSに変換する
                    self.search_result_text.SetItem(Add_line, item, items[item].strftime('%Y/%m/%d %H:%M:%S'))
                else:
                    self.search_result_text.SetItem(Add_line, item, str(items[item]))
            Add_line += 1
        self.frame.SetStatusText(f'累計金額：{all_money:,}円です。')
        self.__year_add_listctrl_item()
        self.__title_add_listctrl_item()
        self.__per_add_listctrl_item()

    def call_sort(self, event):
        """
        検索結果をソート処理を呼び出す

        Parameters
        ----------
        event : event
            wxPythonのeventクラス
        """
        if self.all_data != []:
            if event.GetColumn() not in [1, 6, 7]:
                self.sort_item(event.GetColumn())

    def sort_item(self, col_number):
        """
        listctrlのitemをソートする

        Parameters
        ----------
        col_number : int
            listctrlの列番号

        """
        search_list = []
        # 現在のidの順番を把握する
        for i in range(self.search_result_text.GetItemCount()):
            search_list.append([i, int(self.search_result_text.GetItem(itemIdx=i, col=col_number).GetText())])
        searched_list = sorted(search_list, key=itemgetter(1))
        # ソート結果と、初期データ同じ場合、反転する
        if searched_list == search_list:
            searched_list = searched_list[::-1]
        # 既存のlistctrlの情報をすべて消す
        self.search_result_text.DeleteAllItems()
        # listctrlに情報を追加する
        self.add_listctrl_item(searched_list)
        self.all_data = []
        # 次のソートの時用にall_dataを作り直す
        for i in range(self.search_result_text.GetItemCount()):
            self.all_data_create(i)

    def all_data_create(self, col_number):
        """
        ソート後、all_dataを作成し直す

        Parameters
        ----------
        col_number : int or string
            列番号

        """
        self.all_data.append([])
        number = len(self.all_data)
        for j in range(self.search_result_text.GetColumnCount()):
            self.all_data[number - 1].append(self.search_result_text.GetItemText(col_number, col=j))

    def add_listctrl_item(self, search_list):
        """
        ソート後、listctrlに情報を挿入する

        Parameters
        ----------
        search_list : list型
            idが挿入されたリスト

        """
        # 追加する行の指定
        Add_line = self.search_result_text.GetItemCount()
        # 検索結果を行に追加する
        for date in search_list:
            # 行の追加を行う
            self.search_result_text.InsertItem(Add_line, str(self.all_data[date[0]][0]))
            for item in range(1, len(self.all_data[date[0]])):
                if item == 6 or item == 7:
                    # 作成日と更新日をYY/MM/DD HH:MM:SSに変換する
                    try:
                        self.search_result_text.SetItem(Add_line, item, self.all_data[date[0]][item].strftime('%Y/%m/%d %H:%M:%S'))
                    except:
                        self.search_result_text.SetItem(Add_line, item, str(self.all_data[date[0]][item]))
                else:
                    self.search_result_text.SetItem(Add_line, item, str(self.all_data[date[0]][item]))
            Add_line += 1

    def detail_open(self, event):
        """
        detailの画面を呼び出す

        Parameters
        ----------
        event : event
            wxPythonのeventクラス
        """
        # 選択されたindexを取得する
        index = event.GetIndex()

        # 用途から日までを取得し、リストに格納する
        detail_info_list = []
        # TODO: 用途などの題名テキストをリスト化し、作成、更新日外を長さとして持たせるように変更
        for i in range(6):
            item = self.search_result_text.GetItem(itemIdx=index, col=i)
            detail_info_list.append(item.GetText())

        # HACK: 未動作のためリファクタリングが必要
        select_condition_list = self.adjust_search_info()
        cacheService.update_cache(select_condition_list)
        self.frame.Destroy()
        wx.Exit()
        detail.call_detail(detail_info_list)


class GraphPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)


def call_search():
    app = wx.App(False)
    Search(None, wx.ID_ANY, title=u'CHMS | 検索')
    app.MainLoop()
