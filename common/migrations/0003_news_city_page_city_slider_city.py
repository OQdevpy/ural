# Generated by Django 4.2.3 on 2023-08-28 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alter_news_options_alter_page_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='city',
            field=models.CharField(choices=[('ufa', 'Уфа'), ('sant-peterburg', 'Санкт-Петербург'), ('tyumen', 'Тюмень'), ('magadan', 'Магадан'), ('kursk', 'Курская область'), ('mahachkala', 'Махачкала')], default='ufa', max_length=100, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='page',
            name='city',
            field=models.CharField(choices=[('ufa', 'Уфа'), ('sant-peterburg', 'Санкт-Петербург'), ('tyumen', 'Тюмень'), ('magadan', 'Магадан'), ('kursk', 'Курская область'), ('mahachkala', 'Махачкала')], default='ufa', max_length=100, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='slider',
            name='city',
            field=models.CharField(choices=[('ufa', 'Уфа'), ('sant-peterburg', 'Санкт-Петербург'), ('tyumen', 'Тюмень'), ('magadan', 'Магадан'), ('kursk', 'Курская область'), ('mahachkala', 'Махачкала')], default='ufa', max_length=100, verbose_name='City'),
        ),
    ]
