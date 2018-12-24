def adjust_accounting(adjust_list):
    """
    sql側に渡す前に型変換を行う

    Parameters
    ----------
    adjust_list : list型
        [id, use, money, year, month, day]

    Returns
    -------
    adjust_list : list型
        [id(int), use(str), money(int), year(int), month(int), day(int)]

    """
    adjust_list[0] = int(adjust_list[0])
    adjust_list[2] = int(adjust_list[2])
    adjust_list[3] = int(adjust_list[3])
    adjust_list[4] = int(adjust_list[4])
    adjust_list[5] = int(adjust_list[5])
    return adjust_list
