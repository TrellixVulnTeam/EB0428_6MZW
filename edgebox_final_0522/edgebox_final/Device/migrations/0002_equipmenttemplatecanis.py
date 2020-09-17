# Generated by Django 2.2.2 on 2020-04-25 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentTemplateCanis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('etc_name', models.CharField(max_length=30, verbose_name='模板名称')),
                ('etc_remark', models.CharField(max_length=30, verbose_name='模板描述')),
                ('etr_accordname', models.CharField(default='专有协议接口Canis', max_length=30, verbose_name='模板协议名称')),
                ('etr_pip_no', models.CharField(max_length=30, verbose_name='Canis通道')),
                ('etr_col', models.CharField(max_length=30, verbose_name='列名')),
                ('etr_format', models.SmallIntegerField(choices=[(0, '电压值')], default=0, verbose_name='模板数据格式')),
                ('etr_round', models.CharField(max_length=30, verbose_name='模板返回数据精确值')),
            ],
            options={
                'verbose_name': '专有协议Canis设备模板库',
                'db_table': 'gateway_equipmenttemplatecanis',
                'verbose_name_plural': '专有协议Canis设备模板库',
            },
        ),
    ]
