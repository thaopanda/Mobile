# Generated by Django 3.1.1 on 2021-04-10 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
        ('Product', '0002_auto_20210409_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_In_Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_cart', to='User.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_cart', to='Product.product')),
            ],
        ),
    ]
