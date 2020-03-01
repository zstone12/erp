import pymysql


def get_sql_conn():
    """
    获取数据库连接
    """
    
    cursor = conn.cursor()
    return conn, cursor


def get_index_dict(cursor):
    """
    获取数据库对应表中的字段名
    """
    index_dict = dict()
    index = 0
    for desc in cursor.description:
        index_dict[desc[0]] = index
        index = index + 1
    return index_dict


def get_dict_data_sql(cursor, sql):
    """
    运行sql语句，获取结果，并根据表中字段名，转化成dict格式（默认是tuple格式）
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    index_dict = get_index_dict(cursor)
    print(index_dict)
    res = []
    for datai in data:
        resi = dict()
        for indexi in index_dict:
            resi[indexi] = datai[index_dict[indexi]]
        res.append(resi)
    return res


def main():
    con, cursor = get_sql_conn()
    sql = "select max(ss.order_time) as last_time ,stu.name,stu.tb_username,shop_name,school.school_name from app01_studentshop ss join app01_shop shop on ss.shop_id = shop.id join app01_student stu on ss.student_id = stu.id join app01_school sch on stu.school_id = sch.id a01s on stu.school_id = a01s.id    where stu.name = '翁荷花' and shop.cooperate_state = 1 group by ss.student_id, ss.shop_id order by  stu.tb_username;"
    sql="select max(ss.order_time) as last_time ,stu.name,stu.tb_username,shop_name,school_name from app01_studentshop ss join app01_shop shop on ss.shop_id = shop.id join app01_student stu on ss.student_id = stu.id join app01_school sch on ss.student_id = sch.user where stu.name = '翁荷花' and shop.cooperate_state = 1 group by ss.student_id, ss.shop_id order by  stu.tb_username;"
    sql ="select max(ss.order_time) as last_time ,stu.name,stu.tb_username,shop_name,sch.school_name from app01_studentshop ss join app01_shop shop on ss.shop_id = shop.id join app01_student stu on ss.student_id = stu.id join app01_school sch on ss.student_id = sch.user_id where stu.name = '翁荷花' and shop.cooperate_state = 1 group by ss.student_id, ss.shop_id order by  stu.tb_username;"
    sql="select max(ss.order_time) as last_time ,stu.name,stu.tb_username,shop_name,school_name from app01_studentshop ss join app01_shop shop on ss.shop_id = shop.id join app01_student stu on ss.student_id = stu.id join app01_school sch on stu.school_id = sch.id where stu.name = '翁荷花' and shop.cooperate_state = 1 group by ss.student_id, ss.shop_id order by  stu.tb_username;"

    sql2='''
    select any_value(total.name),any_value(total.shop_name),any_value(total.tb_username),any_value(total.school_name) from (
select
       app01_student.name,
       app01_shop.shop_name,
       app01_student.tb_username,
       school.school_name
from app01_shop,app01_student
    join app01_school school on app01_student.school_id = school.id
where app01_student.name='翁荷花' and app01_shop.cooperate_state=1
and school_id = 2
union
select distinct stu.name,shop.shop_name,tb_username,school_name
from app01_studentshop ss
join app01_shop shop on ss.shop_id = shop.id
join app01_student stu on ss.student_id = stu.id
join app01_school school on stu.school_id = school.id
where stu.name = '翁荷花' and school_id = 2) total
group by total.tb_username,total.shop_name having count(*) <2;
    '''
    #print(sql2)
    res = get_dict_data_sql(cursor, sql2)
    print(res)

if __name__ == '__main__':
    main()
