# -*- coding: UTF-8 -*-
from django.http import JsonResponse
import os
import django
from django.contrib.auth.decorators import login_required
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_manage.settings'
django.setup()
from django.views.decorators.csrf import csrf_exempt
import pymysql
from sys_settings.models import Dbs
from django.shortcuts import render
import subprocess


# 创建数据库连接
def conn(database):
    db_list = Dbs.objects.values_list("name", flat=True)
    host = Dbs.objects.filter(name=database).values_list("host", flat=True).first()
    port = Dbs.objects.filter(name=database).values_list("port", flat=True).first()
    if port is not None:
        port = int(port)
    user = Dbs.objects.filter(name=database).values_list("user", flat=True).first()
    password = Dbs.objects.filter(name=database).values_list("password", flat=True).first()
    db = Dbs.objects.filter(name=database).values_list("db", flat=True).first()

    if database in db_list:
        con = pymysql.connect(host=host, port=port, user=user,
                              password=password, db=db, charset='utf8')
        return con
    else:
        return None


# 查询数据库（读）接口
@csrf_exempt
def sqlr(request):
    sql = request.POST.get('sql', '')
    database = request.POST.get('database', '')
    if sql != "":
        con = conn(database)
        if con is not None:
            con.ping(reconnect=True)
            cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(sql)
            result = cursor.fetchall()
            return JsonResponse(result, safe=False)
        else:
            return JsonResponse({"code": 10001, "message": "输入的数据库有误"})
    else:
        return JsonResponse({"code": 10002, "message": "sql语句不能为空"})


# 查询数据库（写）接口
@csrf_exempt
def sqlw(request):
    sql = request.POST.get('sql', '')
    database = request.POST.get('database', '')
    if sql != "":
        con = conn(database)
        if con is not None:
            con.ping(reconnect=True)
            cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                cursor.execute(sql)
                con.commit()
            except Exception:
                con.rollback()
                return JsonResponse({"code": 10003, "message": "执行失败,请检查你的sql语句:" + str(Exception)})
            finally:
                cursor.close()
                con.close()
            return JsonResponse({"code": 200, "message": "执行成功"})
        else:
            return JsonResponse({"code": 10001, "message": "输入的数据库有误"})
    else:
        return JsonResponse({"code": 10002, "message": "sql语句不能为空"})


# openapi管理
@login_required
def openapi_list(request):
    username = request.session.get('user', '')  # 读取浏览器登录session
    return render(request, "openapi_manage.html")


# 启动vpn
@csrf_exempt
def vpn(request):
    run_sh = "myvpn"
    p = subprocess.Popen(run_sh, shell=True)
    p.wait()
    pcode = p.returncode
    print(pcode)
    if pcode == 0:
        print("输出的内容是:" + str(pcode))
        return JsonResponse({"code":200, "message":"vpn已启动"})
    else:
        print("发生异常")
        return JsonResponse({"code":417, "message":"vpn启动异常，请联系管理员"})