import wx
from . import mainGui
from services import search

class Graph(wx.Frame):
    def __init__(self, parent, id, title):
        self.frame_size = (615,600)
        wx.Frame.__init__(self, parent, id, title, size=self.frame_size)
        self.myinit()

        # 閉じるイベント
        self.Bind(wx.EVT_CLOSE, self.frame_close)

        self.Centre()
        self.Show()

    def myinit(self):
        self.panel = wx.Panel(self, wx.ID_ANY, size=self.frame_size)
        Text = (u'金額', u'用途', u'年', u'月', u'日', u'作成日', u'更新日')
        search_result_text = wx.ListCtrl(self.panel, wx.ID_ANY, size=self.frame_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i, text in enumerate(Text):
            search_result_text.InsertColumn(i, text)

        # Textの幅を個別設定する
        search_result_text.SetColumnWidth(0, 80)
        search_result_text.SetColumnWidth(1, 60)
        search_result_text.SetColumnWidth(2, 60)
        search_result_text.SetColumnWidth(3, 40)
        search_result_text.SetColumnWidth(4, 40)
        search_result_text.SetColumnWidth(5, 150)
        search_result_text.SetColumnWidth(6, 150)

        # 全件データ取得
        all_data = search.all_search()
        Add_line = search_result_text.GetItemCount()
        for index, items in enumerate(all_data):
            search_result_text.InsertItem(Add_line, str(items[0]))
            for item in range(1, len(items)):
                if item == 5 or item == 6:
                    # 作成日と更新日をYY/MM/DD HH:MM:SSに変換する
                    search_result_text.SetItem(Add_line, item, str(items[item].strftime('%Y/%m/%d %H:%M:%S')))
                else:
                    search_result_text.SetItem(Add_line, item, str(items[item]))
            Add_line += 1
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(search_result_text, flag=wx.EXPAND)
        self.panel.SetSizer(layout)

    def frame_close(self, event):
        self.Destroy()
        wx.Exit()
        mainGui.call_mainGui()

def call_search():
    app = wx.App(False)
    Graph(None, wx.ID_ANY, title=u'BRS')
    app.MainLoop()