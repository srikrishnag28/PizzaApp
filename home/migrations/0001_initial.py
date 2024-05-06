# Generated by Django 5.0.4 on 2024-05-04 19:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='pizza')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=100)),
                ('amount', models.IntegerField(default=100)),
                ('status', models.CharField(choices=[('Order Received', 'Order Received'), ('Baking', 'Baking'), ('Baked', 'Baked'), ('Out for delivery', 'Out for delivery')], default='Order Received', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.pizza')),
            ],
        ),
    ]