# Generated by Django 3.1.1 on 2020-09-14 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200914_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speechtimeline',
            name='timeline',
            field=models.TextField(),
        ),
    ]