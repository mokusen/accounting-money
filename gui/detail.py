import wx
import datetime
from utils import useListCreate, dataListCreate
from . import search

class Detail(wx.Frame):
    def __init__(self, parent, id, title, detail_info_list):
        self.frame_size = (675,600)
        wx.Frame.__init__(self, parent, id, title, size=(300,300))
        # 設定
        self.detail_info_list = detail_info_list

        # 要素の作成
        self.myinit()

        # 閉じるイベント
        self.Bind(wx.EVT_CLOSE, self.frame_close)

        self.Centre()
        self.Show()

    def myinit(self):
        self.panel = wx.Panel(self, wx.ID_ANY, size=self.frame_size)
        use_list = useListCreate.create_list()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()
        form_size = (100,25)
        text_size = (50,25)
        button_size = (100,25)

        # 修正フォームのラベル作成
        text_id = wx.StaticText(self.panel, wx.ID_ANY, 'ID', size=text_size, style=wx.TE_CENTER)
        text_use = wx.StaticText(self.panel, wx.ID_ANY, '用途', size=text_size, style=wx.TE_CENTER)
        text_money = wx.StaticText(self.panel, wx.ID_ANY, '金額', size=text_size, style=wx.TE_CENTER)
        text_year = wx.StaticText(self.panel, wx.ID_ANY, '年', size=text_size, style=wx.TE_CENTER)
        text_month = wx.StaticText(self.panel, wx.ID_ANY, '月', size=text_size, style=wx.TE_CENTER)
        text_day = wx.StaticText(self.panel, wx.ID_ANY, '日', size=text_size, style=wx.TE_CENTER)

        # 修正フォーム作成
        detail_id = wx.StaticText(self.panel, wx.ID_ANY, self.detail_info_list[0], size=form_size, style=wx.TE_CENTER)
        detail_use = wx.ComboBox(self.panel, wx.ID_ANY, value=self.detail_info_list[1], choices=use_list, style=wx.CB_DROPDOWN, size=form_size)
        detail_money = wx.TextCtrl(self.panel, wx.ID_ANY, value=self.detail_info_list[2],size=form_size)
        detail_year = wx.TextCtrl(self.panel, wx.ID_ANY, value=self.detail_info_list[3],size=form_size)
        detail_month_ = wx.ComboBox(self.panel, wx.ID_ANY, value=self.detail_info_list[4],choices=month_list, style=wx.CB_DROPDOWN, size=form_size)
        detail_day_ = wx.ComboBox(self.panel, wx.ID_ANY, value=self.detail_info_list[5],choices=day_list, style=wx.CB_DROPDOWN, size=form_size)

        # 更新、削除ボタン
        update_button = wx.Button(self.panel, wx.ID_ANY, '更新', size=button_size)
        delete_button = wx.Button(self.panel, wx.ID_ANY, '削除', size=button_size)

        # 更新、削除ボタンにイベントを登録する
        update_button.Bind(wx.EVT_BUTTON, self.call_update)
        delete_button.Bind(wx.EVT_BUTTON, self.call_delete)

        # レイアウト設定
        detail_layout = wx.GridBagSizer(10, 5)
        detail_layout.Add(text_id, (0, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(text_use, (1, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(text_money, (2, 0), (1,1), flag=wx.EXPAND)
        detail_layout.Add(text_year, (3, 0), (1,1), flag=wx.EXPAND)
        detail_layout.Add(text_month, (4, 0), (1,1), flag=wx.EXPAND)
        detail_layout.Add(text_day, (5, 0), (1,1), flag=wx.EXPAND)
        detail_layout.Add(detail_id, (0, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(detail_use, (1, 1), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(detail_money, (2, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(detail_year, (3, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(detail_month_, (4, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(detail_day_, (5, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(update_button, (1, 2), (2,1), flag=wx.EXPAND)
        detail_layout.Add(delete_button, (4, 2), (2,1), flag=wx.EXPAND)

        # 全体レイアウト
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(detail_layout, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        self.panel.SetSizer(layout)

    def call_update(self, event):
        # TODO update
        print("test")

    def call_delete(self, event):
        # TODO update
        print("test")

    def frame_close(self, event):
        self.Destroy()
        wx.Exit()

def call_detail(detail_info_list):
    app = wx.App(False)
    Detail(None, wx.ID_ANY, title=u'BRS', detail_info_list=detail_info_list)
    app.MainLoop()