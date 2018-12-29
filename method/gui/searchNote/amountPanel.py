import wx
from method.services import accountingService
from .. import common
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)


class AmountPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.__myinit()

    def __myinit(self):
        # 検索結果を表示するリストコントローラ
        ctrl_size = common.statistics_ctrl_size()
        self.per_amonut_text = wx.ListCtrl(self, wx.ID_ANY, size=ctrl_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.per_amonut_text.InsertColumn(0, u'金額幅', wx.LIST_FORMAT_LEFT, 90)
        self.per_amonut_text.InsertColumn(1, u'回数', wx.LIST_FORMAT_RIGHT, 80)
        box = wx.StaticBox(self, wx.ID_ANY, '一回あたりの課金額')
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.per_amonut_text, (0, 0), (1, 1), flag=wx.EXPAND)
        mylayout = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        mylayout.Add(layout)
        self.SetSizer(mylayout)
        self.Layout()

    def amount_add_listctrl_item(self, search_money_list, amount_accounting_list):
        """
        課金額毎回数のlistctrlに追加する
        Parameters
        ----------
        search_money_list : list
            [0, 1000, 2000, ...]
        amount_accounting_list : list in tuple
            [(count of 0, count of 1000, count of 2000, ...)]
        """
        self.per_amonut_text.DeleteAllItems()
        accounting_count = amount_accounting_list[0]
        # 追加する行の指定
        Add_line = self.per_amonut_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(accounting_count)):
            # 行の追加を行う
            self.per_amonut_text.InsertItem(Add_line, f'{search_money_list[index]}～{search_money_list[index+1]}')
            self.per_amonut_text.SetItem(Add_line, 1, f'{accounting_count[index]:,}')
            Add_line += 1
