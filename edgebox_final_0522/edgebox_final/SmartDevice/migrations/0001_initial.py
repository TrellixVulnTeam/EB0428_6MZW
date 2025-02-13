# Generated by Django 2.2.2 on 2020-06-15 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SmartCommunicate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('smart_name', models.CharField(max_length=30, unique=True, verbose_name='通信路径名称')),
                ('smart_area', models.CharField(max_length=30, verbose_name='通信路径区域')),
                ('smart_remark', models.CharField(max_length=50, verbose_name='通信路径描述')),
                ('smart_sns', models.CharField(max_length=50, verbose_name='智能产品SN')),
                ('smart_status', models.CharField(default='离线', max_length=30, verbose_name='通信路径开启状态')),
                ('smart_enable', models.BooleanField(default=True, verbose_name='通信路径激活使能')),
            ],
            options={
                'verbose_name': '网关智能产品通信信息',
                'db_table': 'gateway_smartcommu_list',
                'verbose_name_plural': '网关智能产品通信信息',
            },
        ),
    ]
