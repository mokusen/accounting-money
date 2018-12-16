import wx


class TitlePanel(wx.Panel):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent)
        self.frame = parent
        self.__myinit()

    def __myinit(self):
        title = wx.StaticText(self, wx.ID_ANY, "タイトル別課金額")
        Text = (u'用途', u'金額')
        # 検索結果を表示するリストコントローラ
        self.by_title_panel_text = wx.ListCtrl(self, wx.ID_ANY, size=(200, 380), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        for i, text in enumerate(Text):
            self.by_title_panel_text.InsertColumn(i, text)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(title, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.by_title_panel_text, (1, 0), (1, 1), flag=wx.EXPAND)
        self.SetSizer(layout)
        self.Layout()

    def title_add_listctrl_item(self):
        year = ['デレステ', 'ガルパ', 'パズドラ', 'グラブル', 'クリプト', '神撃', '戦国アスカ', '歌マクロス', 'ホウチ', 'ファンキル', 'ドールズ', 'ゴマ乙', 'ハチナイ', 'キンスレ', 'その他', '音楽', 'シノアリス', 'シャドバ', 'LINE', 'アスタ']
        money = [584240, 325240, 144475, 131880, 72440, 60640, 50400, 46400, 45060, 18000, 17600, 16440, 13130, 10560, 6340, 5750, 3000, 2840, 2800, 1600]
        # 追加する行の指定
        Add_line = self.by_title_panel_text.GetItemCount()
        # 検索結果を行に追加する
        for index in range(len(year)):
            # 行の追加を行う
            self.by_title_panel_text.InsertItem(Add_line, year[index])
            self.by_title_panel_text.SetItem(Add_line, 1, str(money[index]))
            Add_line += 1
