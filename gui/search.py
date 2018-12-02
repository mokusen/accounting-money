import wx
from . import mainGui
from utils import useListCreate, dataListCreate
from services import search

class Graph(wx.Frame):
    def __init__(self, parent, id, title):
        self.frame_size = (675,600)
        wx.Frame.__init__(self, parent, id, title, size=self.frame_size)
        self.myinit()

        # 閉じるイベント
        self.Bind(wx.EVT_CLOSE, self.frame_close)

        self.Centre()
        self.Show()

    def myinit(self):
        self.panel = wx.Panel(self, wx.ID_ANY, size=self.frame_size)
        # 初期設定
        self.input_defalut_text = "選択"
        Text = (u'用途', u'金額', u'年', u'月', u'日', u'作成日', u'更新日')
        use_list = useListCreate.create_list()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()
        self.search_result_text = wx.ListCtrl(self.panel, wx.ID_ANY, size=self.frame_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i, text in enumerate(Text):
            self.search_result_text.InsertColumn(i, text)
        size = (100,25)

        # Textの幅を個別設定する
        self.search_result_text.SetColumnWidth(0, 80)
        self.search_result_text.SetColumnWidth(1, 70)
        self.search_result_text.SetColumnWidth(2, 70)
        self.search_result_text.SetColumnWidth(3, 60)
        self.search_result_text.SetColumnWidth(4, 60)
        self.search_result_text.SetColumnWidth(5, 150)
        self.search_result_text.SetColumnWidth(6, 150)

        # 検索フォームのラベル作成
        text_use = wx.StaticText(self.panel, wx.ID_ANY, '用途', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        text_money = wx.StaticText(self.panel, wx.ID_ANY, '金額', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        text_year = wx.StaticText(self.panel, wx.ID_ANY, '年', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        text_month = wx.StaticText(self.panel, wx.ID_ANY, '月', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        text_day = wx.StaticText(self.panel, wx.ID_ANY, '日', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)

        # 検索フォーム作成
        search_use = wx.ComboBox(self.panel, wx.ID_ANY, self.input_defalut_text, choices=use_list, style=wx.CB_DROPDOWN, size=size)
        search_money_list = []
        search_year_list = []
        search_month_list = []
        search_day_list = []
        for i in range(2):
            search_money_list.append(wx.TextCtrl(self.panel, wx.ID_ANY, size=size))
            search_year_list.append(wx.TextCtrl(self.panel, wx.ID_ANY, size=size))
            search_month_list.append(wx.ComboBox(self.panel, wx.ID_ANY, choices=month_list, style=wx.CB_DROPDOWN, size=size))
            search_day_list.append(wx.ComboBox(self.panel, wx.ID_ANY, choices=day_list, style=wx.CB_DROPDOWN, size=size))

        # ~を作成する
        text_tilde_list = []
        for i in range(4):
            text_tilde_list.append(wx.StaticText(self.panel, wx.ID_ANY, '~', size=(25,25), style=wx.TE_CENTER))

        # 検索ボタン
        search_button = wx.Button(self.panel, wx.ID_ANY, '検索')

        # 検索ボタンにイベントを登録する
        search_button.Bind(wx.EVT_BUTTON, self.call_select)

        # 検索フォームのレイアウト設定
        search_layout = wx.GridBagSizer(0,0)
        search_layout.Add(text_use, (0, 0), (1, 1), flag=wx.EXPAND)
        search_layout.Add(search_use, (0, 1), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_money, (1, 0), (1,1), flag=wx.EXPAND)
        search_layout.Add(text_year, (0, 4), (1,1), flag=wx.EXPAND)
        search_layout.Add(text_month, (1, 4), (1,1), flag=wx.EXPAND)
        search_layout.Add(text_day, (2, 4), (1,1), flag=wx.EXPAND)
        for i in range(2):
            search_layout.Add(search_money_list[i], (1, 1 + i*2), (1, 1), flag=wx.EXPAND)
            search_layout.Add(search_year_list[i], (0, 5 + i*2), (1, 1), flag=wx.EXPAND)
            search_layout.Add(search_month_list[i], (1, 5 + i*2), (1, 1), flag=wx.EXPAND)
            search_layout.Add(search_day_list[i], (2, 5 + i*2), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_tilde_list[0], (1, 2), (1, 1), flag=wx.EXPAND)
        for i in range(3):
            search_layout.Add(text_tilde_list[i+1], (i, 6), (1, 1), flag=wx.EXPAND)
        search_layout.Add(search_button, (2, 1), (1, 3), flag=wx.EXPAND)

        # レイアウト設定
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(search_layout, flag=wx.EXPAND)
        layout.Add(self.search_result_text, flag=wx.EXPAND)
        self.panel.SetSizer(layout)

    def call_select(self, event):
        # 全件データ取得
        all_data = search.all_search()
        Add_line = self.search_result_text.GetItemCount()
        for index, items in enumerate(all_data):
            self.search_result_text.InsertItem(Add_line, str(items[0]))
            for item in range(1, len(items)):
                if item == 5 or item == 6:
                    # 作成日と更新日をYY/MM/DD HH:MM:SSに変換する
                    self.search_result_text.SetItem(Add_line, item, str(items[item].strftime('%Y/%m/%d %H:%M:%S')))
                else:
                    self.search_result_text.SetItem(Add_line, item, str(items[item]))
            Add_line += 1

    def frame_close(self, event):
        self.Destroy()
        wx.Exit()
        mainGui.call_mainGui()

def call_search():
    app = wx.App(False)
    Graph(None, wx.ID_ANY, title=u'BRS')
    app.MainLoop()