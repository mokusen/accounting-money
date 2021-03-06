import wx
from method.services import accountingService
from .. import common
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)


class MonthPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.__myinit()

    def __myinit(self):
        # 検索結果を表示するリストコントローラ
        ctrl_size = common.statistics_data_ctrl_size()
        self.fiscal_month_text = wx.ListCtrl(self, wx.ID_ANY, size=ctrl_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.fiscal_month_text.InsertColumn(0, u'月', wx.LIST_FORMAT_LEFT, 90)
        self.fiscal_month_text.InsertColumn(1, u'金額', wx.LIST_FORMAT_RIGHT, 80)
        self.box = wx.StaticBox(self, wx.ID_ANY, '月別課金額')
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.fiscal_month_text, (0, 0), (1, 1), flag=wx.EXPAND)
        mylayout = wx.StaticBoxSizer(self.box, wx.HORIZONTAL)
        mylayout.Add(layout)
        self.SetSizer(mylayout)
        self.Layout()

    def month_add_listctrl_item(self, year_accounting_list, year):
        """
        月別課金額のlistctrlに追加する
        Parameters
        ----------
        year_accounting_list : list in tuple
            [(year, money, month), (), ...]
        year : str
            検索対象の年度
        """
        self.fiscal_month_text.DeleteAllItems()
        self.box.SetLabel(f"{year}年：月別課金額")
        if year == "累計":
            month = [m for m in range(1, 13)]
            dict_money = {m: 0 for m in month}
            for index in range(len(year_accounting_list)):
                dict_money[year_accounting_list[index][2]] += int(year_accounting_list[index][1])
            money = [dict_money[m] for m in month]
        else:
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
        self.box.SetLabel("月別課金額")
