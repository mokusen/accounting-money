import wx
from .graphNote import yearGraph, useGraph, periodGraph, amountGraph


class GraphNotePanel(wx.Notebook):
    def __init__(self, parent, year_accounting_list, title_accounting_list, all_data, test):
        wx.Notebook.__init__(self, parent=parent)
        self.main_panel = parent
        self.year_accounting_list = year_accounting_list
        self.title_accounting_list = title_accounting_list
        self.all_data = all_data
        self.test = test
        self.__myinit()

    def __myinit(self):
        self.year_panel = yearGraph.YearGraph(self, year_accounting_list=self.year_accounting_list)
        self.use_panel = useGraph.UseGraph(self, title_accounting_list=self.title_accounting_list)
        self.period_panel = periodGraph.PeriodGraph(self, self.test)
        self.amount_panel = amountGraph.AmountGraph(self, self.all_data)
        self.InsertPage(0, self.year_panel, '年度別課金額')
        self.InsertPage(1, self.use_panel, '用途別課金額')
        self.InsertPage(2, self.period_panel, '期間別課金額')
        self.InsertPage(3, self.amount_panel, '課金額別回数')

    # def __create_year(self):

    # def __create_use(self):

    # def __create_period(self):

    # def __create_amount(self):
