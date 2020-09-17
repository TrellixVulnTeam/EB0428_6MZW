from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from User import views

app_name = 'User'
urlpatterns = [
    re_path(r'login(?P<change>/.*)?', views.LoginView.as_view(), name='login'),  # 用户登录
    # path('logout', views.LogoutView.as_view(), name='logout'),  # 用户退出登录
    # path('login', LoginView.as_view(template_name='user/login/login.html'), name='login'),  # 用户登录
    path('verifyApi', views.VerifyCodeApi.as_view(), name='verify_api'),
    re_path(r'verify_code/?', views.VerifyCodeView.as_view(), name='verify_code'),  # 验证码
    path('forget_password', views.ForgetPasswordView.as_view(), name='forget_password'),  # 忘记密码
    path('mend_password', views.MendPasswordView.as_view(), name='mend_password'),  # 修改密码
    path('create_user', views.CreateUserView.as_view(), name='create_user'),  # 创建用户
    re_path(r'activate_user/(?P<token>.*)$', views.ActivateUserView.as_view(), name='activate_user'),  # 激活用户
    re_path(r"send_activate_email/(?P<username>.*)$", views.SendActivateEmailView.as_view(), name="send_activate_email"),  # 发送激活邮件
    re_path(r'user_info/(?P<username>.*)$', views.UserInfoView.as_view(), name='user_info_get'),  # 获取用户信息
    path('user_info', views.UserInfoView.as_view(), name='user_info_post'),  # 修改用户信息
    re_path('delete_user/(?P<username>.*)$', views.DeleteUserView.as_view(), name='delete_user_get'),  # 删除用户之检查用户是否是超级用户
    path('delete_user', views.DeleteUserView.as_view(), name='delete_user_post'),  # 删除用户
]
