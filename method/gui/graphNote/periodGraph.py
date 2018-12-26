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


class PeriodGraph(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        plt.style.use('bmh')

        # matplotlib figure
        year_list = [item[2] for item in test]
        year_list = list(set(year_list))
        year_list.sort()
        month_list = [num for num in range(1, 13)]
        use_list = [item[0] for item in test]
        use_list = list(set(use_list))
        use_list.sort()

        data_list = {use: [[0 for month in month_list] for year in year_list] for use in use_list}

        for item in test:
            for y_index, year in enumerate(year_list):
                if item[2] == year:
                    for month in month_list:
                        if item[3] == month:
                            for use in use_list:
                                if item[0] == use:
                                    data_list[use][y_index][month - 1] = item[1]

        data_print_list = [f"{year}/{month}" for year in year_list for month in month_list]

        plt.style.use('bmh')
        self.figure = Figure()
        self.ax1 = self.figure.subplots()
        all_list = np.array([0 for month in month_list for year in year_list])
        for use in use_list:
            use_data = []
            for data in data_list[use]:
                use_data.extend(data)
            use_data = np.array(use_data)
            all_list += use_data
            self.ax1.plot(data_print_list, use_data)
            self.ax1.set_xticklabels(data_print_list, rotation=270, fontsize='small')
        self.ax2 = self.ax1.twinx()
        res = np.cumsum(all_list)
        self.ax2.plot(data_print_list, res, color="red")

        # canvas
        self.canvas = FigureCanvasWxAgg(self, wx.ID_ANY, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(100, 255, 255))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
