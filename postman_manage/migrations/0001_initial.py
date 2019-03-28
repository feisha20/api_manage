# Generated by Django 2.1.7 on 2019-03-27 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Xkey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xkey', models.CharField(max_length=200, verbose_name='xkey')),
                ('xkey_owner', models.CharField(max_length=200, verbose_name='xkey_owner')),
                ('remark', models.CharField(max_length=200, verbose_name='remark')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'Xkey管理',
                'verbose_name_plural': 'Xkey管理',
            },
        ),
    ]
