import wx
from . import mainGui, detail, common
from utils import useListCreate, dataListCreate
from services import search

class Search(wx.Frame):
    def __init__(self, parent, id, title):
        self.frame_size = (675,600)
        wx.Frame.__init__(self, parent, id, title, size=self.frame_size)

        # icon設定
        self.SetIcon(common.get_icon())

        # 要素の作成
        self.myinit()

        # ステータスバー作成
        self.CreateStatusBar()

        # 詳細ページ表示イベント
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.detail_open)

        # 閉じるイベント
        self.Bind(wx.EVT_CLOSE, self.frame_close)

        self.Centre()
        self.Show()

    def myinit(self):
        self.panel = wx.Panel(self, wx.ID_ANY, size=self.frame_size)
        # 初期設定
        self.input_defalut_text = "選択"
        Text = (u'ID', u'用途', u'金額', u'年', u'月', u'日', u'作成日', u'更新日')
        use_list = useListCreate.create_list()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()

        # 初期値追加
        use_list.insert(0,'')

        # size設定
        form_size = (100,25)
        text_size = (50,25)

        # font設定
        self.font = common.defalut_font_size()

        # 検索結果を表示するリストコントローラ
        self.search_result_text = wx.ListCtrl(self.panel, wx.ID_ANY, size=self.frame_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_EDIT_LABELS)
        for i, text in enumerate(Text):
            self.search_result_text.InsertColumn(i, text)

        # Textの幅を個別設定する
        width_list = [0, 80, 70, 70, 60, 60, 150, 150]
        for index, width in enumerate(width_list):
            self.search_result_text.SetColumnWidth(index, width)

        # 検索フォームのラベル作成
        text_use = wx.StaticText(self.panel, wx.ID_ANY, '用途', size=text_size, style=wx.TE_CENTER)
        text_money = wx.StaticText(self.panel, wx.ID_ANY, '金額', size=text_size, style=wx.TE_CENTER)
        text_year = wx.StaticText(self.panel, wx.ID_ANY, '年', size=text_size, style=wx.TE_CENTER)
        text_month = wx.StaticText(self.panel, wx.ID_ANY, '月', size=text_size, style=wx.TE_CENTER)
        text_day = wx.StaticText(self.panel, wx.ID_ANY, '日', size=text_size, style=wx.TE_CENTER)

        # 検索フォームのラベルフォント設定
        text_use.SetFont(self.font)
        text_money.SetFont(self.font)
        text_year.SetFont(self.font)
        text_month.SetFont(self.font)
        text_day.SetFont(self.font)

        # 検索フォーム作成
        self.search_use = wx.ComboBox(self.panel, wx.ID_ANY, self.input_defalut_text, choices=use_list, style=wx.CB_READONLY, size=form_size)
        self.search_money_list = []
        self.search_year_list = []
        self.search_month_list = []
        self.search_day_list = []

        # タブの進行方向設定のため、分けて行う
        for i in range(2):
            self.search_money_list.append(wx.TextCtrl(self.panel, wx.ID_ANY, size=form_size))
        for i in range(2):
            self.search_year_list.append(wx.TextCtrl(self.panel, wx.ID_ANY, size=form_size))
        for i in range(2):
            self.search_month_list.append(wx.ComboBox(self.panel, wx.ID_ANY, choices=month_list, style=wx.CB_READONLY, size=form_size))
        for i in range(2):
            self.search_day_list.append(wx.ComboBox(self.panel, wx.ID_ANY, choices=day_list, style=wx.CB_READONLY, size=form_size))

        # ~を作成する
        text_tilde_list = []
        for i in range(4):
            text_tilde_list.append(wx.StaticText(self.panel, wx.ID_ANY, '～', size=(25,25), style=wx.TE_CENTER))

        # 検索ボタン
        search_button = wx.Button(self.panel, wx.ID_ANY, '検索')

        # 検索ボタンにイベントを登録する
        search_button.Bind(wx.EVT_BUTTON, self.call_select)

        # 検索フォームのレイアウト設定
        search_layout = wx.GridBagSizer(10, 5)
        search_layout.Add(text_use, (0, 0), (1, 1), flag=wx.EXPAND)
        search_layout.Add(self.search_use, (0, 1), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_money, (1, 0), (1,1), flag=wx.EXPAND)
        search_layout.Add(text_year, (0, 4), (1,1), flag=wx.EXPAND)
        search_layout.Add(text_month, (1, 4), (1,1), flag=wx.EXPAND)
        search_layout.Add(text_day, (2, 4), (1,1), flag=wx.EXPAND)
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
        layout.Add(self.search_result_text, flag=wx.EXPAND)

        # ソートイベントを登録する
        self.panel.Bind(wx.EVT_LIST_COL_CLICK, self.call_sort)

        self.panel.SetSizer(layout)

    def adjust_search_info(self):
        use_value = self.search_use.GetValue()
        money_value_1 = self.search_money_list[0].GetValue()
        money_value_2 = self.search_money_list[1].GetValue()
        year_value_1 = self.search_year_list[0].GetValue()
        year_value_2 = self.search_year_list[1].GetValue()
        month_value_1 = self.search_month_list[0].GetValue()
        month_value_2 = self.search_month_list[1].GetValue()
        day_value_1 = self.search_day_list[0].GetValue()
        day_value_2 = self.search_day_list[1].GetValue()
        return use_value,money_value_1,money_value_2,year_value_1,year_value_2,month_value_1,month_value_2,day_value_1,day_value_2

    def call_select(self, event):
        # 初期化する
        self.search_result_text.DeleteAllItems()

        # 検索ワード取得
        use_value,money_value_1,money_value_2,year_value_1,year_value_2,month_value_1,month_value_2,day_value_1,day_value_2 = self.adjust_search_info()

        # 検索結果取得
        all_data, all_money = search.search_accounting(use_value,money_value_1,money_value_2,year_value_1,year_value_2,month_value_1,month_value_2,day_value_1,day_value_2)

        # 追加する行の指定
        Add_line = self.search_result_text.GetItemCount()

        # 検索結果を行に追加する
        for index, items in enumerate(all_data):
            # 行の追加を行う
            self.search_result_text.InsertItem(Add_line, str(items[0]))
            for item in range(1, len(items)):
                if item == 6 or item == 7:
                    # 作成日と更新日をYY/MM/DD HH:MM:SSに変換する
                    self.search_result_text.SetItem(Add_line, item, str(items[item].strftime('%Y/%m/%d %H:%M:%S')))
                else:
                    self.search_result_text.SetItem(Add_line, item, str(items[item]))
            Add_line += 1

        # 累計金額をステータスバーに表示する
        self.SetStatusText(f'累計金額：{all_money:,}円です。')

    def call_sort(self, event):
        idx = event.GetIndex()


    def detail_open(self, event):
        # 選択されたindexを取得する
        index = event.GetIndex()

        # 用途から日までを取得し、リストに格納する
        detail_info_list = []
        for i in range(6):
            item = self.search_result_text.GetItem(itemIdx=index, col=i)
            detail_info_list.append(item.GetText())
        self.Destroy()
        wx.Exit()
        detail.call_detail(detail_info_list)

    def frame_close(self, event):
        self.Destroy()
        wx.Exit()
        mainGui.call_mainGui()

def call_search():
    app = wx.App(False)
    Search(None, wx.ID_ANY, title=u'CHMS | 検索')
    app.MainLoop()