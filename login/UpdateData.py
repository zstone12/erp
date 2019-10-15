import pandas as pd
import logging
from myuntil import Connect
import pymysql
import datetime
from tqdm import tqdm

def data_add(file_path):
    date = get_now_date()
    db, cursor = Connect().get_db_connection()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(file_path.split('/')[-1])
    df = pd.read_excel(file_path, names=['学校', '姓名', '用户名', '金额', '方式', '订单号', '店铺', '佣金'],
                       usecols=[0, 1, 2, 3, 4, 5, 6, 8]).dropna().reset_index()
    #call add_data('邓启义111','欣优佳99999999','一个无聊的笑话6666 ','贵大10','2019-10-4','563504271515080805',798);
    for index in tqdm(range(df.shape[0])):
        data = df.iloc[index]
        sql = '''
        call add_data('{}','{}','{} ','{}','{}','{}',{})
        '''.format(data['姓名'],data['店铺'],data['用户名'],data['学校'],date,data['订单号'],data['佣金'])
        cursor.execute(sql)
    db.commit()




def get_now_date():
    now = datetime.datetime.now()
    string = '{}-{}-{}'.format(now.year,now.month,now.day)
    return string

if __name__ == '__main__':
    print(get_now_date())