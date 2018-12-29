import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import matplotlib.pyplot as plt
import math
import wx
from matplotlib import rcParams
import matplotlib
from method.utils import chms_logger

logger = chms_logger.set_operate_logger(__name__)
matplotlib.interactive(True)
matplotlib.use('WXAgg')
rcParams.update({'figure.autolayout': True})


class UseGraph(wx.Panel):
    def __init__(self, parent, use_accounting_list):
        wx.Panel.__init__(self, parent=parent)
        plt.style.use('bmh')
        use = [use_accounting[0] for use_accounting in use_accounting_list]
        money = [use_accounting[1] for use_accounting in use_accounting_list]
        use_money_df = pd.DataFrame({"use": use, "money": money}, columns=["use", "money"])
        use_money_df["accum"] = np.cumsum(use_money_df["money"])
        use_money_df["accum_pa"] = use_money_df["accum"] / sum(money) * 100

        # matplotlib figure
        self.figure = Figure()
        self.ax1 = self.figure.subplots()
        self.ax1.bar(use, money, label=u'累計', width=-1, edgecolor='k')
        self.ax1.tick_params(axis="x", which="major", direction="in")
        self.ax1.set_xticklabels(use, rotation=270, fontsize='small')
        self.ax2 = self.ax1.twinx()
        self.ax2.plot(use, use_money_df["accum_pa"], c='k', marker='o', label=u'累積和')
        self.ax2.set_ylim([0, 100])
        self.ax2.set_yticks(np.arange(0, 101, 10))
        percent_labels = [f"{i}%" for i in np.arange(0, 101, 10)]
        self.ax2.set_yticklabels(percent_labels)
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
