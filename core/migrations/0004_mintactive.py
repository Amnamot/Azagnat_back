# Generated by Django 4.1.3 on 2023-07-06 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_senttrans_contract_remove_senttrans_to_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MintActive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]