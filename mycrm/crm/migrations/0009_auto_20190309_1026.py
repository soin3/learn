# Generated by Django 2.1.2 on 2019-03-09 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20190309_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, to='crm.Role', verbose_name='用户角色'),
        ),
    ]
