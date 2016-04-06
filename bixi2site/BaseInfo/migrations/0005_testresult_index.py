# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0004_auto_20151026_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='index',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
