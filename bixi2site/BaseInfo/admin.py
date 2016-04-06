from django.contrib import admin
from BaseInfo.models import Project,TestPlan,BIXIBench,TestResult,AccessControl

admin.site.register(Project)
admin.site.register(TestPlan)
admin.site.register(BIXIBench)
admin.site.register(TestResult)
admin.site.register(AccessControl)