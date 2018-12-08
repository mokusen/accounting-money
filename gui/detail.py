import wx
import datetime
from utils import useListCreate, dataListCreate
from . import search
from services import detail

class Detail(wx.Frame):
    def __init__(self, parent, id, title, detail_info_list):
        self.frame_size = (675,600)
        wx.Frame.__init__(self, parent, id, title, size=(300,300))
        # 課金情報リスト
        self.detail_info_list = detail_info_list

        # 要素の作成
        self.myinit()

        # 閉じるイベント
        self.Bind(wx.EVT_CLOSE, self.frame_close)

        self.Centre()
        self.Show()

    def myinit(self):
        self.panel = wx.Panel(self, wx.ID_ANY, size=self.frame_size)
        use_list = useListCreate.create_list()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()
        form_size = (100,25)
        text_size = (50,25)
        button_size = (100,25)

        # 修正フォームのラベル作成
        text_id = wx.StaticText(self.panel, wx.ID_ANY, 'ID', size=text_size, style=wx.TE_CENTER)
        text_use = wx.StaticText(self.panel, wx.ID_ANY, '用途', size=text_size, style=wx.TE_CENTER)
        text_money = wx.StaticText(self.panel, wx.ID_ANY, '金額', size=text_size, style=wx.TE_CENTER)
        text_year = wx.StaticText(self.panel, wx.ID_ANY, '年', size=text_size, style=wx.TE_CENTER)
        text_month = wx.StaticText(self.panel, wx.ID_ANY, '月', size=text_size, style=wx.TE_CENTER)
        text_day = wx.StaticText(self.panel, wx.ID_ANY, '日', size=text_size, style=wx.TE_CENTER)

        # 修正フォーム作成
        self.detail_id = wx.StaticText(self.panel, wx.ID_ANY, self.detail_info_list[0], size=form_size, style=wx.TE_CENTER)
        self.detail_use = wx.ComboBox(self.panel, wx.ID_ANY, value=self.detail_info_list[1], choices=use_list, style=wx.CB_DROPDOWN, size=form_size)
        self.detail_money = wx.TextCtrl(self.panel, wx.ID_ANY, value=self.detail_info_list[2],size=form_size)
        self.detail_money.SetMaxLength(5)
        self.detail_year = wx.TextCtrl(self.panel, wx.ID_ANY, value=self.detail_info_list[3],size=form_size)
        self.detail_year.SetMaxLength(4)
        self.detail_month = wx.ComboBox(self.panel, wx.ID_ANY, value=self.detail_info_list[4],choices=month_list, style=wx.CB_DROPDOWN, size=form_size)
        self.detail_day = wx.ComboBox(self.panel, wx.ID_ANY, value=self.detail_info_list[5],choices=day_list, style=wx.CB_DROPDOWN, size=form_size)

        # 更新、削除ボタン
        update_button = wx.Button(self.panel, wx.ID_ANY, '更新', size=button_size)
        delete_button = wx.Button(self.panel, wx.ID_ANY, '削除', size=button_size)

        # 更新、削除ボタンにイベントを登録する
        update_button.Bind(wx.EVT_BUTTON, self.call_update)
        delete_button.Bind(wx.EVT_BUTTON, self.call_delete)

        # レイアウト設定
        detail_layout = wx.GridBagSizer(10, 5)
        detail_layout.Add(text_id, (0, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(text_use, (1, 0), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(text_money, (2, 0), (1,1), flag=wx.EXPAND)
        detail_layout.Add(text_year, (3, 0), (1,1), flag=wx.EXPAND)
        detail_layout.Add(text_month, (4, 0), (1,1), flag=wx.EXPAND)
        detail_layout.Add(text_day, (5, 0), (1,1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_id, (0, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_use, (1, 1), (1, 1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_money, (2, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_year, (3, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_month, (4, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(self.detail_day, (5, 1), (1,1), flag=wx.EXPAND)
        detail_layout.Add(update_button, (1, 2), (2,1), flag=wx.EXPAND)
        detail_layout.Add(delete_button, (4, 2), (2,1), flag=wx.EXPAND)

        # 全体レイアウト
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(detail_layout, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        self.panel.SetSizer(layout)

    def call_update(self, event):
        # 更新情報を取得する
        after_list = []
        after_list.append(self.detail_id.GetLabel())
        after_list.append(self.detail_use.GetValue())
        after_list.append(self.detail_money.GetValue())
        after_list.append(self.detail_year.GetValue())
        after_list.append(self.detail_month.GetValue())
        after_list.append(self.detail_day.GetValue())

        # 更新内容に変更があるか確認する
        if self.detail_info_list == after_list:
            wx.MessageBox("最低限1つの項目は変更して下さい。", "ERROR", wx.ICON_ERROR)
        else:
            # 更新するか確認する
            temp_text = "以下の内容で更新しますが、よろしいでしょうか？\n"
            temp_id = f"ID：{after_list[0]}\n"
            temp_use = f"用途：{after_list[1]}\n"
            temp_money = f"金額：{after_list[2]}\n"
            temp_year = f"年：{after_list[3]}\n"
            temp_month = f"月：{after_list[4]}\n"
            temp_day = f"日：{after_list[5]}"
            temple_text = temp_text + temp_id + temp_use + temp_money + temp_year + temp_month+ temp_day
            dlg = wx.MessageDialog(None, f"{temple_text}",' 更新内容確認', wx.YES_NO | wx.ICON_INFORMATION)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                # 更新する
                detail.update_accounting(after_list)
                wx.MessageBox("更新完了しました。", "更新完了", wx.ICON_INFORMATION)
                self.Destroy()
                wx.Exit()
                search.call_search()
            dlg.Destroy()

    def call_delete(self, event):
        # 削除情報を取得する
        delete_list = []
        delete_list.append(self.detail_id.GetLabel())
        delete_list.append(self.detail_use.GetValue())
        delete_list.append(self.detail_money.GetValue())
        delete_list.append(self.detail_year.GetValue())
        delete_list.append(self.detail_month.GetValue())
        delete_list.append(self.detail_day.GetValue())

        # 削除するか確認する
        temp_text = "以下の内容を削除しますが、よろしいでしょうか？\n"
        temp_id = f"ID：{delete_list[0]}\n"
        temp_use = f"用途：{delete_list[1]}\n"
        temp_money = f"金額：{delete_list[2]}\n"
        temp_year = f"年：{delete_list[3]}\n"
        temp_month = f"月：{delete_list[4]}\n"
        temp_day = f"日：{delete_list[5]}"
        temple_text = temp_text + temp_id + temp_use + temp_money + temp_year + temp_month+ temp_day
        dlg = wx.MessageDialog(None, f"{temple_text}",' 削除内容確認', wx.YES_NO | wx.ICON_INFORMATION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            # 更新する
            detail.delete_accounting([delete_list[0]])
            wx.MessageBox("削除完了しました。", "削除完了", wx.ICON_INFORMATION)
            self.Destroy()
            wx.Exit()
            search.call_search()
        dlg.Destroy()

    def frame_close(self, event):
        self.Destroy()
        wx.Exit()
        search.call_search()

def call_detail(detail_info_list):
    app = wx.App(False)
    Detail(None, wx.ID_ANY, title=u'BRS | 更新 削除', detail_info_list=detail_info_list)
    app.MainLoop()