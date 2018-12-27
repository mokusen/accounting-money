import wx
from method.services import accountingService
from .. import common
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)


class MonthPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.search_notebook = parent
        self.__myinit()

    def __myinit(self):
        self.title = wx.StaticText(self, wx.ID_ANY, "月別課金額")
        # 検索結果を表示するリストコントローラ
        ctrl_size = common.statistics_data_ctrl_size()
        self.fiscal_month_text = wx.ListCtrl(self, wx.ID_ANY, size=ctrl_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.fiscal_month_text.InsertColumn(0, u'月', wx.LIST_FORMAT_LEFT, 90)
        self.fiscal_month_text.InsertColumn(1, u'金額', wx.LIST_FORMAT_RIGHT, 90)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.title, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.fiscal_month_text, (1, 0), (1, 1), flag=wx.EXPAND)
        self.SetSizer(layout)
        self.Layout()

    def month_add_listctrl_item(self, year_accounting_list, year):
        self.fiscal_month_text.DeleteAllItems()
        self.title.SetLabel(f"{year}年：月別課金額")
        month = [year_accounting[2] for year_accounting in year_accounting_list if year_accounting[0] == int(year)]
        money = [year_accounting[1] for year_accounting in year_accounting_list if year_accounting[0] == int(year)]
        # 追加する行の指定
        Add_line = self.fiscal_month_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(month)):
            # 行の追加を行う
            self.fiscal_month_text.InsertItem(Add_line, str(month[index]))
            self.fiscal_month_text.SetItem(Add_line, 1, f"{money[index]:,}")
            Add_line += 1
        # 累計結果を追加する
        self.fiscal_month_text.InsertItem(Add_line, "累計")
        self.fiscal_month_text.SetItem(Add_line, 1, f"{sum(money):,}")

    def month_reset_listctrl(self):
        self.fiscal_month_text.DeleteAllItems()
        self.title.SetLabel("月別課金額")
