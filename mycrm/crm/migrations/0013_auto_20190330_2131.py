# Generated by Django 2.1.7 on 2019-03-30 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_auto_20190330_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyrecord',
            name='record',
            field=models.CharField(choices=[(0, '已签到'), (1, '迟到'), (2, '缺勤'), (3, '早退')], default=0, max_length=64, verbose_name='上课纪录'),
        ),
    ]
