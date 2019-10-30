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

import json
import datetime
import hashlib
from copy import deepcopy

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


    res = get_dict_data_sql(cursor, sql)
    return HttpResponse(json.dumps(res, cls=DateEncoder, ensure_ascii=False))  # jq那边在 用js的反序列方法转换即可


def test(request):
    return render(request, "login/test.html")


def ajaxsearchtwo(request):
    con, cursor = get_sql_conn()
    user_name = request.POST.get("username").strip()
    res = {'das': 'asdas', 'adsads': 'asdasd'}
    # res = get_dict_data_sql(cursor, sql2)  # list
    tb_names = set()
    # for i in res:
    #     tb_names.add(i['tb_username'])
    # tb_names = list(tb_names)
    # tmp = []

    #已刷
    used_sql = "select max(ss.order_time) as last_time ,stu.name,stu.tb_username,shop_name,school_name from app01_studentshop ss join app01_shop shop on ss.shop_id = shop.id join app01_student stu on ss.student_id = stu.id join app01_school sch on stu.school_id = sch.id where stu.name = '{}' and shop.cooperate_state = 1 group by ss.student_id, ss.shop_id order by  stu.tb_username;".format(
        user_name)
    total_shop_sql = '''
    SELECT shop_name
    FROM app01_shop
    WHERE cooperate_state = 1
    '''
    cursor.execute(total_shop_sql)
    total_shop = list(cursor.fetchall())
    cursor.execute(used_sql)
    used_info = list(cursor.fetchall())
    used_shop = []
    tb_shop_name=[]

    for index, info in enumerate(used_info):
        if index == 0:
            used_shop.append(used_info[index][3])
            continue
        else:
            if used_info[index][2] != used_info[index - 1][2]:
                tb_shop_name.append({'name': used_info[index-1][1], 'shop_unused':list( set(total_shop) ^ set(used_shop)),
                                     'school_name': used_info[index-1][-1], 'tb_username': used_info[index-1][-2],
                                     'shop_use': deepcopy(used_shop)})
                used_shop = []
            else:
                used_shop.append(used_shop[index][-2])


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
