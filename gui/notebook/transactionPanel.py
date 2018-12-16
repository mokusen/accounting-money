import wx
from services import accountingService


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

    def per_add_listctrl_item(self, select_comdition_list):
        self.per_transaction_text.DeleteAllItems()
        search_money_list, transaction_accounting_list = accountingService.select_accounting_transaction(select_comdition_list)
        accounting_count = transaction_accounting_list[0]
        print(accounting_count)
        # 追加する行の指定
        Add_line = self.per_transaction_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(accounting_count)):
            # 行の追加を行う
            self.per_transaction_text.InsertItem(Add_line, f'{search_money_list[index]}～{search_money_list[index+1]}')
            self.per_transaction_text.SetItem(Add_line, 1, str(accounting_count[index]))
            Add_line += 1
