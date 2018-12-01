import wx
from . import registration
from . import search
from . import graph

class Main(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(750,200))
        self.myinit()
        self.Centre()
        self.Show()

    def myinit(self):
        # 表示するためのパネル生成
        self.panel = wx.Panel(self, wx.ID_ANY, size=(750,200))

        # ボタンを初期作成する
        self.button1 = wx.Button(self.panel, wx.ID_ANY, u'登録', size=(200, 100))
        self.button2 = wx.Button(self.panel, wx.ID_ANY, u'検索', size=(200, 100))
        self.button3 = wx.Button(self.panel, wx.ID_ANY, u'グラフ', size=(200, 100))

        # ボタンにアクションを追加する
        self.button1.Bind(wx.EVT_BUTTON, self.click_button1)
        self.button2.Bind(wx.EVT_BUTTON, self.click_button2)
        self.button3.Bind(wx.EVT_BUTTON, self.click_button3)

        self.layout = wx.GridBagSizer(3, 0)
        self.layout.Add(self.button1, (0,0), (1,1), flag=wx.GROW | wx.LEFT | wx.TOP, border=30)
        self.layout.Add(self.button2, (0,1), (1,1), flag=wx.GROW | wx.LEFT | wx.TOP, border=30)
        self.layout.Add(self.button3, (0,2), (1,1), flag=wx.GROW | wx.LEFT | wx.TOP, border=30)

        self.panel.SetSizer(self.layout)

    def click_button1(self, event):
        """登録を呼び出す

        Parameters
        ----------
        event : クリックイベント
            クリックイベント

        """
        self.Destroy()
        wx.Exit()
        registration.call_register()

    def click_button2(self, event):
        """登録を呼び出す

        Parameters
        ----------
        event : クリックイベント
            クリックイベント

        """
        self.Destroy()
        wx.Exit()
        search.call_search()

    def click_button3(self, event):
        """グラフを呼び出す

        Parameters
        ----------
        event : クリックイベント
            クリックイベント

        """
        self.Destroy()
        wx.Exit()
        graph.call_graph()

def call_mainGui():
    app = wx.App(False)
    Main(None, wx.ID_ANY, title=u'BRS')
    app.MainLoop()