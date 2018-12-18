import wx


class GraphNotePanel(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent)
        self.main_panel = parent
        self.__myinit()

    def __myinit(self):
        self.year_panel = wx.Panel(self, wx.ID_ANY)
        self.use_panel = wx.Panel(self, wx.ID_ANY)
        self.period_panel = wx.Panel(self, wx.ID_ANY)
        self.amount_panel = wx.Panel(self, wx.ID_ANY)
        self.InsertPage(0, self.year_panel, '年度別金額')
        self.InsertPage(1, self.use_panel, '用途別金額')
        self.InsertPage(2, self.period_panel, '期間別金額')
        self.InsertPage(3, self.amount_panel, '金額別回数')

    # def __create_year(self):

    # def __create_use(self):

    # def __create_period(self):

    # def __create_amount(self):
