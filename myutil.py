import pymysql


class Connect():

    @staticmethod
    def get_db_connection():
        db = pymysql.connect()
        cursor = db.cursor()
        return db, cursor
