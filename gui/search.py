import wx
from . import mainGui, detail, common, mainSearchNote
from utils import dataListCreate
from services import accountingService, baseService, cacheService
from logging import getLogger, DEBUG, INFO
from utils import logger

logger = logger.set_operate_logger(__name__)


class Search(wx.Frame):
    def __init__(self, parent, id, title):
        self.frame_size = common.search_frame_size()
        use_display_size = common.search_use_display_size()
        wx.Frame.__init__(self, parent, id, title, size=self.frame_size, pos=use_display_size)
        self.SetIcon(common.get_icon())
        self.CreateStatusBar()
        self.main_panel = MainPanel(self)
        self.Bind(wx.EVT_CLOSE, self.frame_close)
        self.Show()

    def frame_close(self, event):
        self.Destroy()
        try:
            self.main_panel.searchNote.graph.frame_close_oparate()
        except:
            pass
        wx.Exit()
        mainGui.call_mainGui()


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.frame_size = common.search_frame_size()
        self.__myinit()

    def __myinit(self):
        # 初期設定
        self.input_defalut_text = "選択"
        use_list = baseService.select_base()
        month_list = dataListCreate.create_month()
        day_list = dataListCreate.create_day()

        # 初期値追加
        use_list.insert(0, '')

        # size設定
        form_size = (100, 25)
        text_size = (50, 25)

        # font設定
        self.font = common.defalut_font_size()

        # 検索フォームのラベル作成
        text_use = wx.StaticText(self, wx.ID_ANY, '用途', size=text_size, style=wx.TE_CENTER)
        text_money = wx.StaticText(self, wx.ID_ANY, '金額', size=text_size, style=wx.TE_CENTER)
        text_year = wx.StaticText(self, wx.ID_ANY, '年', size=text_size, style=wx.TE_CENTER)
        text_month = wx.StaticText(self, wx.ID_ANY, '月', size=text_size, style=wx.TE_CENTER)
        text_day = wx.StaticText(self, wx.ID_ANY, '日', size=text_size, style=wx.TE_CENTER)

        # 検索フォームのラベルフォント設定
        text_use.SetFont(self.font)
        text_money.SetFont(self.font)
        text_year.SetFont(self.font)
        text_month.SetFont(self.font)
        text_day.SetFont(self.font)

        # 検索フォーム作成
        self.search_use = wx.ComboBox(self, wx.ID_ANY, self.input_defalut_text, choices=use_list, style=wx.CB_READONLY, size=form_size)
        self.search_money_list = [wx.TextCtrl(self, wx.ID_ANY, size=form_size) for _ in range(2)]
        self.search_year_list = [wx.TextCtrl(self, wx.ID_ANY, size=form_size) for _ in range(2)]
        self.search_month_list = [wx.ComboBox(self, wx.ID_ANY, choices=month_list, style=wx.CB_READONLY, size=form_size) for _ in range(2)]
        self.search_day_list = [wx.ComboBox(self, wx.ID_ANY, choices=day_list, style=wx.CB_READONLY, size=form_size) for _ in range(2)]

        # ~を作成する
        text_tilde_list = [wx.StaticText(self, wx.ID_ANY, '～', size=(25, 25), style=wx.TE_CENTER) for _ in range(4)]

        # 検索ボタン
        search_button = wx.Button(self, wx.ID_ANY, '検索')
        search_button.Bind(wx.EVT_BUTTON, self.call_select)

        # notebookを初期化する
        self.searchNote = mainSearchNote.NotebookPanel(self)

        # 検索フォームのレイアウト設定
        search_layout = wx.GridBagSizer(10, 5)
        search_layout.Add(text_use, (0, 0), (1, 1), flag=wx.EXPAND)
        search_layout.Add(self.search_use, (0, 1), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_money, (1, 0), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_year, (0, 4), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_month, (1, 4), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_day, (2, 4), (1, 1), flag=wx.EXPAND)
        for i in range(2):
            search_layout.Add(self.search_money_list[i], (1, 1 + i*2), (1, 1), flag=wx.EXPAND)
            search_layout.Add(self.search_year_list[i], (0, 5 + i*2), (1, 1), flag=wx.EXPAND)
            search_layout.Add(self.search_month_list[i], (1, 5 + i*2), (1, 1), flag=wx.EXPAND)
            search_layout.Add(self.search_day_list[i], (2, 5 + i*2), (1, 1), flag=wx.EXPAND)
        search_layout.Add(text_tilde_list[0], (1, 2), (1, 1), flag=wx.EXPAND)
        for i in range(3):
            search_layout.Add(text_tilde_list[i+1], (i, 6), (1, 1), flag=wx.EXPAND)
        search_layout.Add(search_button, (2, 1), (1, 3), flag=wx.EXPAND)

        # レイアウト設定
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(search_layout, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)
        layout.Add(self.searchNote, flag=wx.EXPAND)

        # cache情報を取得し、反映する
        test_date = cacheService.select_cache()
        self.search_use.SetValue(str(test_date[0][1]))
        self.search_money_list[0].SetValue(str(test_date[0][2]))
        self.search_money_list[1].SetValue(str(test_date[0][3]))
        self.search_year_list[0].SetValue(str(test_date[0][4]))
        self.search_year_list[1].SetValue(str(test_date[0][5]))
        self.search_month_list[0].SetValue(str(test_date[0][6]))
        self.search_month_list[1].SetValue(str(test_date[0][7]))
        self.search_day_list[0].SetValue(str(test_date[0][8]))
        self.search_day_list[1].SetValue(str(test_date[0][9]))
        self.SetSizer(layout)

    def adjust_search_info(self):
        """
        検索条件を取得し、リスト化して返却する

        Returns
        -------
        select_condition_list : list
            [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
        """
        select_condition_list = []
        select_condition_list.append(self.search_use.GetValue())
        select_condition_list.append(self.search_money_list[0].GetValue())
        select_condition_list.append(self.search_money_list[1].GetValue())
        select_condition_list.append(self.search_year_list[0].GetValue())
        select_condition_list.append(self.search_year_list[1].GetValue())
        select_condition_list.append(self.search_month_list[0].GetValue())
        select_condition_list.append(self.search_month_list[1].GetValue())
        select_condition_list.append(self.search_day_list[0].GetValue())
        select_condition_list.append(self.search_day_list[1].GetValue())
        return select_condition_list

    def call_select(self, event):
        select_condition_list = self.adjust_search_info()
        all_data, all_money = accountingService.select_accounting(select_condition_list)
        cacheService.update_cache(select_condition_list)
        self.frame.SetStatusText(f'累計金額：{all_money:,}円です。')
        self.searchNote.search_accounting(all_data, select_condition_list)

    def close_frame(self):
        self.frame.Destroy()
        wx.Exit()


def call_search():
    app = wx.App(False)
    logger.info("START Search")
    Search(None, wx.ID_ANY, title=u'CHMS | 検索')
    app.MainLoop()
