import wx


class YearPanel(wx.Panel):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent)
        self.notebook = parent
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

    def year_add_listctrl_item(self):
        year = ['2012', '2013', '2014', '2015', '2016', '2017', '2018']
        money = [9000, 60475, 120800, 177930, 325200, 355090, 510340]
        # 追加する行の指定
        Add_line = self.fiscal_year_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(year)):
            # 行の追加を行う
            self.fiscal_year_text.InsertItem(Add_line, year[index])
            self.fiscal_year_text.SetItem(Add_line, 1, str(money[index]))
            Add_line += 1
