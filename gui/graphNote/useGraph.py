import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import matplotlib.pyplot as plt
import math
import wx
from matplotlib import rcParams
import matplotlib
from utils import logger

logger = logger.set_operate_logger(__name__)
matplotlib.interactive(True)
matplotlib.use('WXAgg')
rcParams.update({'figure.autolayout': True})


class UseGraph(wx.Panel):
    def __init__(self, parent, title_accounting_list):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        plt.style.use('bmh')
        xxx = [year_accounting[0] for year_accounting in title_accounting_list]
        yyy = [year_accounting[1] for year_accounting in title_accounting_list]
        sample_df = pd.DataFrame({"use": xxx, "money": yyy}, columns=["use", "money"])
        sample_df["accum"] = np.cumsum(sample_df["money"])
        sum_yyy = sum(yyy)
        sample_df["accum_pa"] = sample_df["accum"] / sum_yyy * 100

        # matplotlib figure
        self.figure = Figure()
        self.ax1 = self.figure.subplots()
        self.ax1.bar(xxx, sample_df["money"], label=u'累計', width=-1, edgecolor='k')
        self.ax1.tick_params(axis="x", which="major", direction="in")
        self.ax1.set_xticklabels(xxx, rotation=270, fontsize='small')
        self.ax2 = self.ax1.twinx()
        self.ax2.plot(xxx, sample_df["accum_pa"], c='k', marker='o', label=u'累積和')
        self.ax2.set_ylim([0, 100])
        self.ax2.set_yticks(np.arange(0, 101, 10))
        percent_labels = [f"{i}%" for i in np.arange(0, 101, 10)]
        self.ax2.set_yticklabels(percent_labels)
        # TODO: 調整
        try:
            self.figure.legend(bbox_to_anchor=(1, 0.05), loc='upper right', ncol=2)
        except:
            pass

        # canvas
        self.canvas = FigureCanvasWxAgg(self, wx.ID_ANY, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(100, 255, 255))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
