from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from db.base_model import BaseModel
from django.contrib.auth.hashers import make_password, check_password


class User(AbstractUser, BaseModel):
    """用户模型类"""
    user_id_six = models.CharField(max_length=6, verbose_name='身份证后六位')
    phone_regex = RegexValidator(regex=r'^\d{11}$', message='手机号必须输入格式："999999999"，最多允许11位数字。')
    phone_number = models.CharField(max_length=11, validators=[phone_regex], verbose_name='手机号')  # 验证器应该是一个列表

    # def generate_active_token(self):
    #     """生成用户签名字符串"""
    #     serializer = Serializer(settings.SECRET_KEY, 3600)
    #     info = {'confirm': self.id}
    #     token = serializer.dumps(info)
    #     return token.decode()
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'edgebox_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

# user = User.objects.create_superuser(username="jackie", password="admin", email="jackie.h.zhou@mail.foxocnn.com", user_id_six="123456", )
# # user.password = make_password("admin", "jackie", "pbkdf2_sha256")
# # user.save()



