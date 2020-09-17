from django.conf.urls import url, include
# from user import views
from . import views


app_name = 'remotely'
urlpatterns = [
    url(r'^list/', views.List, name='remotelylist'),  #
    url(r'^setting/enable', views.settingEnable, name='remotelysettingenable'),  #
]
