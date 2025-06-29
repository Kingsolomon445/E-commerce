# Generated by Django 5.1.6 on 2025-04-22 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Order placed', max_length=50),
        ),
    ]
