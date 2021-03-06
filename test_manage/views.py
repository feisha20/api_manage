from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
import pymysql
from django.shortcuts import render
from test_manage.settings import DATABASES
from django.contrib.auth.decorators import login_required
from project_manage.models import ProjectVersion
from django.contrib.auth.models import User
from base.models import User_info
db = DATABASES

# 数据库的链接信息
con = pymysql.connect(
    host=db["default"]["HOST"],
    port=int(db["default"]["PORT"]),
    user=db["default"]["USER"],
    password=db["default"]["PASSWORD"],
    db=db["default"]["NAME"],
    charset="utf8",
)


# 读数据库
def read_db(sql):
    con.ping(reconnect=True)
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    con.close()
    return result


# 写数据库
def write_db(sql):
    con.ping(reconnect=True)
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()


# 登录
def login(request):
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/home/')
            return response
        else:
            return render(request, 'login.html', {'error': '账号或者密码错误，请重新输入！'})
    return render(request, 'login.html')


# 首页
def home(request):
    return render(request, "home.html")


@login_required
def index(request):
    username = request.session.get('user', '')  # 读取浏览器登录session
    owner_ids = User_info.objects.values_list("owner_id", flat=True)
    if request.user.id not in owner_ids:
        User_info.objects.create(
            sex=0,
            remark="",
            owner=request.user
        )
    user = User.objects.filter(username=username)
    user_info = User_info.objects.filter(owner=request.user.id)
    projectversion_list = ProjectVersion.objects.all().order_by("-publish_date")  # 读取project
    return render(request, "index_v2.html", {"user": username, "projectversions": projectversion_list, 'user':user, 'user_info': user_info})


# 文件管理
def file_manage(request):
    return render(request, "file_manager.html")


# 首页2
def index2(request):
    return render(request, "index_v2.html")


# 登出
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


# 访问项目日志
def project_log(request):
    projectversion_list = ProjectVersion.objects.all().order_by("-publish_date")  # 读取project
    return render(request, 'project_log.html', {"projectversions": projectversion_list})
