# Generated by Django 2.2.11 on 2020-05-10 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webtest', '0002_auto_20200430_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='pre_case',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
