import wx


""" FONT SIZE SETTING """


def defalut_font_size():
    return wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Meiryo UI')


def main_defalut_font_size():
    return wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Meiryo UI')


""" ICON SETTING """


def get_icon():
    return wx.Icon('method/image/chms.ico', wx.BITMAP_TYPE_ICO)


""" FRAME SIZE SETTING """


def main_frame_size():
    return (750, 300)


def registration_frame_size():
    return (560, 390)


def search_frame_size():
    return (625, 730)


def graph_frame_size():
    return (650, 547)


def detail_frame_size():
    return (300, 300)


def csvdb_frame_size():
    return (500, 310)


""" DISPLAY POS SETTING """


def search_use_display_size():
    current_display_size = wx.DisplaySize()
    use_display_size = ((current_display_size[0] - 1200) / 2, (current_display_size[1] - 730 - 40) / 2)
    return use_display_size


def graph_use_display_size():
    current_display_size = wx.DisplaySize()
    use_display_size = ((current_display_size[0] - 1200) / 2 + 625, (current_display_size[1] - 730 - 40) / 2)
    return use_display_size


""" LISTCTRL SIZE SETTING """


def search_ctrl_size():
    return (600, 523)


def statistics_ctrl_size():
    return (190, 460)


def statistics_data_ctrl_size():
    return (190, 237)


""" DEFAULT ITEM SIZE SETTING """


def main_button_size():
    return (200, 100)


def regi_statitext_size():
    return (100, 23)


def regi_numtext_size():
    return (30, 23)


def regi_button_size():
    return (200, 46)


def detail_form_size():
    return (100, 25)


def detail_text_size():
    return (50, 25)


def detail_button_size():
    return (100, 25)
