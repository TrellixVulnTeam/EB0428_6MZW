from django.db import models
from edgebox_final.base_model import BaseModel
# Create your models here.

class get_settingdown_model(BaseModel):
    '''
    获取配置下发的列表
    '''
    down_type = models.CharField(max_length=30, verbose_name="配置的类型")
    down_topic = models.CharField(max_length=30, verbose_name="主题")
    down_num = models.IntegerField(default=0, verbose_name="已下发次数")
    down_num2 = models.IntegerField(default=0, verbose_name="失敗次數")
    down_param = models.CharField(max_length=300, verbose_name="需要的参数设置")
    down_remark = models.CharField(max_length=100, verbose_name="下发描述")

    class Meta:
        db_table = 'gateway_settingdown'
        verbose_name = '網關配置下发'
        verbose_name_plural = verbose_name
