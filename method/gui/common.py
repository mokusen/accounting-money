import wx


def defalut_font_size():
    return wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Meiryo UI')


def main_defalut_font_size():
    return wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Meiryo UI')


def get_icon():
    return wx.Icon('method/image/chms.ico', wx.BITMAP_TYPE_ICO)


def search_frame_size():
    return (625, 631)


def search_use_display_size():
    current_display_size = wx.DisplaySize()
    use_display_size = ((current_display_size[0] - 1200) / 2, (current_display_size[1] - 631 - 40) / 2)
    return use_display_size


def graph_frame_size():
    return (650, 547)


def graph_use_display_size():
    current_display_size = wx.DisplaySize()
    use_display_size = ((current_display_size[0] - 1200) / 2 + 625, (current_display_size[1] - 631 - 40) / 2)
    return use_display_size


def statistics_ctrl_size():
    return (200, 409)


def statistics_data_ctrl_size():
    return (200, 200)
