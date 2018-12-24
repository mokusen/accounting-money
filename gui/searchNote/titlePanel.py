import wx
from services import accountingService
from .. import common
from utils import logger


logger = logger.set_operate_logger(__name__)


class TitlePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.__myinit()

    def __myinit(self):
        title = wx.StaticText(self, wx.ID_ANY, "用途別金額")
        # 検索結果を表示するリストコントローラ
        ctrl_size = common.statistics_ctrl_size()
        self.by_title_panel_text = wx.ListCtrl(self, wx.ID_ANY, size=ctrl_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.by_title_panel_text.InsertColumn(0, u'用途', wx.LIST_FORMAT_LEFT, 90)
        self.by_title_panel_text.InsertColumn(1, u'金額', wx.LIST_FORMAT_RIGHT, 90)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(title, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.by_title_panel_text, (1, 0), (1, 1), flag=wx.EXPAND)
        self.SetSizer(layout)
        self.Layout()

    def title_add_listctrl_item(self, title_accounting_list):
        self.by_title_panel_text.DeleteAllItems()
        use = [title_accounting[0] for title_accounting in title_accounting_list]
        money = [title_accounting[1] for title_accounting in title_accounting_list]
        # 追加する行の指定
        Add_line = self.by_title_panel_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(use)):
            # 行の追加を行う
            self.by_title_panel_text.InsertItem(Add_line, str(use[index]))
            self.by_title_panel_text.SetItem(Add_line, 1, f"{money[index]:,}")
            Add_line += 1
