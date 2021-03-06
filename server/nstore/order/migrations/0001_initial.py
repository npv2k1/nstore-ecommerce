# Generated by Django 3.2.9 on 2021-11-16 11:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('tracking_number', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_gateway', models.CharField(choices=[('STRIPE', 'STRIPE'), ('CASH_ON_DELIVERY', 'CASH_ON_DELIVERY')], default='STRIPE', max_length=50)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('delivery_fee', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('delivery_time', models.CharField(max_length=255, null=True)),
                ('billing_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='billing_address', to='customer.address')),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('shipping_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipping_address', to='customer.address')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('serial', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='order.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_product', to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='order.orderstatus'),
        ),
    ]
