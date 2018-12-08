import wx
import datetime
from . import mainGui, common
from utils import useListCreate, dataListCreate
from services import register

class Register(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(560,390))

        # icon設定
        self.SetIcon(common.get_icon())

        # panel作成
        panel = MainPanel(self)

        # 閉じるイベント
        self.Bind(wx.EVT_CLOSE, self.frame_close)

        self.Centre()
        self.Show()

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

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        # デフォルト設定
        now = datetime.datetime.now()
        self.year = str(now.year)
        self.month = str(now.month)
        self.day = str(now.day)
        self.myinit()

    def myinit(self):
        # 初期設定
        self.input_length = 10
        self.input_defalut_text = "選択"
        use_list = useListCreate.create_list()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()

        # size設定
        size = (100, 23)
        num_size = (30, 23)
        btn_size = (200,46)

        # font設定
        self.font = common.defalut_font_size()

        # テキスト設定
        text_list = []
        text_list.append(wx.StaticText(self, wx.ID_ANY, '', size=num_size))
        text_list.append(wx.StaticText(self, wx.ID_ANY, '用途', size=size, style=wx.TE_CENTER))
        text_list.append(wx.StaticText(self, wx.ID_ANY, '金額', size=size, style=wx.TE_CENTER))
        text_list.append(wx.StaticText(self, wx.ID_ANY, '年', size=size, style=wx.TE_CENTER))
        text_list.append(wx.StaticText(self, wx.ID_ANY, '月', size=size, style=wx.TE_CENTER))
        text_list.append(wx.StaticText(self, wx.ID_ANY, '日', size=size, style=wx.TE_CENTER))

        # テキストフォント設定
        for text in text_list:
            text.SetFont(self.font)

        # リセット、登録ボタン作成
        register_button = wx.Button(self, wx.ID_ANY, '登録', size=btn_size)

        # リセット、登録ボタンにイベントを登録する
        register_button.Bind(wx.EVT_BUTTON, self.get_register_info)

        # 入力欄リスト
        self.text_number_list = []
        self.combobox_use_list = []
        self.spinctrl_money_list = []
        self.spinctrl_year_list = []
        self.combobox_month_list = []
        self.combobox_day_list = []

        # 入力欄リスト要素生成
        for i in range(self.input_length):
            self.text_number_list.append(wx.StaticText(self, wx.ID_ANY, str(i+1), size=num_size, style=wx.TE_CENTER))
            self.combobox_use_list.append(wx.ComboBox(self, wx.ID_ANY, self.input_defalut_text, choices=use_list, style=wx.CB_DROPDOWN, size=size))
            self.spinctrl_money_list.append(wx.SpinCtrl(self, wx.ID_ANY, max=1000000, size=size))
            self.spinctrl_year_list.append(wx.SpinCtrl(self, wx.ID_ANY, value=self.year, max=3000, size=size))
            self.combobox_month_list.append(wx.ComboBox(self, wx.ID_ANY, self.month, choices=month_list, style=wx.CB_READONLY, size=size))
            self.combobox_day_list.append(wx.ComboBox(self, wx.ID_ANY, self.day, choices=day_list, style=wx.CB_READONLY, size=size))

        # テキストナンバーリストのフォント設定
        for text_number in self.text_number_list:
            text_number.SetFont(self.font)

        layout = wx.GridBagSizer(0,0)

        # テキストレイアウト追加
        for t, text in enumerate(text_list):
            layout.Add(text, (0,t), (1,1), flag=wx.TOP, border=10)

        # 入力欄レイアウト追加
        for i in range(self.input_length):
            layout.Add(self.text_number_list[i], (i+1,0), (1,1))
            layout.Add(self.combobox_use_list[i], (i+1,1), (1,1))
            layout.Add(self.spinctrl_money_list[i], (i+1,2), (1,1))
            layout.Add(self.spinctrl_year_list[i], (i+1,3), (1,1))
            layout.Add(self.combobox_month_list[i], (i+1,4), (1,1))
            layout.Add(self.combobox_day_list[i], (i+1,5), (1,1))

        # 登録ボタンレイアウト追加
        layout.Add(register_button, (12,3), (2,3), flag=wx.GROW)

        self.SetSizer(layout)

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

def call_register():
    app = wx.App(False)
    Register(None, wx.ID_ANY, title=u'CHMS | 登録')
    app.MainLoop()