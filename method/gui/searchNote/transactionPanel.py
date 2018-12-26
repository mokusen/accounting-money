import wx
from method.services import accountingService
from .. import common
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)


class TransactionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.__myinit()

    def __myinit(self):
        title = wx.StaticText(self, wx.ID_ANY, "一回あたりの課金額")
        Text = (u'金額幅', u'回数')
        # 検索結果を表示するリストコントローラ
        ctrl_size = common.statistics_ctrl_size()
        self.per_transaction_text = wx.ListCtrl(self, wx.ID_ANY, size=ctrl_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.per_transaction_text.InsertColumn(0, u'金額幅', wx.LIST_FORMAT_LEFT, 90)
        self.per_transaction_text.InsertColumn(1, u'回数', wx.LIST_FORMAT_RIGHT, 90)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(title, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.per_transaction_text, (1, 0), (1, 1), flag=wx.EXPAND)
        self.SetSizer(layout)
        self.Layout()

    def per_add_listctrl_item(self, search_money_list, transaction_accounting_list):
        self.per_transaction_text.DeleteAllItems()
        accounting_count = transaction_accounting_list[0]
        # 追加する行の指定
        Add_line = self.per_transaction_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(accounting_count)):
            # 行の追加を行う
            self.per_transaction_text.InsertItem(Add_line, f'{search_money_list[index]}～{search_money_list[index+1]}')
            self.per_transaction_text.SetItem(Add_line, 1, f'{accounting_count[index]:,}')
            Add_line += 1
