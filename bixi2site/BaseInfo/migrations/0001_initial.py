# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accesstype', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BIXIBench',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(related_name='owner_project', default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('project', models.ForeignKey(related_name='project_testplan', to='BaseInfo.Project')),
                ('tester', models.ForeignKey(related_name='tester_testinfo', default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('casename', models.CharField(max_length=100)),
                ('platform', models.CharField(max_length=100)),
                ('testdate', models.DateField()),
                ('app', models.CharField(max_length=100)),
                ('score', models.FloatField()),
                ('scoretype', models.CharField(max_length=10)),
                ('reportfilename', models.CharField(max_length=500)),
                ('bixibench', models.ForeignKey(related_name='bixibench_testinfo', default=None, to='BaseInfo.BIXIBench')),
                ('testplan', models.ForeignKey(related_name='testplan_testplan', default=None, to='BaseInfo.TestPlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='accesscontrol',
            name='project',
            field=models.ForeignKey(related_name='Project_testinfo', to='BaseInfo.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accesscontrol',
            name='user',
            field=models.ForeignKey(related_name='user_testinfo', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
