# Generated by Django 4.1.7 on 2023-02-16 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saleproduct', '0010_category_category_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeBannerContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='res/image/home_banner')),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Home Banner Content',
                'verbose_name_plural': 'Home Banner Contents',
                'ordering': ('-created_at',),
            },
        ),
    ]
