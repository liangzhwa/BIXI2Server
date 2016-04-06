from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='owner_project', default=None)
    description = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class TestPlan(models.Model):
    name = models.CharField(max_length=100)
    tester = models.ForeignKey(User, related_name='tester_testinfo', default=None)
    testrequirement = models.TextField(default="")
    description = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='project_testplan')
    
    def __unicode__(self):
        return self.name

class BIXIBench(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class TestResult(models.Model):
    casename = models.CharField(max_length=100)
    platform = models.CharField(max_length=100,default=None)
    bixibench = models.ForeignKey(BIXIBench, related_name='bixibench_testinfo', default=None)
    testplan = models.ForeignKey(TestPlan, related_name='testplan_testplan', default=None)
    testdate = models.DateField(default=None)
    app = models.CharField(max_length=100)
    index = models.IntegerField(blank=True, default=0)
    hsc = models.FloatField(default=None)
    fpstools = models.FloatField(default=None)
    launchtime = models.FloatField(default=None)
    reportfilename = models.CharField(max_length=500)

    def __unicode__(self):
        return self.casename

class BIXI2Version(models.Model):
    name = models.CharField(max_length=100)
    releasedate = models.DateField(default=None)
    
    def __unicode__(self):
        return self.name

class AccessControl(models.Model):
    user = models.ForeignKey(User, related_name='user_testinfo')
    project = models.ForeignKey(Project, related_name='Project_testinfo')
    accesstype = models.CharField(max_length=10)