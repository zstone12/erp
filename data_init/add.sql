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


select count(*) from app01_studentshop;

select ss.order_time,stu.name,stu.tb_username,shop_name from app01_studentshop ss
join app01_shop shop on ss.shop_id = shop.id
join app01_student stu on ss.student_id = stu.id
where stu.name = '倪诗思' order by ss.order_time;

select max(ss.order_time) as last_time ,stu.name,stu.tb_username,shop_name
from app01_studentshop ss
join app01_shop shop on ss.shop_id = shop.id
join app01_student stu on ss.student_id = stu.id
where stu.name = '翁荷花' and shop.cooperate_state = 1
group by ss.student_id, ss.shop_id order by  stu.tb_username;

update app01_shop set cooperate_state = 0 where id > 200;


select distinct stu.tb_username,stu.school_id
from app01_studentshop ss
join app01_shop shop on ss.shop_id = shop.id
join app01_student stu on ss.student_id = stu.id
where stu.name = '翁荷花' and school_id = 2;

select shop_name from app01_shop where id not in (select distinct ss.shop_id
from app01_studentshop ss
join app01_shop shop on ss.shop_id = shop.id
join app01_student stu on ss.student_id = stu.id
where stu.tb_username = 'tb971437173')  and cooperate_state = 1;

select shop_name from app01_shop where shop_name like '%欣优佳%';


drop procedure if exists add_data;
create procedure add_data(
in stu_name varchar(100)character set gbk,
in shop_name1 varchar(100) character set gbk,
in tb_username1 varchar(100) character set gbk,
in school varchar(100) character set gbk,
in used_time varchar(100) character set gbk,
in order_num varchar(100) character set gbk,
in money int
)
begin
    declare shop_id1 int;
    declare shop_count int;
    declare stu_count int;
    declare school_id int;
    declare school_count int;
    declare stu_id1 int;
    declare ss_count int;
    select count(*) from app01_shop where shop_name like concat('%',shop_name1,'%') into shop_count;
    if shop_count = 0
        then insert app01_shop (shop_name, cooperate_state) values (shop_name1,1);
    end if ;
    select count(*) from app01_school where school_name=school into school_count;
    if school_count=0 then
        insert app01_school (school_name) values (school);
    end if;
    select id from app01_school where school_name = school limit 1 into school_id;
    select id from app01_shop where shop_name like concat('%',shop_name1,'%') limit 1 into shop_id1;
#     select shop_id1;
    select count(*) from app01_student where tb_username = tb_username1 into stu_count;
    if stu_count=0 then
        insert into app01_student (tb_username, name, state, school_id) values (tb_username1,stu_name,0,school_id);
    end if;
    select id from app01_student where tb_username = tb_username1 limit 1 into stu_id1;
    select count(*) from app01_studentshop where student_id = stu_id1 and shop_id = shop_id1 and order_time = used_time limit 1 into ss_count;
    if ss_count = 0 then
        insert app01_studentshop (order_time, shop_id, student_id, money, order_number) values (used_time,shop_id1,stu_id1,money,order_num);
    end if;
end;
call add_data('邓启义111','欣优佳99999999','一个无聊的笑话6666 ','贵大10','2019-10-4','563504271515080805',798);



select * from app01_studentshop where order_time='2019-10-8';

select shop_name from app01_shop where shop_name like '%揽胜所有%';


delete from app01_studentshop where order_time='2019-10-8';

select id from app01_student order by id desc ;





update app01_shop set cooperate_state = 1 where 1;

create procedure test()
# begin
#     declare shop_count int;
#     select count(*) from app01_shop
# end;
select any_value(total.name),any_value(total.shop_name),any_value(total.tb_username),any_value(total.school_name) from (
select
       app01_student.name,
       app01_shop.shop_name,
       app01_student.tb_username,
       school.school_name
from app01_shop,app01_student
    join app01_school school on app01_student.school_id = school.id
where app01_student.name='倪诗思' and app01_shop.cooperate_state=1
union
select distinct stu.name,shop.shop_name,tb_username,school_name
from app01_studentshop ss
join app01_shop shop on ss.shop_id = shop.id
join app01_student stu on ss.student_id = stu.id
join app01_school school on stu.school_id = school.id
where stu.name = '倪诗思') total
group by total.tb_username,total.shop_name,total.school_name,total.tb_username having count(*) <2;


update app01_shop set cooperate_state = 0 where id > 40;

show tables ;

select distinct tb_username,name,a01s.school_name,(select count(distinct shop_id)) as count_ from app01_studentshop ss
            join app01_student stu on ss.student_id = stu.id
            join app01_shop shop on ss.shop_id = shop.id
            join app01_school a01s on stu.school_id = a01s.id
            where shop.shop_name != 'abc' and school_id in (1,2,3) group by tb_username, name, school_name having count_ > 1 order by count_ asc limit 500;

call delete_all_stu_info();

select  count(*), shop_id from erpData.app01_studentshop group by shop_id;

select tb_username,name,a01s.school_name,stu.state,count(distinct shop_id) as count_ from app01_studentshop ss
                      join app01_student stu on ss.student_id = stu.id
                      join app01_shop shop on ss.shop_id = shop.id
                      join app01_school a01s on stu.school_id = a01s.id
                      where shop.shop_name != '路特斯所有' and school_id in (1,2,3) and stu.state=0 group by tb_username, name, school_name having count_ > 1 order by count_ asc limit 500;


create index ss on app01_studentshop(shop_id,student_id);
create index shop1 on erpDB.app01_shop(id);
create index stu1 on erpDB.app01_shop(id,shop_name);
select count(*) from app01_studentshop;

drop index ss1 on app01_studentshop;

update app01_student set app01_student.remark='' where 1;

select distinct tb_username,name,any_value(stu.remark) as remark,a01s.school_name,count(distinct shop_id) as count_, max(ss.order_time) as time_ from app01_studentshop ss
                    join app01_student stu on ss.student_id = stu.id
                    join app01_shop shop on ss.shop_id = shop.id
                    join app01_school a01s on stu.school_id = a01s.id
                    where school_id in (2,3,4) and stu.state=0 and student_id not in(select distinct student_id from erpDB.app01_studentshop where shop_name ='116-电动车') group by tb_username, name, school_name having count_ > 1 order by count_,time_ asc limit 50;


show create table update_file_md5;

CREATE TABLE `update_file_md5` (
  `md5` varchar(300) NOT NULL,
  PRIMARY KEY (`md5`)
);