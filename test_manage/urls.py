"""test_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from postman_manage import views
from postman_manage import views_coll
from postman_manage import views_xkey
from postman_manage import views_env
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
import postman_manage.views as view

urlpatterns = [
                  path('admin/', admin.site.urls),
                  url(r'^$', views.login),
                  path('login/', views.login),
                  path('home/', views.home),
                  path('home/index_v2.html', views.index),
                  path('logout/', views.logout),
                  path('get_xkey/', views_xkey.get_xkey),
                  path('add_xkey.html', views_xkey.add_xkey),
                  path('edit_xkey.html', views_xkey.eidt_xkey),
                  path('del_xkey.html', views_xkey.del_xkey),
                  path('collections_manage/', views_coll.collections_manage),
                  path('get_collections/', views_coll.get_collections),
                  path('get_single_collection.html', views_coll.get_single_collection),
                  path('xkeysearch/', views_xkey.xkey_search),
                  path('collection_search/', views_coll.collection_search),
                  path('envs_manage/', views_env.envs_manage),
                  path('get_envs/', views_env.get_envs),
                  path('get_singel_env.html/', views_env.get_single_env),
                  path('env_search/', views_env.env_search),
                  path('get_single_env.html', views_env.get_single_env),
                  path('edit_collection.html', views_coll.eidt_collection),
                  path('del_collection.html', views_coll.del_collection),
                  path('run_collection.html', views_coll.get_collection_detail),
                  path('run_collection/', views_coll.run_collection),
                  path('stop_collection.html/', views_coll.stop_collection),
                  path('index2/', views.index2),
                  path('file_manage/', views.file_manage),
                  url('^report/(?P<path>.*)$', serve, {'document_root': settings.REPORT_ROOT}),
                  url(r'^project/', include('project_manage.urls', namespace="project_manage")),
                  url(r'^task/', include('task_manage.urls', namespace="task_manage")),
                  url(r'^sys_settings/', include('sys_settings.urls', namespace="sys_settings")),
                  url(r'^open_api/', include('open_api.urls', namespace="open_api")),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = view.page_not_found
handler500 = view.page_error