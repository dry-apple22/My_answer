import pandas as pd

"""
1.数据完整性验证validate_data
2.数据格式标准化process_data
"""


def validate_data(df):
    """
    验证数据完整性
    :param df: 待验证的数据
    :return: (bool, str) 是否有效, 错误信息。即(bool, message) 元组
    """
    required_columns = ['date', 'code', 'open', 'high', 'low', 'close', 'volume']  #必要字段，和数据库表结构完全一致

    # 检查必要列是否存在
    if not all(col in df.columns for col in required_columns):
        return False, "缺少必要列"  #无效！

    # 检查空值
    if df[required_columns].isnull().any().any():  #df[required_columns]返回一个包含指定col的新df
        # 第一个any()检查每列是否有空值，返回Series。第二个检查Series中是否有True
        return False, "存在空值"  #无效！

    # 检查价格合理性
    if (df['close'] <= 0).any():  #如果任何一个close非正
        return False, "收盘价有非正值"  #无效！

    return True, "数据有效"


def process_data(df):
    """
    数据处理(清洗)：规范列名和数据类型
    :param df: 原始DataFrame
    :return: 处理后的标准化DataFrame
    """
    df = df.copy()  #避免修改原始的df
    if '日期' in df.columns:  #存在日期列
        df.rename(columns={'日期': 'date'}, inplace=True)  #就重命名为date，implace为True即直接修改当前df
    if '代码' in df.columns:
        df.rename(columns={'代码': 'code'}, inplace=True)

    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        #to_datetime()智能解析各种日期格式。strftime()统一转为‘YYYY-MM-DD’字符串，字符串日期可以直接比较，且SQLite没有原生datetime
    return df[['date', 'code', 'open', 'high', 'low', 'close', 'volume']]