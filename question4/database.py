import sqlite3
import pandas as pd
from datetime import datetime
from getData_A import get_all_stock_daily


class StockDatabase:
    def __init__(self, db_path='stock_data.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_daily (
                date TEXT,
                code TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                amount REAL,
                outstanding_share REAL,
                turnover REAL,
                PRIMARY KEY (date, code)
                )
        ''')
        conn.commit()
        conn.close()

    def save_data(self, df):
        """保存数据到数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            df.to_sql('stock_daily', conn, if_exists='append', index=False)
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # 忽略重复数据
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False

    def save_data(self, df):
        """
        保存数据到数据库
        """
        try:
            conn = sqlite3.connect(self.db_path)  #建立连接
            df.to_sql(  #将df写入数据库中的表
                'stock_daily',       #表名
                conn,                #数据库连接对象（实例）
                if_exists='append',  #表存在，就加入数据
                index=False          #不写入df的索引列
            )
            conn.close()  #关闭连接
            return True  #成功！
        except sqlite3.IntegrityError:  #IntegrityError此错误为违反主键唯一原则
            # 重复写入数据时，也算作成功
            return True  #成功！
        except Exception as e:
            print(f"保存数据失败: {e}")  #打印错误
            return False  #失败！

    def recover_data(self, start_date=None, end_date=None):
        """
        数据恢复：重新获取并保存所有数据
        """
        df = get_all_stock_daily(start_date, end_date)  #重新获取之前所有日频行情数据
        if df is not None:  #获取成功
            print('日频数据成功调入内存！（recover_data）')
            conn = sqlite3.connect(self.db_path)  #建立连接
            cursor = conn.cursor()  #创建游标
            cursor.execute('DELETE FROM stock_daily')  # 清空表
            conn.commit()  #提交修改
            result = self.save_data(df)  #调用保存数据进数据库函数
            conn.close()
            if result is True:
                print('数据全面恢复成功（recover_data）')
                return True  #恢复成功
            else:
                print('数据全面恢复失败（recover_data）')
                return False  #恢复失败
        print('数据全面恢复失败（recover_data）')
        return False

    def get_last_date(self):
        """
        获取数据库中最新日期
        Returns:
            str/None: 返回YYYY-MM-DD格式的日期字符串，若表为空则返回None
        """
        conn = sqlite3.connect(self.db_path)  #建立连接
        print('连接数据库成功！（get_last_date）')
        cursor = conn.cursor()  #创建游标
        cursor.execute('SELECT MAX(date) FROM stock_daily')  #选择日期最新的一条
        last_date = cursor.fetchone()[0]  #从SQLite缓冲区提取一行到python内存
        print("目前数据库中的最新日期：",last_date)
        conn.close()
        return last_date