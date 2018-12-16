import wx


class TransactionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent)
        self.frame = parent
        self.__myinit()

    def __myinit(self):
        title = wx.StaticText(self, wx.ID_ANY, "一回あたりの課金額")
        Text = (u'金額幅', u'回数')
        # 検索結果を表示するリストコントローラ
        self.per_transaction_text = wx.ListCtrl(self, wx.ID_ANY, size=(200, 400), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i, text in enumerate(Text):
            self.per_transaction_text.InsertColumn(i, text)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(title, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.per_transaction_text, (1, 0), (1, 1), flag=wx.EXPAND)
        self.SetSizer(layout)
        self.Layout()

    def per_add_listctrl_item(self):
        year = ['1-1000', '1001-2000', '2001-3000', '3001-4000', '4001-5000', '5001-6000', '6001-7000', '7001-8000', '8001-9000', '9001-10000', '10001-11000', '11001-12000', '12001-13000']
        money = [68, 45, 12, 11, 28, 24, 12, 0, 2, 100, 3, 1, 1]
        # 追加する行の指定
        Add_line = self.per_transaction_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(year)):
            # 行の追加を行う
            self.per_transaction_text.InsertItem(Add_line, year[index])
            self.per_transaction_text.SetItem(Add_line, 1, str(money[index]))
            Add_line += 1
