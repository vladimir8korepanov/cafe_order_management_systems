# Generated by Django 5.1.5 on 2025-02-05 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_options_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.JSONField(default=list, verbose_name='Заказанные блюда'),
        ),
    ]
