import wx
import datetime
from . import mainGui
from service import useListCreate
from service import dataListCreate

class Register(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500,500))
        now = datetime.datetime.now()
        self.year = str(now.year)
        self.month = str(now.month)
        self.day = str(now.day)
        self.myinit()

        # 閉じるイベント
        self.Bind(wx.EVT_CLOSE, self.frame_close)

        self.Centre()
        self.Show()

    def myinit(self):
        self.panel = wx.Panel(self, wx.ID_ANY, size=(500,500))
        # 初期設定
        input_length = 10
        use_list = useListCreate.create_list()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()
        layout_list = []
        size = (100,25)

        # 金額入力欄
        text_money = wx.StaticText(self.panel, wx.ID_ANY, '金額', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list.append(wx.BoxSizer(wx.VERTICAL))
        layout_list[0].Add(text_money)
        spinctrl_money_list = []
        for i in range(input_length):
            spinctrl_money_list.append(wx.SpinCtrl(self.panel, wx.ID_ANY, max=1000000, size=size))
            layout_list[0].Add(spinctrl_money_list[i])

        # 用途入力欄
        text_use = wx.StaticText(self.panel, wx.ID_ANY, '用途', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list.append(wx.BoxSizer(wx.VERTICAL))
        layout_list[1].Add(text_use)
        combobox_use_list = []
        for i in range(input_length):
            combobox_use_list.append(wx.ComboBox(self.panel, wx.ID_ANY, '選択', choices=use_list, style=wx.CB_DROPDOWN, size=size))
            layout_list[1].Add(combobox_use_list[i])

        # 年度入力欄
        text_year = wx.StaticText(self.panel, wx.ID_ANY, '年', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list.append(wx.BoxSizer(wx.VERTICAL))
        layout_list[2].Add(text_year)
        spinctrl_year_list = []
        for i in range(input_length):
            spinctrl_year_list.append(wx.SpinCtrl(self.panel, wx.ID_ANY, value=self.year, max=3000, size=size))
            layout_list[2].Add(spinctrl_year_list[i])

        # 月入力欄
        text_month = wx.StaticText(self.panel, wx.ID_ANY, '月', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list.append(wx.BoxSizer(wx.VERTICAL))
        layout_list[3].Add(text_month)
        combobox_month_list = []
        for i in range(input_length):
            combobox_month_list.append(wx.ComboBox(self.panel, wx.ID_ANY, self.month, choices=month_list, style=wx.CB_DROPDOWN, size=size))
            layout_list[3].Add(combobox_month_list[i])

        # 日入力欄
        text_day = wx.StaticText(self.panel, wx.ID_ANY, '日', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list.append(wx.BoxSizer(wx.VERTICAL))
        layout_list[4].Add(text_day)
        combobox_day_list = []
        for i in range(input_length):
            combobox_day_list.append(wx.ComboBox(self.panel, wx.ID_ANY, self.day, choices=day_list, style=wx.CB_DROPDOWN, size=size))
            layout_list[4].Add(combobox_day_list[i])

        layout = wx.BoxSizer(wx.HORIZONTAL)
        for i in range(len(layout_list)):
            layout.Add(layout_list[i])

        self.panel.SetSizer(layout)

    def frame_close(self, event):
        self.Destroy()
        wx.Exit()
        mainGui.call_mainGui()

def call_register():
    app = wx.App(False)
    Register(None, wx.ID_ANY, title=u'BRS')
    app.MainLoop()