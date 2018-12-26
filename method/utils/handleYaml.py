import yaml

path = "config.yaml"
with open(path, 'r', encoding="utf-8") as cy:
    config_data = yaml.load(cy)


def get_config_file_limit():
    """
    config.yamlからfileLimit情報を取得する
    Returns
    -------
    file_limit : int
    """
    file_limit = config_data["logger"]["fileLimit"]
    try:
        file_limit = int(file_limit)
        if file_limit < 1:
            onetime_error_msgbox(f"config.yamlのfileLimitは1以上で設定してください。\nfileLimit：{file_limit}")
    except:
        onetime_error_msgbox(f"config.yamlのfileLimitは1以上で設定してください。\nfileLimit：{file_limit}")
    return file_limit


def get_config_directory_capacity():
    """
    config.yamlからdirectoryCapacity情報を取得する
    Returns
    -------
    directory_capacity : int
    """
    directory_capacity = config_data["logger"]["directoryCapacity"]
    try:
        directory_capacity = int(directory_capacity)
        if directory_capacity < 1:
            onetime_error_msgbox(f"config.yamlのdirectoryCapacityは最低限1以上で設定してください。\ndirectoryCapacity：{directory_capacity}")
    except:
        onetime_error_msgbox(f"config.yamlのdirectoryCapacityは最低限1以上で設定してください。\ndirectoryCapacity：{directory_capacity}")
    return directory_capacity


def get_config_output_flg():
    """
    config.yamlからoutputFlg情報を取得する
    Returns
    -------
    output_flg : boolean or int
        True, False, 1, 0が返却される
    """
    output_flg = config_data["logger"]["outputFlg"]
    if output_flg not in [True, False]:
        onetime_error_msgbox(f"config.yamlのoutputFlgはtrue or falseで設定してください。\noutputFlg：{output_flg}")
    return output_flg


def onetime_error_msgbox(msg):
    import wx
    """
    共通機能のエラー表示
    Parameters
    ----------
    msg : str
        エラーメッセージ
    """
    app = wx.App()
    wx.MessageBox(f"{msg}", "ERROR", wx.ICON_ERROR)
    app.MainLoop()
    wx.Exit()
