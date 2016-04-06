# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0003_auto_20151022_0743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='score',
        ),
        migrations.RemoveField(
            model_name='testresult',
            name='scoretype',
        ),
        migrations.AddField(
            model_name='testresult',
            name='fpstools',
            field=models.FloatField(default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='testresult',
            name='hsc',
            field=models.FloatField(default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='testresult',
            name='launchtime',
            field=models.FloatField(default=None),
            preserve_default=True,
        ),
    ]
