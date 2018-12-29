import wx
import datetime
from method.utils import dataListCreate
from . import search, common
from method.services import accountingService, baseService, cacheService
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)


class Detail(wx.Frame):
    def __init__(self, parent, id, title, detail_info_list):
        frame_size = common.detail_frame_size()
        wx.Frame.__init__(self, parent, id, title, size=frame_size)
        self.SetIcon(common.get_icon())
        self.detail_info_list = detail_info_list
        panel = MainPanel(self)
        self.Bind(wx.EVT_CLOSE, self.frame_close)
        self.Center()
        self.Show()

    def frame_close(self, event):
        self.Destroy()
        wx.Exit()
        search.call_search()


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.__myinit()

    def __myinit(self):
        use_list = baseService.select_base()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()

        # size設定
        form_size = common.detail_form_size()
        text_size = common.detail_text_size()
        button_size = common.detail_button_size()

        # font設定
        self.font = common.defalut_font_size()

        # 修正フォームのラベル作成
        text_id = wx.StaticText(self, wx.ID_ANY, 'ID', size=text_size, style=wx.TE_CENTER)
        text_use = wx.StaticText(self, wx.ID_ANY, '用途', size=text_size, style=wx.TE_CENTER)
        text_money = wx.StaticText(self, wx.ID_ANY, '金額', size=text_size, style=wx.TE_CENTER)
        text_year = wx.StaticText(self, wx.ID_ANY, '年', size=text_size, style=wx.TE_CENTER)
        text_month = wx.StaticText(self, wx.ID_ANY, '月', size=text_size, style=wx.TE_CENTER)
        text_day = wx.StaticText(self, wx.ID_ANY, '日', size=text_size, style=wx.TE_CENTER)

        # 修正フォームのラベルフォント設定
        text_id.SetFont(self.font)
        text_use.SetFont(self.font)
        text_money.SetFont(self.font)
        text_year.SetFont(self.font)
        text_month.SetFont(self.font)
        text_day.SetFont(self.font)

        # 修正フォーム作成
        self.detail_id = wx.StaticText(self, wx.ID_ANY, self.frame.detail_info_list[0], size=form_size, style=wx.TE_CENTER)
        self.detail_use = wx.ComboBox(self, wx.ID_ANY, value=self.frame.detail_info_list[1], choices=use_list, style=wx.CB_DROPDOWN, size=form_size)
        self.detail_money = wx.TextCtrl(self, wx.ID_ANY, value=self.frame.detail_info_list[2], size=form_size)
        self.detail_money.SetMaxLength(5)
        self.detail_year = wx.TextCtrl(self, wx.ID_ANY, value=self.frame.detail_info_list[3], size=form_size)
        self.detail_year.SetMaxLength(4)
        self.detail_month = wx.ComboBox(self, wx.ID_ANY, value=self.frame.detail_info_list[4], choices=month_list, style=wx.CB_DROPDOWN, size=form_size)
        self.detail_day = wx.ComboBox(self, wx.ID_ANY, value=self.frame.detail_info_list[5], choices=day_list, style=wx.CB_DROPDOWN, size=form_size)

        # 更新、削除ボタン
        update_button = wx.Button(self, wx.ID_ANY, '更新', size=button_size)
        update_button.SetFont(self.font)
        delete_button = wx.Button(self, wx.ID_ANY, '削除', size=button_size)
        delete_button.SetFont(self.font)

        # 更新、削除ボタンにイベントを登録する
        update_button.Bind(wx.EVT_BUTTON, self.call_update)
        delete_button.Bind(wx.EVT_BUTTON, self.call_delete)

        # レイアウト設定
        detail_layout = wx.GridBagSizer(10, 5)
        detail_layout.Add(text_id, (0, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(text_use, (1, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(text_money, (2, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(text_year, (3, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(text_month, (4, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(text_day, (5, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_id, (0, 1), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_use, (1, 1), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_money, (2, 1), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_year, (3, 1), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_month, (4, 1), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_day, (5, 1), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(update_button, (1, 2), (2, 1), flag=wx.EXPAND)
        detail_layout.Add(delete_button, (4, 2), (2, 1), flag=wx.EXPAND)

        # 全体レイアウト
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(detail_layout, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(layout)

    def get_detail_info(self):
        """
        現在選択している、課金情報を取得する

        Returns
        -------
        detail_list : list
            [id, use, money, year, month, day]
        """

        detail_list = []
        detail_list.append(self.detail_id.GetLabel())
        detail_list.append(self.detail_use.GetValue())
        detail_list.append(self.detail_money.GetValue())
        detail_list.append(self.detail_year.GetValue())
        detail_list.append(self.detail_month.GetValue())
        detail_list.append(self.detail_day.GetValue())
        return detail_list

    def create_check_text(self, check_text, detail_list):
        """
        確認メッセージ用に選択している課金情報を表示用に整形する

        Parameters
        ----------
        check_text : string
            前情報
        detail_list : list
            [id, use, money, year, month, day]

        Returns
        -------
        check_text : string
            check_text += detail_list convert to text
        """
        check_text += f"ID：{detail_list[0]}\n"
        check_text += f"用途：{detail_list[1]}\n"
        check_text += f"金額：{detail_list[2]}\n"
        check_text += f"年：{detail_list[3]}\n"
        check_text += f"月：{detail_list[4]}\n"
        check_text += f"日：{detail_list[5]}"
        return check_text

    def call_check_dialog(self, sql_text, sql_list):
        """
        sqlの種類を入力させ、確認メッセージを出力する

        Parameters
        ----------
        sql_text : string
            更新 or 削除
        sql_list : list
            [id, use, money, year, month, day]
        """
        temple_text = f"以下の内容で{sql_text}しますが、よろしいでしょうか？\n"
        temple_text = self.create_check_text(temple_text, sql_list)
        dlg = wx.MessageDialog(None, f"{temple_text}", f'{sql_text}内容確認', wx.YES_NO | wx.ICON_INFORMATION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            if sql_text == "更新":
                accountingService.update_accounting(sql_list)
            elif sql_text == "削除":
                accountingService.delete_accounting(tuple([sql_list[0]]))
            else:
                logger.error(f"ダイアログから取得した値が不正です。プログラムの修正が必要です。 {sql_text}")
            wx.MessageBox(f"{sql_text}完了しました。", f"{sql_text}完了", wx.ICON_INFORMATION)
            self.frame.Destroy()
            search.call_search()
        dlg.Destroy()

    def call_update(self, event):
        """
        更新処理を呼び出す

        Parameters
        ----------
        event : event
            wxPythonのeventクラス

        """
        update_list = self.get_detail_info()

        # 更新内容に変更があるか確認する
        if self.frame.detail_info_list == update_list:
            wx.MessageBox("最低限1つの項目は変更して下さい。", "ERROR", wx.ICON_ERROR)
        else:
            self.call_check_dialog("更新", update_list)

    def call_delete(self, event):
        """
        削除処理を呼び出す

        Parameters
        ----------
        event : event
            wxPythonのeventクラス

        """
        delete_list = self.get_detail_info()
        self.call_check_dialog("削除", delete_list)


def call_detail(detail_info_list):
    app = wx.App(False)
    logger.info("START Detail")
    Detail(None, wx.ID_ANY, title=u'CHMS | 更新 削除', detail_info_list=detail_info_list)
    app.MainLoop()
