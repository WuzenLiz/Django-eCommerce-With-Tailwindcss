# Generated by Django 4.1.7 on 2023-03-31 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0009_alter_order_payment_orderproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('COD', 'Thanh toán khi nhận hàng')], default='COD', max_length=9000),
        ),
    ]
