import wx
import datetime
from . import mainGui, common
from utils import logger
from dbInit import accountingDB, baseDB, dbInit
from sqls import insert


logger = logger.set_operate_logger(__name__)


class CsvOperation(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500, 310))
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
        self.__myinit()

    def __myinit(self):
        # 初期設定
        self.font = common.defalut_font_size()
        text_size = (350, 75)
        btn_size = (100, 25)

        text_list = ["現在登録されている用途と、課金履歴をCsvOut下に\nbase.csvとaccounting.csvで出力します。\n上記のcsvが存在する場合、上書き保存となり\n実行前のデータは削除されます。",
                     "CsvIn下にあるbase.csvとaccounting.csvを取り込みます。\n追加処理になるため、登録機能としても利用可能です。",
                     "データベースを初期化します。", ]
        btn_list = ['CSV出力', 'CSV取込', 'DB初期化']
        wx_text_list = [wx.StaticText(self, wx.ID_ANY, f"{text}", size=text_size, style=wx.TE_RIGHT) for text in text_list]
        wx_btn_list = [wx.Button(self, wx.ID_ANY, f"{btn_text}", size=btn_size) for btn_text in btn_list]
        # テキストナンバーリストのフォント設定
        for text in wx_text_list:
            text.SetFont(self.font)
        for btn in wx_btn_list:
            btn.SetFont(self.font)

        # Event登録
        wx_btn_list[0].Bind(wx.EVT_BUTTON, self.db_export_csv)
        wx_btn_list[1].Bind(wx.EVT_BUTTON, self.csv_insert_db)
        wx_btn_list[2].Bind(wx.EVT_BUTTON, self.db_init)

        layout = wx.GridBagSizer(0, 0)
        for i in range(len(wx_text_list)):
            layout.Add(wx_text_list[i], (i, 0), (1, 1), flag=wx.GROW | wx.LEFT | wx.TOP, border=10)
            layout.Add(wx_btn_list[i], (i, 1), (1, 1), flag=wx.GROW | wx.LEFT | wx.TOP, border=10)
        self.SetSizer(layout)

    def db_export_csv(self, event):
        dlg = wx.MessageDialog(None, "CSV出力を開始します。\n用途によって必要であればbase.csvとaccounting.csvの\nバックアップを取ることをオススメします", "CSV出力確認", wx.YES_NO | wx.ICON_INFORMATION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            baseDB.csv_export()
            accountingDB.csv_export()
            wx.MessageBox("CSV出力が完了しました。", "CSV出力完了", wx.ICON_INFORMATION)
        dlg.Destroy()

    def csv_insert_db(self, event):
        dlg = wx.MessageDialog(None, "CSV取込を開始します。", "CSV取込確認", wx.YES_NO | wx.ICON_INFORMATION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            use_list = baseDB.create_init_list()
            for item in use_list:
                insert.insert_base(item)
            accounting_list = accountingDB.create_list()
            for item in accounting_list:
                insert.insert_accounting(item)
            wx.MessageBox("CSV取込が完了しました。", "CSV取込完了", wx.ICON_INFORMATION)
        dlg.Destroy()

    def db_init(self, event):
        dlg = wx.MessageDialog(None, "DB初期化を開始します。\n用途によって必要であればCSV出力して、バックアップを取ることをオススメします", "DB初期化確認", wx.YES_NO | wx.ICON_INFORMATION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            dbInit.db_all_init()
            wx.MessageBox("DB初期化が完了しました。", "DB初期化完了", wx.ICON_INFORMATION)
        dlg.Destroy()


def call_csvOperation():
    app = wx.App(False)
    logger.info("START CsvOperation")
    CsvOperation(None, wx.ID_ANY, title=u'CHMS | CSV操作')
    app.MainLoop()
