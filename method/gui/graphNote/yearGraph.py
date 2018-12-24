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


class YearGraph(wx.Panel):
    def __init__(self, parent, year_accounting_list):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        plt.style.use('bmh')
        xx = [year_accounting[0] for year_accounting in year_accounting_list]
        yy = [year_accounting[1] for year_accounting in year_accounting_list]
        ave_yy = [int(np.average(yy)) for _ in range(len(xx))]

        # matplotlib figure
        self.figure = Figure()
        self.subplot = self.figure.add_subplot(111)
        self.subplot.plot(xx, yy, marker='o', label=u'課金額')
        self.subplot.plot(xx, ave_yy, marker='o', label=u'平均課金額')
        self.subplot.legend(bbox_to_anchor=(1, -0.1), loc='upper right', ncol=2)

        # canvas
        self.canvas = FigureCanvasWxAgg(self, wx.ID_ANY, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(100, 255, 255))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
