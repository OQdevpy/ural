# Generated by Django 4.2.3 on 2023-08-26 08:13

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_orderitem_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('lft', 'title'), 'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='offer',
            options={'ordering': ('order', 'title'), 'verbose_name': 'торговое предложение', 'verbose_name_plural': 'торговые предложения'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'заказ', 'verbose_name_plural': 'заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'позиция заказа', 'verbose_name_plural': 'позиции заказов'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('title',), 'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AlterField(
            model_name='product',
            name='city',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('ufa', 'Уфа'), ('sant-peterburg', 'Санкт-Петербург'), ('tyumen', 'Тюмень'), ('magadan', 'Магадан'), ('kursk', 'Курская область'), ('mahachkala', 'Махачкала')], default='ufa', max_length=100, verbose_name='City'),
        ),
    ]
