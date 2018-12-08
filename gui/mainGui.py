import wx
from . import registration
from . import search
from . import graph
from . import common

class Main(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(750,300))
        # icon設定
        self.SetIcon(common.get_icon())

        panel = MainPanel(self)
        self.Centre()
        self.Show()

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.myinit()

    def myinit(self):
        # 初期設定
        self.font = common.main_defalut_font_size()

        # ボタンを初期作成する
        self.button1 = wx.Button(self, wx.ID_ANY, u'登録', size=(200, 100))
        self.button2 = wx.Button(self, wx.ID_ANY, u'検索', size=(200, 100))
        self.button3 = wx.Button(self, wx.ID_ANY, u'グラフ', size=(200, 100))

        # ボタンにフォントサイズを適応する
        self.button1.SetFont(self.font)
        self.button2.SetFont(self.font)
        self.button3.SetFont(self.font)

        # ボタンにアクションを追加する
        self.button1.Bind(wx.EVT_BUTTON, self.click_button1)
        self.button2.Bind(wx.EVT_BUTTON, self.click_button2)
        self.button3.Bind(wx.EVT_BUTTON, self.click_button3)

        # レイアウト設定
        self.layout = wx.GridBagSizer(0, 0)
        self.layout.Add(self.button1, (4,0), (1,1), flag=wx.GROW | wx.LEFT | wx.TOP, border=30)
        self.layout.Add(self.button2, (4,1), (1,1), flag=wx.GROW | wx.LEFT | wx.TOP, border=30)
        self.layout.Add(self.button3, (4,2), (1,1), flag=wx.GROW | wx.LEFT | wx.TOP, border=30)

        self.SetSizer(self.layout)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def click_button1(self, event):
        """登録を呼び出す

        Parameters
        ----------
        event : クリックイベント
            クリックイベント

        """
        self.frame.Destroy()
        wx.Exit()
        registration.call_register()

    def click_button2(self, event):
        """登録を呼び出す

        Parameters
        ----------
        event : クリックイベント
            クリックイベント

        """
        self.frame.Destroy()
        wx.Exit()
        search.call_search()

    def click_button3(self, event):
        """グラフを呼び出す

        Parameters
        ----------
        event : クリックイベント
            クリックイベント

        """
        self.frame.Destroy()
        wx.Exit()
        graph.call_graph()

    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("image/chms.jpg")
        dc.DrawBitmap(bmp, 0, 0)

def call_mainGui():
    app = wx.App(False)
    Main(None, wx.ID_ANY, title=u'CHMS')
    app.MainLoop()