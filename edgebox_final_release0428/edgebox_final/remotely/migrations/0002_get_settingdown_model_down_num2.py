# Generated by Django 2.2.2 on 2020-04-24 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remotely', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='get_settingdown_model',
            name='down_num2',
            field=models.CharField(default=0, max_length=30, verbose_name='失敗次數'),
        ),
    ]
