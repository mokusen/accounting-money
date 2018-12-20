import wx
from . import mainGui, common, mainGraphNote


class Graph(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500, 500))
        self.SetIcon(common.get_icon())
        MainPanel(self)
        self.Bind(wx.EVT_CLOSE, self.frame_close)
        self.Centre()
        self.Show()

    def frame_close(self, event):
        self.Destroy()


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.__myinit()

    def __myinit(self):
        self.graphNote = mainGraphNote.GraphNotePanel(self)
        # レイアウト設定
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.graphNote, flag=wx.EXPAND)
        self.SetSizer(layout)


def call_graph():
    Graph(None, wx.ID_ANY, title=u'CHMS | グラフ')
