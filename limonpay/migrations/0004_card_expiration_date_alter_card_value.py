# Generated by Django 5.0.7 on 2024-07-29 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('limonpay', '0003_user_date_joined_user_email_user_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='expiration_date',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='value',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=15),
        ),
    ]
