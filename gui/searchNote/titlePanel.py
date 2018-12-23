import wx
from services import accountingService
from utils import logger

logger = logger.set_operate_logger(__name__)


class TitlePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.__myinit()

    def __myinit(self):
        title = wx.StaticText(self, wx.ID_ANY, "用途別金額")
        Text = (u'用途', u'金額')
        # 検索結果を表示するリストコントローラ
        self.by_title_panel_text = wx.ListCtrl(self, wx.ID_ANY, size=(200, 380), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i, text in enumerate(Text):
            self.by_title_panel_text.InsertColumn(i, text)
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
            self.by_title_panel_text.SetItem(Add_line, 1, str(money[index]))
            Add_line += 1
