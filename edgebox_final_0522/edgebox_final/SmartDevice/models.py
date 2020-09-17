from django.db import models, connection

# Create your models here.
from edgebox_final.base_model import BaseModel


class SmartCommunicate(BaseModel):
    '''M5之间通信模型类'''

    smart_name = models.CharField(max_length=30, unique=True, verbose_name="通信路径名称")
    smart_area = models.CharField(max_length=30, verbose_name="通信路径区域")
    smart_remark = models.CharField(max_length=50, verbose_name="通信路径描述")
    smart_sns = models.CharField(max_length=50, verbose_name="智能产品SN")
    smart_status = models.CharField(max_length=30, default="离线", verbose_name="通信路径开启状态")
    smart_enable = models.BooleanField(default=False, verbose_name="通信路径激活使能")

    class Meta:
        db_table = 'gateway_smartcommu_list'
        verbose_name = '网关智能产品通信信息'
        verbose_name_plural = verbose_name


class SmartSns(BaseModel):
    '''M5的SN模型类'''

    smart_sname = models.CharField(max_length=30, unique=True, verbose_name="智能产品SN名称")
    smart_sns = models.CharField(max_length=50, verbose_name="智能产品SN")


    class Meta:
        db_table = 'gateway_smartsns_list'
        verbose_name = '网关智能产品SN信息'
        verbose_name_plural = verbose_name


class SmartM5Log(BaseModel):
    '''M5的日志模型类'''

    smart_sname = models.CharField(max_length=30, unique=True, verbose_name="智能产品SN名称")
    smart_sns = models.CharField(max_length=50, verbose_name="智能产品SN")


    class Meta:
        db_table = 'gateway_smartlog'
        verbose_name = '网关智能产品日志信息'
        verbose_name_plural = verbose_name
