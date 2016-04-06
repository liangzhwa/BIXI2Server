# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0005_testresult_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='platform',
            field=models.CharField(default=None, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testresult',
            name='testdate',
            field=models.DateField(default=None),
            preserve_default=True,
        ),
    ]
