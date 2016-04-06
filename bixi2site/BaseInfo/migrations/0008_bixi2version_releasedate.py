# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0007_bixi2version'),
    ]

    operations = [
        migrations.AddField(
            model_name='bixi2version',
            name='releasedate',
            field=models.DateField(default=None),
            preserve_default=True,
        ),
    ]
