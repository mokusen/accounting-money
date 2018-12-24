import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import matplotlib.pyplot as plt
import math
import wx
from matplotlib import rcParams
import matplotlib
from method.utils import logger

logger = logger.set_operate_logger(__name__)
matplotlib.interactive(True)
matplotlib.use('WXAgg')
rcParams.update({'figure.autolayout': True})


class AmountGraph(wx.Panel):
    def __init__(self, parent, all_data):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        plt.style.use('bmh')

        # matplotlib figure
        self.figure = Figure()
        self.ax = self.figure.subplots()
        test = [item[2] for item in all_data]
        # FIXME: やばい
        if test == []:
            a = 1000
        else:
            a = max(test)
        b = round(a / 1000)
        self.ax.hist(test, histtype='barstacked', bins=b, range=(0, b*1000), rwidth=1)

        # canvas
        self.canvas = FigureCanvasWxAgg(self, wx.ID_ANY, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(100, 255, 255))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
