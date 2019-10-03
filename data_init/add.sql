desc app01_school_user;
desc app01_shop;
desc app01_school;

insert app01_school (school_name) values ('枣庄');

insert app01_student (tb_username, name, state, school_id)
 VALUES ('aaaklq','孔令谦',0,1),
        ('a','孔令谦',0,1);

insert into app01_shop values (1,'test1',1);

insert app01_studentshop (id, order_time, shop_id, student_id, money, order_number) VALUES
(1,'2019-10-3',1,2,100,'628051362784330536');


create procedure delete_all_stu_info()
begin

    delete from app01_studentshop where 1;
    delete from app01_shop where 1;
    delete from app01_student where 1;
    delete from app01_school where 1;

end;

drop procedure if exists delete_all_stu_info ;

call delete_all_stu_info();
