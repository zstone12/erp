# login/views.py
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm
from .forms import RegisterForm
from .search import get_sql_conn, get_dict_data_sql
from .UpdateData import data_add
from app01 import models
from login.models import User

import json
import datetime
import hashlib


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    shop_list = models.Shop.objects.all()
    return render(request, 'login/index.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


def ajaxsearch(request):
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return json.JSONEncoder.default(self, obj)

    user_name = request.POST.get("username").strip()

    print(user_name)
    con, cursor = get_sql_conn()
    sql = "select max(ss.order_time) as last_time ,stu.name,stu.tb_username,shop_name,school_name from app01_studentshop ss join app01_shop shop on ss.shop_id = shop.id join app01_student stu on ss.student_id = stu.id join app01_school sch on stu.school_id = sch.id where stu.name = '{}' and shop.cooperate_state = 1 group by ss.student_id, ss.shop_id order by  stu.tb_username;".format(
        user_name)

    # sql1 = "select shop_name from app01_shop where id not in (select distinct ss.shop_id from app01_studentshop ss join app01_shop shop on ss.shop_id = shop.id join app01_student stu on ss.student_id = stu.id where stu.tb_username = 'tb971437173')  and cooperate_state = 1;"
    res = get_dict_data_sql(cursor, sql)
    return HttpResponse(json.dumps(res, cls=DateEncoder, ensure_ascii=False))  # jq那边在 用js的反序列方法转换即可


def test(request):
    # tb_names = set()
    # for i in res:
    #     tb_names.add(i['tb_username'])
    # tb_names = list(tb_names)
    #
    # tb_usernames={}
    # for i in tb_names:
    #     student = models.Student.objects.filter(tb_username=i).first()
    #     tb_usernames[i]={'used_shop':[],'unused_shop':[],'school':student.school.school_name}
    #
    # for i in res:
    #     tb_usernames[i['tb_username']]['used_shop'].append(
    #             i['shop_name']
    #         )
    #
    # sql2 = '''
    #         select any_value(total.name) as total_name,any_value(total.shop_name) as shop_name,any_value(total.tb_username) as tb_username,any_value(total.school_name) as school_name from (
    # select
    #        app01_student.name,
    #        app01_shop.shop_name,
    #        app01_student.tb_username,
    #        school.school_name
    # from app01_shop,app01_student
    #     join app01_school school on app01_student.school_id = school.id
    # where app01_student.name='{}' and app01_shop.cooperate_state=1
    # union
    # select distinct stu.name,shop.shop_name,tb_username,school_name
    # from app01_studentshop ss
    # join app01_shop shop on ss.shop_id = shop.id
    # join app01_student stu on ss.student_id = stu.id
    # join app01_school school on stu.school_id = school.id
    # where stu.name = '{}') total
    # group by total.tb_username,total.shop_name,total.school_name,total.tb_username having count(*) <2;'''.format(
    #     user_name,
    #     user_name)
    # res2 = get_dict_data_sql(cursor, sql2)  # list
    #
    # for j in res2:
    #     tb_usernames[j['tb_username']]['unused_shop'].append(
    #         j['shop_name']
    #     )
    # print(tb_usernames)
    return render(request, "login/test.html")


def ajaxsearchtwo(request):
    con, cursor = get_sql_conn()
    user_name = request.POST.get("username").strip()

    res = {'das': 'asdas', 'adsads': 'asdasd'}
    sql2 = '''
        select any_value(total.name) as total_name,any_value(total.shop_name) as shop_name,any_value(total.tb_username) as tb_username,any_value(total.school_name) as school_name from (
select
       app01_student.name,
       app01_shop.shop_name,
       app01_student.tb_username,
       school.school_name
from app01_shop,app01_student
    join app01_school school on app01_student.school_id = school.id
where app01_student.name='{}' and app01_shop.cooperate_state=1
union
select distinct stu.name,shop.shop_name,tb_username,school_name
from app01_studentshop ss
join app01_shop shop on ss.shop_id = shop.id
join app01_student stu on ss.student_id = stu.id
join app01_school school on stu.school_id = school.id
where stu.name = '{}') total
group by total.tb_username,total.shop_name,total.school_name,total.tb_username having count(*) <2;'''.format(user_name,
                                                                                   user_name)
    res = get_dict_data_sql(cursor, sql2)  # list

    tb_names = set()
    # for i in res:
    #     tb_names.add(i['tb_username'])
    # tb_names = list(tb_names)
    # tmp = []


    return HttpResponse(json.dumps(res, ensure_ascii=False))  # jq那边在 用js的反序列方法转换即可


def upload(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not os.path.exists('./data'):
            os.makedirs('./data')

        path = os.path.join("./data", myFile.name)
        destination = open(path, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        res = {'das': 'asdas', 'adsads': 'asdasd'}
        try:
            data_add(path)
            return HttpResponse(json.dumps(res))
        except:
            res = {'wrong': 'wrong'}
            return HttpResponse(json.dumps(res))


def shop_search(requests):
    res = {'msg': 'ok'}
    #    res = get_dict_data_sql(cursor, sql2) 将sql语句执行结果转化为字典
    return HttpResponse(json.dumps(res, ensure_ascii=False))


def shop_merge(requests):
    annex_shop_id = requests.POST.get("annex_shop")
    main_shop_id = requests.POST.get("main_shop")
    print(annex_shop_id, main_shop_id)
    res = {'msg': 'ok'}
    return HttpResponse(json.dumps(res, ensure_ascii=False))


def recommended_students(requests):
    res = {'msg': 'ok'}
    #    res = get_dict_data_sql(cursor, sql2) 将sql语句执行结果转化为字典
    con, cursor = get_sql_conn()
    shop_name = requests.POST.get("shopname").strip()
    print(shop_name)
    try:
        models.Shop.objects.filter(shop_name=shop_name)
    except Exception as e:
        return HttpResponse(json.dumps(res, ensure_ascii=False))

    user_name =requests.session['user_name']
    schools = models.School.objects.filter(user__name=user_name)
    str1=''
    for i in schools:
        str1+=str(i.id)+','
    str1=str1[:-1]
    sql3 = '''
    select distinct tb_username,name,a01s.school_name,(select count(distinct shop_id)) as count_ from app01_studentshop ss
            join app01_student stu on ss.student_id = stu.id
            join app01_shop shop on ss.shop_id = shop.id
            join app01_school a01s on stu.school_id = a01s.id
            where shop.shop_name != '{}' and school_id in ({}) group by tb_username, name, school_name having count_ > 1 order by count_ asc limit 500;
    '''.format(shop_name,str1)
    res = get_dict_data_sql(cursor, sql3)

    return HttpResponse(json.dumps(res, ensure_ascii=False))
