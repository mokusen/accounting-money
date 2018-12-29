from operator import itemgetter
import wx
from method.services import accountingService, cacheService
from . import detail, graph, common
from .searchNote import usePanel, amountPanel, yearPanel, monthPanel


class NotebookPanel(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent)
        self.main_panel = parent
        self.__myinit()

    def __myinit(self):
        self.search_result_panel = wx.Panel(self, wx.ID_ANY)
        self.statistics_panel = wx.Panel(self, wx.ID_ANY)
        self.InsertPage(0, self.search_result_panel, '検索結果')
        self.InsertPage(1, self.statistics_panel, '統計情報')
        self.__create_search_result()
        self.__create_statistics()

    """　notebookのpanel作成　"""

    def __create_search_result(self):
        """
        検索結果を表示するNoteBookパネルを作成する
        """
        Text = (u'ID', u'用途', u'金額', u'年', u'月', u'日', u'作成日', u'更新日')
        self.frame_size = common.search_ctrl_size()
        self.search_result_text = wx.ListCtrl(self.search_result_panel, wx.ID_ANY, size=self.frame_size, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_EDIT_LABELS)
        for i, text in enumerate(Text):
            self.search_result_text.InsertColumn(i, text)
        # Textの幅を個別設定する
        width_list = [30, 80, 60, 60, 50, 50, 125, 125]
        for index, width in enumerate(width_list):
            self.search_result_text.SetColumnWidth(index, width)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.search_result_text, (0, 0), (1, 1), flag=wx.EXPAND)
        self.search_result_panel.SetSizer(layout)
        # 詳細ページ表示イベント
        self.search_result_panel.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.detail_open)
        # ソートイベントを登録する
        self.search_result_panel.Bind(wx.EVT_LIST_COL_CLICK, self.call_sort)
        self.search_result_panel.Layout()

    def __create_statistics(self):
        """
        統計情報を表示するNoteBookパネルを作成する
        """
        self.fiscal_year_panel = yearPanel.YearPanel(self.statistics_panel)
        self.fiscal_month_panel = monthPanel.MonthPanel(self.statistics_panel)
        self.by_use_panel = usePanel.UsePanel(self.statistics_panel)
        self.every_amount_panel = amountPanel.AmountPanel(self.statistics_panel)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.fiscal_year_panel, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.fiscal_month_panel, (1, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.by_use_panel, (0, 1), (2, 1), flag=wx.EXPAND)
        layout.Add(self.every_amount_panel, (0, 2), (2, 1), flag=wx.EXPAND)
        self.statistics_panel.SetSizer(layout)
        self.statistics_panel.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.test_open)
        self.statistics_panel.Layout()

    """ 共通機能作成 """

    def search_statistics(self, select_comdition_list):
        """
        統計情報を取得する。
        年度別、用途別、課金額毎、期間別を取得する
        Parameters
        ----------
        select_comdition_list : list
            [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
        """
        self.year_accounting_list = accountingService.select_accounting_year(select_comdition_list)
        use_accounting_list = accountingService.select_accounting_use(select_comdition_list)
        search_money_list, amount_accounting_list = accountingService.select_accounting_amount(select_comdition_list)
        period_accounting_list = accountingService.select_accounting_period(select_comdition_list)
        # 統計情報のパネル設定
        self.fiscal_year_panel.year_add_listctrl_item(self.year_accounting_list)
        self.fiscal_month_panel.month_reset_listctrl()
        self.by_use_panel.use_add_listctrl_item(use_accounting_list)
        self.every_amount_panel.amount_add_listctrl_item(search_money_list, amount_accounting_list)
        try:
            self.graph.frame_close_oparate()
        except:
            pass
        statistics_info_dict = {"year": self.year_accounting_list, "use": use_accounting_list, "amount": self.all_data, "period": period_accounting_list}
        self.graph = graph.call_graph(statistics_info_dict)

    """ 検索結果画面の機能 """

    def search_accounting(self, all_data, select_condition_list):
        """
        検索条件を元に、検索を行い、検索結果に表示する。
        Parameters
        ----------
        all_data : list
            全件データを格納する
        select_condition_list : list
            [use, min_money, max_money, min_year, max_year, min_month, max_month, min_day, max_day]
        """
        # 検索結果格納リスト
        self.all_data = all_data
        self.search_result_text.DeleteAllItems()
        # 追加する行の指定
        Add_line = self.search_result_text.GetItemCount()
        # 検索結果を行に追加する
        for items in self.all_data:
            # 行の追加を行う
            self.search_result_text.InsertItem(Add_line, str(items[0]))
            for item in range(1, len(items)):
                if item in [6, 7]:
                    # 作成日と更新日をYY/MM/DD HH:MM:SSに変換する
                    self.search_result_text.SetItem(Add_line, item, items[item].strftime('%Y/%m/%d %H:%M:%S'))
                else:
                    self.search_result_text.SetItem(Add_line, item, str(items[item]))
            Add_line += 1
        self.search_statistics(select_condition_list)

    def call_sort(self, event):
        """
        検索結果をソート処理を呼び出す

        Parameters
        ----------
        event : event
            wxPythonのeventクラス
        """
        if self.all_data != []:
            if event.GetColumn() not in [1, 6, 7]:
                self.sort_item(event.GetColumn())

    def sort_item(self, col_number):
        """
        listctrlのitemをソートする

        Parameters
        ----------
        col_number : int
            listctrlの列番号

        """
        search_list = []
        # 現在のidの順番を把握する
        for i in range(self.search_result_text.GetItemCount()):
            search_list.append([i, int(self.search_result_text.GetItem(itemIdx=i, col=col_number).GetText())])
        searched_list = sorted(search_list, key=itemgetter(1))
        # ソート結果と、初期データ同じ場合、反転する
        if searched_list == search_list:
            searched_list = searched_list[::-1]
        # 既存のlistctrlの情報をすべて消す
        self.search_result_text.DeleteAllItems()
        # listctrlに情報を追加する
        self.add_listctrl_item(searched_list)
        self.all_data = []
        # 次のソートの時用にall_dataを作り直す
        for i in range(self.search_result_text.GetItemCount()):
            self.all_data_create(i)

    def all_data_create(self, col_number):
        """
        ソート後、all_dataを作成し直す

        Parameters
        ----------
        col_number : int or string
            列番号

        """
        self.all_data.append([])
        number = len(self.all_data)
        for j in range(self.search_result_text.GetColumnCount()):
            self.all_data[number - 1].append(self.search_result_text.GetItemText(col_number, col=j))

    def add_listctrl_item(self, search_list):
        """
        ソート後、listctrlに情報を挿入する

        Parameters
        ----------
        search_list : list型
            idが挿入されたリスト

        """
        # 追加する行の指定
        Add_line = self.search_result_text.GetItemCount()
        # 検索結果を行に追加する
        for date in search_list:
            # 行の追加を行う
            self.search_result_text.InsertItem(Add_line, str(self.all_data[date[0]][0]))
            for item in range(1, len(self.all_data[date[0]])):
                if item in [6, 7]:
                    # 作成日と更新日をYY/MM/DD HH:MM:SSに変換する
                    try:
                        self.search_result_text.SetItem(Add_line, item, self.all_data[date[0]][item].strftime('%Y/%m/%d %H:%M:%S'))
                    except:
                        self.search_result_text.SetItem(Add_line, item, str(self.all_data[date[0]][item]))
                else:
                    self.search_result_text.SetItem(Add_line, item, str(self.all_data[date[0]][item]))
            Add_line += 1

    def detail_open(self, event):
        """
        detailの画面を呼び出す

        Parameters
        ----------
        event : event
            wxPythonのeventクラス
        """
        # 選択されたindexを取得する
        index = event.GetIndex()

        # 用途から日までを取得し、リストに格納する
        detail_info_list = []
        column = self.search_result_text.GetColumnCount()-2
        for i in range(column):
            item = self.search_result_text.GetItem(itemIdx=index, col=i)
            detail_info_list.append(item.GetText())

        self.main_panel.close_frame()
        try:
            self.graph.frame_close_oparate()
        except:
            pass
        detail.call_detail(detail_info_list)

    def test_open(self, event):
        index = event.GetIndex()
        year = self.fiscal_year_panel.fiscal_year_text.GetItem(itemIdx=index, col=0).GetText()
        self.fiscal_month_panel.month_add_listctrl_item(self.year_accounting_list, year)
