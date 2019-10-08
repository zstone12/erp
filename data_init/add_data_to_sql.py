import pymysql
import pandas as pd
import openpyxl as pyx
from tqdm import tqdm

TEST = 1

class AddData2SQL(object):

    def __init__(self):
        self.school_id = 1
        self.stu_id = 1
        self.shop_id = 1
        self.ss_id = 1
        self._visible_list = self._get_visible_list()
        self.cursor, self.db = self._connect_to_sql()
        self._destory_db()
        self._test()

    @staticmethod
    def _connect_to_sql():
        '''
        connect to database and return cursor and db to commit data
        :return:
        '''
        db = pymysql.connect("123.56.162.193", "root", "erp2019/10/02", "erpDB")
        cursor = db.cursor()
        return cursor,db

    @staticmethod
    def _get_visible_list():
        '''
        to get all visible shop and insert it to the shop
        :return: visible shop name list
        '''
        wb = pyx.load_workbook('./data/刷单所有.xlsx')
        sheets = wb.get_sheet_names()
        visible_sheet = []
        for sheet_name in sheets:
            if wb[sheet_name].sheet_state == 'visible' and sheet_name not in ['黑名单','注意事项截图']:
                visible_sheet.append(sheet_name)
        return visible_sheet

    def _insert_shop(self,shop_name):
        '''
        insert shop name and shop id plus 1
        :param shop_name:str
        :return:
        '''
        self.shop_id += 1
        visible_list = self._visible_list
        if shop_name in visible_list:
            flag = 1
        else:
            flag = 0
        shop_name = shop_name.strip()
        sql = '''
        insert into app01_shop values ({},'{}',{});
        '''.format(self.shop_id,shop_name,flag)
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
        school = school.strip()
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
        name = name.strip()
        tb_username = tb_username.strip()
        school = school.strip()
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
        name = name.strip()
        tb_username = tb_username.strip()
        school = school.strip()
        used_time = used_time.strip()
        order_num = order_num.strip()
        money = int(money)
        stu_id = self._insert_stu_info(name, tb_username, school)
        self.ss_id += 1
        sql = '''
        insert app01_studentshop (id, order_time, shop_id, student_id, money, order_number) VALUES
        ({},'{}',{},{},{},'{}')
        '''.format(self.ss_id,used_time,self.shop_id,stu_id,money,order_num)
         
        self.cursor.execute(sql)
        self.db.commit()

    def _destory_db(self):
        self.cursor.execute('call delete_all_stu_info()')
        self.db.commit()

    def main(self):
        df_dict = pd.read_excel('./data/刷单所有.xlsx', None, encoding='gbk',
                                names=['日期', '学校', '姓名', '淘宝账号', '支付款', '订单号'],usecols=[0,1,2,3,4,6])
        try:
            del df_dict['注意事项截图']
        except ValueError:
            pass
        for df_name in tqdm(df_dict):
            if df_name == '黑名单' or df_name == '注意事项截图':
                continue
            try:
                self._insert_shop(df_name)
            except Exception as e:
                print(e)
            shop_list = df_dict[df_name].dropna().values.tolist()
            for stu_values in shop_list:
                try:
                    self._insert_stu_school(stu_values[2],stu_values[3],stu_values[1],stu_values[0],
                                        stu_values[5],stu_values[4])
                except Exception as e:
                    # print(stu_values,df_name,'error')
                    pass


    def _test(self):
        self.main()

if __name__ == '__main__':
    AddData2SQL()