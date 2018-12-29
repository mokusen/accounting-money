import wx
from .graphNote import yearGraph, useGraph, periodGraph, amountGraph
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)


class GraphNotePanel(wx.Notebook):
    def __init__(self, parent, statistics_info_dict):
        wx.Notebook.__init__(self, parent=parent)
        self.main_panel = parent
        self.statistics_info_dict = statistics_info_dict
        self.__myinit()

    def __myinit(self):
        self.year_panel = yearGraph.YearGraph(self, self.statistics_info_dict["year"])
        self.use_panel = useGraph.UseGraph(self, self.statistics_info_dict["use"])
        self.period_panel = periodGraph.PeriodGraph(self, self.statistics_info_dict["period"])
        self.amount_panel = amountGraph.AmountGraph(self, self.statistics_info_dict["amount"])
        self.InsertPage(0, self.year_panel, '年度別課金額')
        self.InsertPage(1, self.use_panel, '用途別課金額')
        self.InsertPage(2, self.period_panel, '期間別課金額')
        self.InsertPage(3, self.amount_panel, '課金額別回数')
