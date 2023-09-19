# Generated by Django 4.2.4 on 2023-08-22 05:35

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Active')),
                ('alias', models.CharField(blank=True, db_index=True, default='', help_text='Page URL. For example: about-us.', max_length=255, verbose_name='Alias')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Title')),
                ('introtext', models.TextField(blank=True, null=True, verbose_name='Introductory Text')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Content')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Creation Date')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Update Date')),
                ('h1', models.CharField(blank=True, max_length=255, null=True, verbose_name='H1')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Browser Window Title')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name='Meta Keywords')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories', verbose_name='Image')),
                ('banner_text', models.TextField(blank=True, null=True, verbose_name='Banner Text')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='catalog.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('lft', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, db_index=True, default='', max_length=255, verbose_name='Title')),
                ('article', models.CharField(blank=True, db_index=True, default='', max_length=255, verbose_name='Article')),
                ('price', models.FloatField(blank=True, db_index=True, default=0, verbose_name='Price')),
                ('old_price', models.FloatField(blank=True, db_index=True, default=0, verbose_name='Old Price')),
                ('quantity', models.IntegerField(blank=True, db_index=True, default=0, verbose_name='Quantity')),
                ('order', models.IntegerField(db_index=True, default=500, verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Trade Offer',
                'verbose_name_plural': 'Trade Offers',
                'ordering': ('order', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Cart'), (1, 'Placed'), (2, 'Processed')], default=0)),
                ('receiver', models.CharField(db_index=True, default='', max_length=255, verbose_name='Receiver')),
                ('email', models.CharField(db_index=True, default='', max_length=50, verbose_name='Email')),
                ('phone', models.CharField(db_index=True, default='', max_length=30, verbose_name='Phone')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Active')),
                ('alias', models.CharField(blank=True, db_index=True, default='', help_text='Page URL. For example: about-us.', max_length=255, verbose_name='Alias')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Title')),
                ('introtext', models.TextField(blank=True, null=True, verbose_name='Introductory Text')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Content')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Creation Date')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Update Date')),
                ('h1', models.CharField(blank=True, max_length=255, null=True, verbose_name='H1')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Browser Window Title')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name='Meta Keywords')),
                ('image', models.ImageField(upload_to='product_images')),
                ('city', models.CharField(choices=[('ufa', 'Уфа'), ('sant-peterburg', 'Санкт-Петербург'), ('tyumen', 'Тюмень'), ('magadan', 'Магадан'), ('kursk', 'Курская область'), ('mahachkala', 'Махачкала')], max_length=100, verbose_name='City')),
                ('categories', mptt.fields.TreeManyToManyField(blank=True, null=True, related_name='products', to='catalog.category', verbose_name='Additional Categories')),
                ('category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='native_products', to='catalog.category', verbose_name='Main Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, db_index=True, default=0, verbose_name='Price')),
                ('quantity', models.IntegerField(blank=True, db_index=True, default=0, verbose_name='Quantity')),
                ('offer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='catalog.offer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.order')),
            ],
        ),
        migrations.AddField(
            model_name='offer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='catalog.product'),
        ),
    ]