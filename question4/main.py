from datetime import datetime, timedelta
from getData_A import get_all_stock_daily  #数据获取
from database import StockDatabase  #数据存储
from data_processor import process_data, validate_data  #数据清洗


def main():
    #初始化一个数据库对象
    db = StockDatabase(db_path='D:/My_code/pyTorch_project/database/stock_data.db')

    # 检查是否需要全量恢复
    if db.get_last_date() is None:
        print("数据库为空，开始全量恢复数据...")
        if not db.recover_data():  #开始恢复
            print("全量恢复失败！")
            return
        print("全量恢复成功！")

    # 增量更新：获取最新数据
    last_date = db.get_last_date()  #最新数据日期
    start_date = (datetime.strptime(last_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
    #start_date = (datetime.strptime(last_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')  #测试用
        #开始增量记录的日期为最新日期+1，避免重复获取数据

    print(f"开始获取增量数据，从 {start_date} 至今...")
    new_data = get_all_stock_daily(start_date=start_date)  #获取最新一日数据

    if new_data is not None:  #不为空
        print('最新一日增量数据获取成功',new_data)
        processed_data = process_data(new_data)
        print('数据清洗后结果',processed_data)
        #验证数据有效性
        is_valid, msg = validate_data(processed_data)

        if is_valid:  #有效
            print("增量数据有效（validate_data验证）")
            if db.save_data(processed_data):
                print("增量数据保存成功！（save_data）")
            else:
                print("增量数据保存失败，尝试全量恢复...")
                db.recover_data()
        else:  #无效
            print(f"增量数据无效: {msg}")
    else:
        print("获取增量数据失败")


if __name__ == '__main__':
    main()