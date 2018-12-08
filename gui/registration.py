import wx
import datetime
from . import mainGui
from utils import useListCreate, dataListCreate
from services import register

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
        self.input_length = 10
        self.input_defalut_text = "選択"
        use_list = useListCreate.create_list()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()
        layout_list = []
        for i in range(11):
            layout_list.append(wx.BoxSizer(wx.HORIZONTAL))
        size = (100,25)
        co_size = (100,30)

        # 用途入力欄
        text_use = wx.StaticText(self.panel, wx.ID_ANY, '用途', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list[0].Add(text_use, flag= wx.TOP | wx.LEFT , border=10)
        self.combobox_use_list = []

        # 金額入力欄
        text_money = wx.StaticText(self.panel, wx.ID_ANY, '金額', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list[0].Add(text_money, flag= wx.TOP, border=10)
        self.spinctrl_money_list = []

        # 年度入力欄
        text_year = wx.StaticText(self.panel, wx.ID_ANY, '年', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list[0].Add(text_year, flag= wx.TOP, border=10)
        self.spinctrl_year_list = []

        # 月入力欄
        text_month = wx.StaticText(self.panel, wx.ID_ANY, '月', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list[0].Add(text_month, flag= wx.TOP, border=10)
        self.combobox_month_list = []

        # 日入力欄
        text_day = wx.StaticText(self.panel, wx.ID_ANY, '日', size=size, style=wx.TE_CENTER | wx.SIMPLE_BORDER)
        layout_list[0].Add(text_day, flag= wx.TOP | wx.RIGHT , border=10)
        self.combobox_day_list = []

        # 登録ボタン作成
        register_button = wx.Button(self.panel, wx.ID_ANY, '登録')

        # 登録ボタンにイベントを登録する
        register_button.Bind(wx.EVT_BUTTON, self.get_register_info)

        # インプット要素生成
        for i in range(self.input_length):
            self.combobox_use_list.append(wx.ComboBox(self.panel, wx.ID_ANY, self.input_defalut_text, choices=use_list, style=wx.CB_DROPDOWN, size=co_size))
            self.spinctrl_money_list.append(wx.SpinCtrl(self.panel, wx.ID_ANY, max=1000000, size=size))
            self.spinctrl_year_list.append(wx.SpinCtrl(self.panel, wx.ID_ANY, value=self.year, max=3000, size=size))
            self.combobox_month_list.append(wx.ComboBox(self.panel, wx.ID_ANY, self.month, choices=month_list, style=wx.CB_DROPDOWN, size=co_size))
            self.combobox_day_list.append(wx.ComboBox(self.panel, wx.ID_ANY, self.day, choices=day_list, style=wx.CB_DROPDOWN, size=co_size))

        # インプット要素をレイアウトする
        for i in range(self.input_length):
            layout_list[i+1].Add(self.combobox_use_list[i], flag= wx.LEFT, border=10)
            layout_list[i+1].Add(self.spinctrl_money_list[i])
            layout_list[i+1].Add(self.spinctrl_year_list[i])
            layout_list[i+1].Add(self.combobox_month_list[i])
            layout_list[i+1].Add(self.combobox_day_list[i], flag= wx.RIGHT, border=10)

        # 全体レイアウトを設定する
        layout = wx.GridBagSizer(0,0)
        for i in range(len(layout_list)):
            layout.Add(layout_list[i], (i,0), (1,5))
        layout.Add(register_button, (11,3), (1,2), flag=wx.EXPAND)

        self.panel.SetSizer(layout)

    def get_register_info(self, event):
        give_register_info = []
        for i in range(self.input_length):
            # 用途、金額共にデフォルトでない場合は、登録する
            if self.spinctrl_money_list[i].GetValue() != 0 and self.combobox_use_list[i].GetValue() != self.input_defalut_text:
                give_register_info.append([])
                give_length = len(give_register_info) - 1
                give_register_info[give_length].append(self.combobox_use_list[i].GetValue())
                give_register_info[give_length].append(self.spinctrl_money_list[i].GetValue())
                give_register_info[give_length].append(self.spinctrl_year_list[i].GetValue())
                give_register_info[give_length].append(self.combobox_month_list[i].GetValue())
                give_register_info[give_length].append(self.combobox_day_list[i].GetValue())
        error_msg = register.register(give_register_info)
        print(error_msg)

    def frame_close(self, event):
        """
        閉じるボタンが押下されたときにメインに戻る

        Parameters
        ----------
        event : event
            閉じるイベント
        """

        self.Destroy()
        wx.Exit()
        mainGui.call_mainGui()

def call_register():
    app = wx.App(False)
    Register(None, wx.ID_ANY, title=u'BRS | 登録')
    app.MainLoop()