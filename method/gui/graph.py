import wx
from . import mainGui, common, mainGraphNote
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)


class Graph(wx.Frame):
    def __init__(self, parent, id, title, statistics_info_dict):
        frame_size = common.graph_frame_size()
        use_display_size = common.graph_use_display_size()
        wx.Frame.__init__(self, parent, id, title, size=frame_size, pos=use_display_size)
        self.SetIcon(common.get_icon())
        MainPanel(self, statistics_info_dict)
        self.Bind(wx.EVT_CLOSE, self.frame_close)
        self.Show()

    def frame_close(self, event):
        self.Destroy()

    def frame_close_oparate(self):
        self.Destroy()


class MainPanel(wx.Panel):
    def __init__(self, parent, statistics_info_dict):
        wx.Panel.__init__(self, parent=parent)
        self.graphNote = mainGraphNote.GraphNotePanel(self, statistics_info_dict)
        self.__myinit()

    def __myinit(self):
        # レイアウト設定
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.graphNote, flag=wx.EXPAND)
        self.SetSizer(layout)


def call_graph(statistics_info_dict):
    logger.info("START Graph")
    graph = Graph(None, wx.ID_ANY, title=u'CHMS | グラフ', statistics_info_dict=statistics_info_dict)
    return graph
