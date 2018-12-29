import wx
from method.services import accountingService
from .. import common
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)


class YearPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.__myinit()

    def __myinit(self):
        # 検索結果を表示するリストコントローラ
        ctrl_size = common.statistics_data_ctrl_size()
        self.fiscal_year_text = wx.ListCtrl(self, wx.ID_ANY, size=ctrl_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.fiscal_year_text.InsertColumn(0, u'年', wx.LIST_FORMAT_LEFT, 90)
        self.fiscal_year_text.InsertColumn(1, u'金額', wx.LIST_FORMAT_RIGHT, 80)
        box = wx.StaticBox(self, wx.ID_ANY, '年度別課金額')
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.fiscal_year_text, (0, 0), (1, 1), flag=wx.EXPAND)
        mylayout = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        mylayout.Add(layout)
        self.SetSizer(mylayout)
        self.Layout()

    def year_add_listctrl_item(self, year_accounting_list):
        """
        年度別課金額のlistctrlに追加する
        Parameters
        ----------
        year_accounting_list : list in tuple
            [(year, money, month), (), ...]
        """
        self.fiscal_year_text.DeleteAllItems()
        year = [year_accounting[0] for year_accounting in year_accounting_list]
        money = [year_accounting[1] for year_accounting in year_accounting_list]
        year_list = sorted(list(set([year_accounting[0] for year_accounting in year_accounting_list])))
        dict_money = {year: 0 for year in year_list}
        for index in range(len(year_accounting_list)):
            dict_money[year_accounting_list[index][0]] += int(year_accounting_list[index][1])
        money_list = [dict_money[years] for years in year_list]
        # 追加する行の指定
        Add_line = self.fiscal_year_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(year_list)):
            # 行の追加を行う
            self.fiscal_year_text.InsertItem(Add_line, str(year_list[index]))
            self.fiscal_year_text.SetItem(Add_line, 1, f"{money_list[index]:,}")
            Add_line += 1
        # 累計結果を追加する
        self.fiscal_year_text.InsertItem(Add_line, "累計")
        self.fiscal_year_text.SetItem(Add_line, 1, f"{sum(money_list):,}")
