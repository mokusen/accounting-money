import wx
from .notebook import titlePanel
from .notebook import transactionPanel
from .notebook import yearPanel


class NotebookPanel(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent)
        self.frame = parent
        self.__myinit()

    def __myinit(self):
        self.search_result_panel = wx.Panel(self, wx.ID_ANY)
        self.statistics_panel = wx.Panel(self, wx.ID_ANY)
        self.InsertPage(0, self.search_result_panel, '検索結果')
        self.InsertPage(1, self.statistics_panel, '統計情報')
        self.__create_search_result()
        self.__create_statistics()

    def __create_search_result(self):
        Text = (u'ID', u'用途', u'金額', u'年', u'月', u'日', u'作成日', u'更新日')
        self.frame_size = (600, 400)
        self.frame.search_result_text = wx.ListCtrl(self.search_result_panel, wx.ID_ANY, size=self.frame_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_EDIT_LABELS)
        for i, text in enumerate(Text):
            self.frame.search_result_text.InsertColumn(i, text)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.frame.search_result_text, (0, 0), (1, 1), flag=wx.EXPAND)
        self.search_result_panel.SetSizer(layout)
        self.search_result_panel.Layout()

    def __create_statistics(self):
        self.fiscal_year_panel = yearPanel.YearPanel(self.statistics_panel)
        self.by_title_panel = titlePanel.TitlePanel(self.statistics_panel)
        self.per_transaction_panel = transactionPanel.TransactionPanel(self.statistics_panel)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.fiscal_year_panel, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.by_title_panel, (0, 1), (1, 1), flag=wx.EXPAND)
        layout.Add(self.per_transaction_panel, (0, 2), (1, 1), flag=wx.EXPAND)
        self.statistics_panel.SetSizer(layout)
        self.statistics_panel.Layout()

    def add_item(self):
        self.fiscal_year_panel.year_add_listctrl_item()
        self.by_title_panel.title_add_listctrl_item()
        self.per_transaction_panel.per_add_listctrl_item()
