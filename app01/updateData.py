import sys
sys.path.append('..')
import pandas as pd
from myutil import Connect
import datetime
from tqdm import tqdm
import logging
import os


def data_add(file_path):
    date = get_now_date()
    success, fail = logger_init(date)
    db, cursor = Connect().get_db_connection()
    df = pd.read_excel(file_path, names=['学校', '姓名', '用户名', '金额', '方式', '订单号', '店铺', '佣金'],
                       usecols=[0, 1, 2, 3, 4, 5, 6, 8]).dropna().reset_index()
    #call add_data('邓启义111','欣优佳99999999','一个无聊的笑话6666 ','贵大10','2019-10-4','563504271515080805',798);
    for index in tqdm(range(df.shape[0])):
        try:
            data = df.iloc[index]
            sql = '''
            call add_data('{}','{}','{} ','{}','{}','{}',{})
            '''.format(data['姓名'],data['店铺'],data['用户名'],data['学校'],date,data['订单号'],data['佣金'])
            cursor.execute(sql)
            success.warning(str(data.values))
        except Exception as e:
            print(e)
            success.warning(str(e))
    db.commit()


def logger_init(date):
    if not os.path.exists('../static/logger/{}'.format(date)):
        os.mkdir('../static/logger/{}'.format(date))
    fail_logger = logging.getLogger('fail')
    fail_logger.addHandler(logging.FileHandler('../static/logger/{}/fail.log'.format(date)))
    success_logger = logging.getLogger('success')
    success_logger.addHandler(logging.FileHandler('../static/logger/{}/success.log'.format(date)))
    return success_logger, fail_logger


def get_now_date():
    now = datetime.datetime.now()
    string = '{}-{}-{}'.format(now.year,now.month,now.day)
    return string


if __name__ == '__main__':
    data_add(r'C:\Users\song\PycharmProjects\erp\static\daily update data\今日全部.xlsx')