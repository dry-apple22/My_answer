import akshare as ak  #导入金融数据库，用于获取股票数据
from datetime import datetime, timedelta  #具体日期时间，计算时间间隔
import pandas as pd  #处理表格数据


def get_all_stock_daily(start_date=None, end_date=None):
    """
    获取全A股日频行情数据
    :param start_date: 开始日期(YYYY-MM-DD)
    :param end_date: 结束日期(YYYY-MM-DD)
    :return: DataFrame，全A股在上述日期的tick合集，日期相同的tick相邻
    """
    #测试用start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    if end_date is None:  #如果结束日期为空，就设为当前日期。
        end_date = datetime.now().strftime('%Y-%m-%d')  #获取系统时间，并格式化为日期
    if start_date is None:  #如果起始日期为空，就设为365天之前的日期。
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')  #

    try:  #以下代码可能运行失败
        # 获取所有A股代码
        stock_list = ak.stock_zh_a_spot()  #获取全A股实时行情，stock_list（DF类型）含列 代码，名称，最新价...
        codes = stock_list['代码'].tolist()  #提取‘代码’列转化为列表，['000001','600000',...]

        # 获取每只股票的日线数据
        all_data = []

        for code in codes:  #for code in ['bj430017','bj430047','bj430090','bj430139']:  #测试用
            df = ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date=end_date)  #获取单只股票的日频行情数据,df是二维数组，行索引为日期，列包括[open,high,low,close,...]
            df['code'] = code  #在最后添加一列code，值均为code
            all_data.append(df)  #每个元素是一只股票的df
            print(len(all_data))
            print('载入日线',code)
        print('获取数据成功！（get_all_stock_daily）')
        return pd.concat(all_data)  #合并all_data中所有股票的df，自动按相同列名日期对其数据，也就是日期相同的相邻。
    except Exception as e:  #上述try失败后
        print(f"获取数据失败: {e}")  #打印错误代码
        return None  #返回无