from django.db import models, connection

# Create your models here.
from edgebox_final.base_model import BaseModel


class get_event_model(BaseModel):
    '''
    应用Tcp设备模板接口信息
    '''
    # LEVEL = (
    #     (0, "info"),
    #     (1, "success"),
    #     (2, "warning"),
    #     (3, "error")
    # )
    event_level = models.CharField(max_length=30, verbose_name="事件等級")
    event_username = models.CharField(max_length=30, verbose_name="用戶操作")
    event_remark = models.CharField(max_length=100, verbose_name="事件詳情")

    class Meta:
        db_table = 'gateway_event'
        verbose_name = '網關事件中心'
        verbose_name_plural = verbose_name

def get_subdevicelog_model(subdevice_name):
    table_name = 'gateway_{0}_log'.format(subdevice_name)

    class SubdeviceMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            name += '_' + subdevice_name  # 这是Model的name.
            return models.base.ModelBase.__new__(cls, name, bases, attrs)

    class SubdeviceLog(BaseModel):
        __metaclass__ = SubdeviceMetaclass
        subdevice_name = models.CharField(max_length=30, verbose_name="子设备名称")
        remark = models.CharField(max_length=100, verbose_name="日志详情")

        @staticmethod
        def is_exists():
            return table_name in connection.introspection.table_names()

        class Meta:
            db_table = table_name
            indexes = [models.Index(fields=['id']), ] # 給id 字段添加索引

    return SubdeviceLog