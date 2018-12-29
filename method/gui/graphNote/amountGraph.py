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


class AmountGraph(wx.Panel):
    def __init__(self, parent, all_data):
        wx.Panel.__init__(self, parent=parent)
        plt.style.use('bmh')

        # matplotlib figure
        self.figure = Figure()
        self.ax = self.figure.subplots()
        money_list = [money[2] for money in all_data]
        if money_list == []:
            max_money = 1000
        else:
            max_money = max(money_list)
        hist_bins = round(max_money / 1000)
        self.ax.hist(money_list, histtype='barstacked', bins=hist_bins, range=(0, hist_bins*1000), rwidth=1)

        # canvas
        self.canvas = FigureCanvasWxAgg(self, wx.ID_ANY, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(100, 255, 255))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
