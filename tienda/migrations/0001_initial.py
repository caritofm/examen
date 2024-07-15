# Generated by Django 4.1.2 on 2024-07-02 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAdress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=200, null=True)),
                ('ciudad', models.CharField(max_length=200, null=True)),
                ('estado', models.CharField(max_length=200, null=True)),
                ('zipcode', models.CharField(max_length=200, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.cliente')),
                ('orden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.orden')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('orden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.orden')),
            ],
        ),
    ]
