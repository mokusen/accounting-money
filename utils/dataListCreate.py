def create_month():
    """
    月のデータリストを作成する

    Returns
    -------
    m_list : list型
        1月から12月分のデータを格納する
    """
    m_list = [str(month + 1) for month in range(12)]
    m_list.insert(0,'')
    return m_list

def create_day():
    """
    月のデータリストを作成する

    Returns
    -------
    m_list : list型
        1月から12月分のデータを格納する
    """
    d_list = [str(day + 1) for day in range(31)]
    d_list.insert(0,'')
    return d_list