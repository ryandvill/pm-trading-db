# Generated by Django 2.1.7 on 2019-05-30 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationaldb', '0010_auto_20180322_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_hash',
            field=models.CharField(default='', max_length=64),
        ),
    ]
