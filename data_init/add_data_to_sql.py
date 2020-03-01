import pymysql
import pandas as pd
import openpyxl as pyx
from tqdm import tqdm
import logging

TEST = 1

class AddData2SQL(object):

    def __init__(self):
        self.school_id = 1
        self.stu_id = 1
        self.shop_id = 200
        self.ss_id = 1
        self._visible_list = self._get_visible_list()
        self.cursor, self.db = self._connect_to_sql()
        self._destory_db()
        self.shoping_id = -1
        self._test()



    @staticmethod
    def _connect_to_sql():
        '''
        connect to database and return cursor and db to commit data
        :return:
        '''
        cursor = db.cursor()
        return cursor,db

    @staticmethod
    def _get_visible_list():
        '''
        to get all visible shop and insert it to the shop
        :return: visible shop name list
        '''
        # wb = pyx.load_workbook('../data/刷单所有11.4最新唯一.xlsx')
        # sheets = wb.get_sheet_names()
        # visible_sheet = []
        # for sheet_name in sheets:
        #     if wb[sheet_name].sheet_state == 'visible' and sheet_name not in ['黑名单','注意事项截图']:
        #         visible_sheet.append(sheet_name)
        # # visible_sheet = ['162尚兔','175-TAWA帐篷+吸尘器+定位器+充气泵']
        # print(visible_sheet)
        return ['136-揽胜所有', '146-路特斯所有', '162尚兔', '175-TAWA帐篷+吸尘器+定位器+充气泵', '147-麦兜', '布莱希', '160-沙驰腾龙', '138老林二手手机', '老陈手机', '158-荣事达处理器', '170-欣优佳电视', '121-创佳电视', '127-京东玩具', '155-俏物唯品', '149-福州内衣', '177-指天下', '弘硕', '博菱除湿机', '103-GIH显示器', '148魔觉电视', '178-制写旗舰店', '101-beex旗舰店', '172-雅马哈雅悦专卖店', '102-beex电脑', '老郭平板', '韩京', '169-小宋平板', '179-众奇朱总电视', '104-KOIVIKDA官方企业店', '113-创彩彩电', '京东山居人家', '150-拼多多BEEX ', '110-柏尔显示器', '107-PFI旗舰店', '125-金汇佳', '173-医疗设备', '123-吉普官方', '熊大男鞋', '174-易品华禧', '171-新东腾', '129-聚利饮水机', '116-电动车', '144-李文杰手机', '老郭通瀚平板', '105-MAINGEAR笔记本', '老王悦动', '124-金创佳商贸', '166-拓谱申显示器', '131-君耿数码', '154-老王鄱阳县家具', '新维科', '112-陈海城衣服', '拼多多显理', '120-广州德雅电子', '122-华云数码家店', '165-提莫', '燕青家电', '167-王牌', '108-UOLUO优品', '111-标致', '依依', '捕虾船传媒', '168-小家电', '118-多乐加斯蒂专卖店', '126-金松银柏电器专营店', '128-京东一寸相思', '137-老郭小白兔', '157-全托', '152-拼多多欣沃斯', '114-达为电脑直销店', '106-MIUI厨房电器', '133-可乐法纳斯钢琴', '135-可乐音嘉架子鼓', '可乐婴儿车', '109-阿坤立酷', '京东路依', '115-德雅企业店广告机', '134-可乐艺无界', '119-梵公爵世家', '163-圣派尔旗舰店', '156-清厨恩旗舰店', '117-度安旗舰店', '椰子', '怡恋妈妈装', '176-真帅食品', '145-联显科技', '159-润芝堂', '153-拼丽旗舰店', '161-上海若之家', '151-拼多多共典旗舰店', '164-十分睡眠', '141-老刘东风', '140-老刘彬彬', '142-老刘佳裕', '139-老刘宾利来']


    def _insert_shop(self,shop_name,shop_set_id = -1):
        '''
        insert shop name and shop id plus 1
        :param shop_name:str
        :return:
        '''
        if shop_set_id == -1:
            self.shop_id += 1
            shop_id = self.shop_id
        else:
            shop_id = shop_set_id
        self.shoping_id = shop_id
        visible_list = self._visible_list
        if shop_name in visible_list:
            flag = 1
        else:
            flag = 0
        shop_name = str(shop_name).strip()
        sql = '''
        insert into app01_shop values ({},'{}',{});
        '''.format(shop_id,shop_name,flag)
        self.cursor.execute(sql)
        self.db.commit()

    def _insert_school(self,school):
        '''
        get school id if exist else to find id in database
        :param school: str school name
        :return: int:school id
        '''
        sql = '''
        select id from app01_school where school_name = '{}'
        '''.format(school)
        count = self.cursor.execute(sql)
        school = str(school).strip()
        if count == 0:
            self.school_id += 1
            sql = '''
            insert app01_school (id,school_name) values ({},'{}');
            '''.format(self.school_id,school)
            self.cursor.execute(sql)
            self.db.commit()
            return self.school_id
        else:
            data = self.cursor.fetchone()
            return data[0]

    def _insert_stu_info(self,name,tb_username,school):
        '''
        1.get school id in db
        2.insert student info into database
        :param name: str student name
        :param tb_username: str student taobao username
        :param school: str student school name
        :return: student id in db
        '''
        name = str(name).strip()
        tb_username = str(tb_username).strip()
        school = str(school).strip()
        school_id = self._insert_school(school)
        sql = '''
        select id from app01_student 
        where name = '{}' and tb_username = '{}' and school_id = {}
        '''.format(name,tb_username,school_id)
         
        line_num = self.cursor.execute(sql)
        if line_num == 0:
            self.stu_id += 1
            sql = '''
            insert app01_student (id,tb_username, name, state, school_id)
            VALUES ({},'{}','{}',0,{})
            '''.format(self.stu_id,tb_username,name,school_id)
            self.cursor.execute(sql)
            self.db.commit()
            return self.stu_id
        else:
            return self.cursor.fetchone()[0]

    def _insert_stu_school(self,name,tb_username,school,used_time,order_num,money):
        '''
        use it and easy add stu info
        :param name: str: student name
        :param tb_username: str: taobao user name
        :param school: str school name
        :param used_time: str type is yyyy-mm-dd
        :param order_num: str the number of order
        :param money: int used money
        :return:
        '''
        name = str(name).strip()
        tb_username = str(tb_username).strip()
        school = str(school).strip()
        if type(used_time) in [str,int]:
            used_time = str(used_time).strip()
        else:
            print(type(used_time))
            used_time = '{}-{}-{}'.format(used_time.year,used_time.month,used_time.day)
        order_num = str(order_num).strip()
        money = int(money)
        stu_id = self._insert_stu_info(name, tb_username, school)
        self.ss_id += 1
        sql = '''
        insert app01_studentshop (id, order_time, shop_id, student_id, money, order_number) VALUES
        ({},'{}',{},{},{},'{}')
        '''.format(self.ss_id,used_time,self.shoping_id,stu_id,money,order_num)
         
        self.cursor.execute(sql)
        self.db.commit()

    def _destory_db(self):
        pass
        # self.cursor.execute('call delete_all_stu_info()')
        # self.db.commit()

    def main(self):
        # names = ['日期', '学校', '姓名', '淘宝账号', '支付款', '订单号'],
        df_dict = pd.read_excel('../data/刷单所有11.4最新唯一.xlsx', None, encoding='gbk',usecols=[0,1,2,3,4,5,6,7])
        # print(df_dict)
        for df_name in tqdm(df_dict):
            if df_name == '黑名单' or df_name == '注意事项截图':
                continue
            try:
                try:
                    shop_id = int(df_name[:3])
                except ValueError:
                    shop_id = -1
                self._insert_shop(df_name,shop_id)
            except Exception as e:
                print(e,'fuck')
            shop_list = df_dict[df_name].values.tolist()
            for stu_values in tqdm(shop_list):
                for i in range(2):
                    try:
                        self._insert_stu_school(stu_values[2],stu_values[3],stu_values[1],stu_values[0],
                                            stu_values[6],stu_values[4])
                        if i == 1:
                            print(1)
                        break
                    except ValueError as e:
                        stu_values[6] = stu_values[5]
                    except Exception as e:
                        print(stu_values,df_name,'error')
                        stu_values = stu_values[1:]
                        print('er',e,stu_values)


    def _test(self):
        self.main()
if __name__ == '__main__':
    AddData2SQL()
