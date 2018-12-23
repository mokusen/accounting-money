import wx
from services import accountingService


class YearPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.search_notebook = parent
        self.__myinit()

    def __myinit(self):
        title = wx.StaticText(self, wx.ID_ANY, "年度別課金額")
        Text = (u'年', u'金額')
        # 検索結果を表示するリストコントローラ
        self.fiscal_year_text = wx.ListCtrl(self, wx.ID_ANY, size=(200, 400), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i, text in enumerate(Text):
            self.fiscal_year_text.InsertColumn(i, text)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(title, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.fiscal_year_text, (1, 0), (1, 1), flag=wx.EXPAND)
        self.SetSizer(layout)
        self.Layout()

    def year_add_listctrl_item(self, year_accounting_list):
        self.fiscal_year_text.DeleteAllItems()
        year = [year_accounting[0] for year_accounting in year_accounting_list]
        money = [year_accounting[1] for year_accounting in year_accounting_list]
        # 追加する行の指定
        Add_line = self.fiscal_year_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(year)):
            # 行の追加を行う
            self.fiscal_year_text.InsertItem(Add_line, str(year[index]))
            self.fiscal_year_text.SetItem(Add_line, 1, str(money[index]))
            Add_line += 1
