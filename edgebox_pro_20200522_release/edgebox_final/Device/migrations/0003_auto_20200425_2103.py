# Generated by Django 2.2.2 on 2020-04-25 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Device', '0002_equipmenttemplatecanis'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipmenttemplatecanis',
            old_name='etr_accordname',
            new_name='etc_accordname',
        ),
        migrations.RenameField(
            model_name='equipmenttemplatecanis',
            old_name='etr_col',
            new_name='etc_col',
        ),
        migrations.RenameField(
            model_name='equipmenttemplatecanis',
            old_name='etr_format',
            new_name='etc_format',
        ),
        migrations.RenameField(
            model_name='equipmenttemplatecanis',
            old_name='etr_pip_no',
            new_name='etc_pip_no',
        ),
        migrations.RenameField(
            model_name='equipmenttemplatecanis',
            old_name='etr_round',
            new_name='etc_round',
        ),
    ]
