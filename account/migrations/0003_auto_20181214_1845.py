# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-14 18:45
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20181214_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiaryaccountdetails',
            name='transfer_limit',
            field=models.DecimalField(decimal_places=2, default=100000, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)]),
        ),
    ]
