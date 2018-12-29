import wx
import datetime
from . import mainGui, common
from method.utils import dataListCreate
from method.services import accountingService, baseService
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)


class Register(wx.Frame):
    def __init__(self, parent, id, title):
        frame_size = common.registration_frame_size()
        wx.Frame.__init__(self, parent, id, title, size=frame_size)
        self.SetIcon(common.get_icon())
        panel = MainPanel(self)
        self.Bind(wx.EVT_CLOSE, self.frame_close)
        self.Center()
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
        self.__myinit()

    def __myinit(self):
        # 初期設定
        self.input_length = 10
        self.input_defalut_text = "選択"
        use_list = baseService.select_base()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()

        # size設定
        stati_size = common.regi_statitext_size()
        num_size = common.regi_numtext_size()
        btn_size = common.regi_button_size()

        # font設定
        self.font = common.defalut_font_size()

        # テキスト設定
        show_text_list = ['用途', '金額', '年', '月', '日']
        text_list = []
        text_list.append(wx.StaticText(self, wx.ID_ANY, '', size=num_size))
        for text in show_text_list:
            text_list.append(wx.StaticText(self, wx.ID_ANY, text, size=stati_size, style=wx.TE_CENTER))

        # テキストフォント設定
        for text in text_list:
            text.SetFont(self.font)

        # 登録ボタン作成
        register_button = wx.Button(self, wx.ID_ANY, '登　録', size=btn_size)
        register_button.SetFont(self.font)

        # 登録ボタンにイベントを登録する
        register_button.Bind(wx.EVT_BUTTON, self.call_insert)

        # 入力欄リスト
        input_text_list = ["text", "use", "money", "year", "month", "day"]
        self.input_dict = {input_text: [] for input_text in input_text_list}

        # 入力欄リスト要素生成
        for i in range(self.input_length):
            self.input_dict["text"].append(wx.StaticText(self, wx.ID_ANY, str(i + 1), size=num_size, style=wx.TE_CENTER))
            self.input_dict["use"].append(wx.ComboBox(self, wx.ID_ANY, self.input_defalut_text, choices=use_list, style=wx.CB_DROPDOWN, size=stati_size))
            self.input_dict["money"].append(wx.SpinCtrl(self, wx.ID_ANY, max=1000000, size=stati_size))
            self.input_dict["year"].append(wx.SpinCtrl(self, wx.ID_ANY, value=self.year, max=3000, size=stati_size))
            self.input_dict["month"].append(wx.ComboBox(self, wx.ID_ANY, self.month, choices=month_list, style=wx.CB_READONLY, size=stati_size))
            self.input_dict["day"].append(wx.ComboBox(self, wx.ID_ANY, self.day, choices=day_list, style=wx.CB_READONLY, size=stati_size))

        # テキストナンバーリストのフォント設定
        for text_number in self.input_dict["text"]:
            text_number.SetFont(self.font)

        layout = wx.GridBagSizer(0, 0)

        # テキストレイアウト追加
        for t, text in enumerate(text_list):
            layout.Add(text, (0, t), (1, 1), flag=wx.TOP, border=10)

        # 入力欄レイアウト追加
        for index in range(self.input_length):
            for t_index, input_text in enumerate(input_text_list):
                layout.Add(self.input_dict[input_text][index], (index+1, t_index), (1, 1))

        # 登録ボタンレイアウト追加
        layout.Add(register_button, (12, 3), (2, 3), flag=wx.GROW)

        self.SetSizer(layout)

    def create_check_text(self):
        """
        登録確認用のメッセージを作成し、エラー条件に引っかかる場合はエラーフラグを返却する

        Returns
        -------
        error_flag : boolean
            True : エラーあり
            False : エラーなし
        temp_text : string
            確認内容
        """
        temp_text = "以下の内容で登録しますが、よろしいでしょうか？\n"
        error_counter = 0
        # 確認コメント作成
        for i in range(self.input_length):
            temp_text += f"{str(i+1):<2} : "
            # 用途がデフォルトまたは、金額が0円の行数をカウントする
            if self.input_dict["use"][i].GetValue() == self.input_defalut_text or self.input_dict["money"][i].GetValue() == 0:
                error_counter += 1
            if self.input_dict["use"][i].GetValue() == self.input_defalut_text:
                temp_text += f"{'':<8} "
            else:
                temp_text += f"{self.input_dict['use'][i].GetValue():<8} "
            temp_text += f"{self.input_dict['money'][i].GetValue():>5}円 "
            temp_text += f"{self.input_dict['year'][i].GetValue():>4}/"
            temp_text += f"{self.input_dict['month'][i].GetValue():>2}/"
            temp_text += f"{self.input_dict['day'][i].GetValue():>2}\n"
        # エラー処理
        if error_counter == self.input_length:
            return True, temp_text
        else:
            return False, temp_text

    def create_insert_list(self):
        """
        登録する内容をリストに保存し、返却する
        また、登録されていない用途を登録する

        Returns
        -------
        insert_info : list in list
            [[id, use, moneuy, year, month, day], [id, use, moneuy, year, month, day],...]
        """
        insert_info = []
        for i in range(self.input_length):
            # 用途取得
            use = self.input_dict["use"][i].GetValue()
            money = self.input_dict["money"][i].GetValue()
            # 用途、金額共にデフォルトでない場合は、登録する
            if money != 0 and use != self.input_defalut_text:
                # 新規の用途か判定し、ない場合追加する
                if use not in baseService.select_base():
                    baseService.insert_base(use)
                insert_info.append([])
                give_length = len(insert_info) - 1
                insert_info[give_length].append(self.input_dict["use"][i].GetValue())
                insert_info[give_length].append(self.input_dict["money"][i].GetValue())
                insert_info[give_length].append(self.input_dict["year"][i].GetValue())
                insert_info[give_length].append(self.input_dict["month"][i].GetValue())
                insert_info[give_length].append(self.input_dict["day"][i].GetValue())
        return insert_info

    def call_insert(self, event):
        """
        登録処理を呼び出す

        Parameters
        ----------
        event : event
            wxPythonのeventクラス
        """

        error_flag, temp_text = self.create_check_text()
        if error_flag:
            return wx.MessageBox("最低限1行入力して、登録データを作成してください", "入力エラー", wx.ICON_ERROR)
        dlg = wx.MessageDialog(None, f"{temp_text}", ' 登録内容確認', wx.YES_NO | wx.ICON_INFORMATION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            insert_info = self.create_insert_list()
            error_msg = accountingService.insert_accounting(insert_info)
            if error_msg is not False:
                return wx.MessageBox(error_msg, "Error", wx.ICON_ERROR)
            wx.MessageBox("登録完了しました。", "登録完了", wx.ICON_INFORMATION)
            self.frame.Destroy()
            wx.Exit()
            mainGui.call_mainGui()
        dlg.Destroy()


def call_register():
    app = wx.App(False)
    logger.info("START Register")
    Register(None, wx.ID_ANY, title=u'CHMS | 登録')
    app.MainLoop()
