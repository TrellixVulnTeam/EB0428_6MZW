from django.conf.urls import url, include
# from user import views
from . import views


app_name = 'Log'
urlpatterns = [
    url(r'^list/', views.List, name='Loglist'),  #
    url(r'^select/', views.Select, name='Logselect'),  #
    url(r'^event/', views.Event, name='LogEvent'),  #
    url(r'^delete/', views.Delete, name='LogDelete'),  #
]
