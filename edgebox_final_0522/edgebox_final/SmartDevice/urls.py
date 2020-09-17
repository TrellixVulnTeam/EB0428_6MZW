from django.conf.urls import url
# from user import views
from . import views

# app_name = 'user'
app_name = 'SmartDevice'
urlpatterns = [
    url(r'^pipe/', views.pipeLine, name='pipe'),  #
    url(r'^pipenable/', views.Enable, name='pipeEnable'),  #
    url(r'^apptest/', views.apptest, name='apptest'),  #
    url(r'^smartlist/', views.smartList, name='smartList'),  #
    url(r'^smartenable', views.smartEnable, name='smartEnable'),  #
    url(r'^smartcreate', views.smartCreate, name='smartCreate'),  #
    url(r'^smartdelete', views.smartDelete, name='smartDelete'),  #
    url(r'^smartorder', views.smartOrder, name='smartOrder'),  #
    url(r'^logweb', views.logWeb, name='logWeb'),  #

]

# 'DIRS': [os.path.join(BASE_DIR, 'SmartDevice/templates')],
