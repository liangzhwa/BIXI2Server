# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0002_testplan_testrequirement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplan',
            name='testrequirement',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
