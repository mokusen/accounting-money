import wx
from method.services import accountingService
from .. import common
from method.utils import chms_logger


logger = chms_logger.set_operate_logger(__name__)


class UsePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.__myinit()

    def __myinit(self):
        # 検索結果を表示するリストコントローラ
        ctrl_size = common.statistics_ctrl_size()
        self.by_use_panel_text = wx.ListCtrl(self, wx.ID_ANY, size=ctrl_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.by_use_panel_text.InsertColumn(0, u'用途', wx.LIST_FORMAT_LEFT, 90)
        self.by_use_panel_text.InsertColumn(1, u'金額', wx.LIST_FORMAT_RIGHT, 80)
        box = wx.StaticBox(self, wx.ID_ANY, '用途別金額')
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.by_use_panel_text, (0, 0), (1, 1), flag=wx.EXPAND)
        mylayout = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        mylayout.Add(layout)
        self.SetSizer(mylayout)
        self.Layout()

    def use_add_listctrl_item(self, use_accounting_list):
        """
        用途別課金額をlistctrlに追加する
        Parameters
        ----------
        use_accounting_list : list in tuple
            [('use', money), (...)]
        """
        self.by_use_panel_text.DeleteAllItems()
        use = [use_accounting[0] for use_accounting in use_accounting_list]
        money = [use_accounting[1] for use_accounting in use_accounting_list]
        # 追加する行の指定
        Add_line = self.by_use_panel_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(use)):
            # 行の追加を行う
            self.by_use_panel_text.InsertItem(Add_line, str(use[index]))
            self.by_use_panel_text.SetItem(Add_line, 1, f"{money[index]:,}")
            Add_line += 1
