import pymysql


class Connect():

    @staticmethod
    def get_db_connection():
        db = pymysql.connect("129.204.185.247", "root", "erp2019/10/02", "erpDB")
        cursor = db.cursor()
        return db, cursor