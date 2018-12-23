from operator import itemgetter
import wx
from services import accountingService, cacheService
from . import detail, graph
from .searchNote import titlePanel, transactionPanel, yearPanel


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

    """
    notebookのpanel作成
    """

    def __create_search_result(self):
        Text = (u'ID', u'用途', u'金額', u'年', u'月', u'日', u'作成日', u'更新日')
        self.frame_size = (600, 400)
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
        self.fiscal_year_panel = yearPanel.YearPanel(self.statistics_panel)
        self.by_title_panel = titlePanel.TitlePanel(self.statistics_panel)
        self.per_transaction_panel = transactionPanel.TransactionPanel(self.statistics_panel)
        layout = wx.GridBagSizer(0, 0)
        layout.Add(self.fiscal_year_panel, (0, 0), (1, 1), flag=wx.EXPAND)
        layout.Add(self.by_title_panel, (0, 1), (1, 1), flag=wx.EXPAND)
        layout.Add(self.per_transaction_panel, (0, 2), (1, 1), flag=wx.EXPAND)
        self.statistics_panel.SetSizer(layout)
        self.statistics_panel.Layout()

    """
    共通機能作成
    """

    def search_statistics(self, select_comdition_list):
        year_accounting_list = accountingService.select_accounting_year(select_comdition_list)
        title_accounting_list = accountingService.select_accounting_use(select_comdition_list)
        search_money_list, transaction_accounting_list = accountingService.select_accounting_transaction(select_comdition_list)
        test = accountingService.test(select_comdition_list)
        self.fiscal_year_panel.year_add_listctrl_item(year_accounting_list)
        self.by_title_panel.title_add_listctrl_item(title_accounting_list)
        self.per_transaction_panel.per_add_listctrl_item(search_money_list, transaction_accounting_list)
        try:
            self.graph.frame_close_oparate()
        except:
            pass
        self.graph = graph.call_graph(year_accounting_list, title_accounting_list, self.all_data, test)

    """
    検索結果画面の機能
    """

    def search_accounting(self, all_data, select_condition_list):
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
                if item == 6 or item == 7:
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
                if item == 6 or item == 7:
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
