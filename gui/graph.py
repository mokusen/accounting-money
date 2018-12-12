import wx
from . import mainGui, common


class Graph(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500, 500))

        # icon設定
        self.SetIcon(common.get_icon())

        # 閉じるイベント
        self.Bind(wx.EVT_CLOSE, self.frame_close)

        self.Centre()
        self.Show()

    def frame_close(self, event):
        self.Destroy()
        wx.Exit()
        mainGui.call_mainGui()


def call_graph():
    app = wx.App(False)
    Graph(None, wx.ID_ANY, title=u'CHMS | グラフ')
    app.MainLoop()
