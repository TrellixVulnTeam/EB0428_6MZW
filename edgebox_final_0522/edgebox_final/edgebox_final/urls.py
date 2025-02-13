"""edgebox_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API文档')


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('apis/user/', include('User.urls', namespace='user')),  # 用户管理
    path('apis/agent/', include('Agent.urls', namespace='agent')),  #
    path('apis/device/', include('Device.urls', namespace='device')),  #
    path('apis/drive/', include('Drive.urls', namespace='drive')),  #
    path('apis/m5/', include('SmartDevice.urls', namespace='m5')),  #
    path('apis/log/', include('Log.urls', namespace='log')),  #
    path('apis/remotely/', include('remotely.urls', namespace='remotely')),  #
    path(r'docs/', schema_view),

]
