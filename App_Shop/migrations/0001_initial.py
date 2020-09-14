# Generated by Django 3.0.3 on 2020-08-16 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=50)),
                ('category_created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=264)),
                ('product_image', models.ImageField(upload_to='Products')),
                ('product_preview_text', models.TextField(max_length=200, verbose_name='Preview Text')),
                ('product_detail_text', models.TextField(max_length=1000, verbose_name='Description')),
                ('product_price', models.FloatField()),
                ('product_old_price', models.FloatField(default=0.0)),
                ('product_created_date', models.DateTimeField(auto_now_add=True)),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='App_Shop.Category')),
            ],
            options={
                'ordering': ['-product_created_date'],
            },
        ),
    ]
