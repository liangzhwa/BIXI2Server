from django.shortcuts import render
from django.http import HttpResponse
from django import forms as forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest import db
import bixi2site.settings as settings
from datetime import *
import MySQLdb
import json
import sys
import os
from warnings import filterwarnings
reload(sys)
sys.setdefaultencoding('utf8')
filterwarnings('ignore', category = MySQLdb.Warning)

class UploadFileForm(forms.Form):
    file = forms.FileField()

def index(request):
    InitDB()
    return HttpResponse("Hello,word!")

@csrf_exempt
def AddProject(request):
    status = ""
    newid = 0
    if request.user.id is not None:
        InitDB()
        projectname = request.POST["name"]
        description = request.POST["desc"]
        if os.path.exists(os.path.join(settings.REPORT_PATH,projectname)):
            status = "ERROR_EXIST"
        else:
            os.mkdir(os.path.join(settings.REPORT_PATH,projectname))
            status = "SUCCESS"
        newid = db.insert("BaseInfo_project",name=projectname,description=description,owner_id=request.user.id)
        db.insert("BaseInfo_accesscontrol",project_id=newid,user_id=request.user.id,accesstype="3")
    else:
        status = "NOTLOGIN"
    return HttpResponse(json.dumps({"status":status,"result":newid}))

@csrf_exempt
def AddPlan(request):
    status = ""
    rowcount = 0
    if request.user.id is not None:
        InitDB()
        projectid = request.POST["projectid"]
        projectname = request.POST["projectname"]
        planname = request.POST["name"]
        requirement = request.POST["requirement"]
        rowcount = db.insert("BaseInfo_testplan",name=planname,project_id=projectid,testrequirement=requirement,tester_id=request.user.id,description="")
        if os.path.exists(os.path.join(settings.REPORT_PATH,projectname,planname)):
            status = "ERROR_EXIST"
        else:
            os.mkdir(os.path.join(settings.REPORT_PATH,projectname,planname))
            status = "SUCCESS"
    else:
        status = "NOTLOGIN"
    return HttpResponse(json.dumps({"status":status,"result":rowcount}))

def Login(request):
    status = ""
    username = request.GET.get("username")
    pwd = request.GET.get("pwd")
    print username,pwd
    user = auth.authenticate(username=username, password=pwd)
    if user is not None and user.is_active:
        auth.login(request,user)
        status = "SUCCESS"
    else:
        status = "FAILE"        
    return HttpResponse(json.dumps({"status":status}))
def Logout(request):
    auth.logout(request)
    return HttpResponse(json.dumps({"logout":"seccess"}))
def GetProjectList(request):
    results = []
    user = request.user if request.user.id is not None else CheckAuth(request)
    if user.id is not None:        
        InitDB()
        url = "select a.id,a.name,b.accesstype from BaseInfo_project a left join BaseInfo_accesscontrol b on b.project_id=a.id and b.accesstype>1 where b.user_id='%s'" % (user.id)
        results = db.select(url)    
    return HttpResponse(json.dumps({"result":results}))
def GetReportList(request):
    results = []
    user = request.user if request.user.id is not None else CheckAuth(request)
    if user is not None and user.id is not None: 
        InitDB()
        url = "SELECT c.`name` project,b.`name` plan,a.app,a.casename,a.reportfilename,d.accesstype FROM BaseInfo_testresult a left join BaseInfo_testplan b on a.testplan_id=b.id left join BaseInfo_project c on b.project_id=c.id left join BaseInfo_accesscontrol d on b.project_id=d.project_id where d.user_id='%s'" % (user.id)
        results = db.select(url)
    return HttpResponse(json.dumps({"result":results}))
    
@csrf_exempt
def GetUserList(request):
    results = []
    user = request.user if request.user.id is not None else CheckAuth(request)
    if user is not None and user.id is not None: 
        InitDB()
        url = "SELECT id,username FROM auth_user"
        results = db.select(url)
    return HttpResponse(json.dumps({"result":results}))
def GetTestPlan(request):
    InitDB()
    username = ""
    testplans = []
    user = user = request.user if request.user.id is not None else CheckAuth(request)
    if user is not None and user.id is not None: 
        url = "select a.id,b.name project,a.name,a.testrequirement from BaseInfo_testplan a right join BaseInfo_project b on a.project_id=b.id left join BaseInfo_accesscontrol c on b.id=c.project_id where c.user_id=%s" % (user.id)
        testplans = db.select(url)
        username = user.username
    return HttpResponse(json.dumps({"username":username,"result":testplans}))

def GetTestResult(request):
    InitDB()
    pid = request.GET.get("pid")
    url = "select app,casename,platform,`index`,hsc,fpstools,launchtime,reportfilename,b.name plan,c.name project from BaseInfo_testresult a left join BaseInfo_testplan b on a.testplan_id=b.id left join BaseInfo_project c on b.project_id=c.id where b.id=%s order by app,casename" % (pid)
    results = db.select(url)
    return HttpResponse(json.dumps({"result":results}))

@csrf_exempt
def GetUserInProject(request):
    InitDB()
    pid = request.GET.get("pid")
    url_view = "select b.id,b.username from BaseInfo_accesscontrol a left join auth_user b on a.user_id=b.id where project_id=%s and accesstype=1" % (pid)
    url_edit = "select b.id,b.username from BaseInfo_accesscontrol a left join auth_user b on a.user_id=b.id where project_id=%s and accesstype=2" % (pid)
    url_owner = "select b.id,b.username from BaseInfo_accesscontrol a left join auth_user b on a.user_id=b.id where project_id=%s and accesstype=3" % (pid)
    views = db.select(url_view)
    edits = db.select(url_edit)
    owner = db.select(url_owner)
    return HttpResponse(json.dumps({ "views":views,"edits":edits,"owner":owner }))

@csrf_exempt
def UpdateAuth(request):
    InitDB()
    project = request.POST["project"]
    viewlist = request.POST.getlist("viewlist[]") if request.POST.has_key("viewlist[]") else []
    editlist = request.POST.getlist("editlist[]") if request.POST.has_key("editlist[]") else []
    
    url_del = "delete from BaseInfo_accesscontrol where project_id=? and accesstype != ?"
    db.delete(url_del,project,"3")
    for viewer in viewlist:
        db.insert("BaseInfo_accesscontrol",project_id=project,user_id=viewer,accesstype=1)
    for editer in editlist:
        db.insert("BaseInfo_accesscontrol",project_id=project,user_id=editer,accesstype=2)
    return HttpResponse(json.dumps({"result":"SUCCESS"}))

def ChangePwd(request):
    result = "FAILE"
    user = request.user if request.user.id is not None else CheckAuth(request)
    if user.id is not None:
        username = user.username
        oldpwd = request.GET["oldpwd"]
        newpwd = request.GET["newpwd"]
        user = auth.authenticate(username=username, password=oldpwd)
        if user is not None and user.is_active:
            user.set_password(newpwd)
            user.save()
            result = "SUCCESS"
        else:
            result = "PASSWORDERROR"
    return HttpResponse(json.dumps({"result":result}))
    
def UploadLoginCheck(request):
    InitDB()
    results = []
    isAuth = False
    username = request.GET.get("username")
    password = request.GET.get("pwd")
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        isAuth = True
        url = "select a.id,b.name project,a.name,c.accesstype from BaseInfo_testplan a left join BaseInfo_project b on a.project_id=b.id left join BaseInfo_accesscontrol c on b.id=c.project_id where c.user_id=%s" % (user.id)
        results = db.select(url)
    return HttpResponse(json.dumps({"auth":isAuth,"result":results}))

def handle_uploaded_file(project,plan,file):
    filename = str(file)
    destination = open('%s/%s/%s/%s' % (settings.REPORT_PATH,project,plan,filename), 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return filename
def handle_newversion_file(file):
    filename = str(file)
    destination = open('%s/%s' % (settings.NEWVERSION_PATH,filename), 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return filename
    
@csrf_exempt
def Upload(request):
    InitDB()
    project = request.POST["project"]
    plan = request.POST["plan"]
    plan_id = request.POST["plan_id"]
    app = request.POST["app"]
    casename = request.POST["casename"]
    index = request.POST["index"]
    hsc = "0" if request.POST["hsc"] == "" else request.POST["hsc"]
    fpstools = "0" if request.POST["fpstools"] == "" else request.POST["fpstools"]
    launchtime = "0" if request.POST["launchtime"] == "" else request.POST["launchtime"]
    file = request.FILES["file"]
    filename = handle_uploaded_file(project,plan,file)
    rowcount = db.insert("BaseInfo_testresult",testplan_id=plan_id,app=app,casename=casename,index=index,hsc=hsc,fpstools=fpstools,launchtime=launchtime,reportfilename=filename,bixibench_id='1',platform='',testdate=str(date.today()))
    return HttpResponse(json.dumps({ "status":"SUCCESS","result":rowcount }))

@csrf_exempt
def UploadNewVersion(request):
    InitDB()
    newversion = request.POST["newversion"]
    file = request.FILES["file"]
    filename = handle_newversion_file(file)
    rowcount = db.insert("BaseInfo_bixi2version",name=newversion,releasedate=str(date.today()))
    return HttpResponse(json.dumps({ "status":"SUCCESS","result":rowcount }))

def GetNewVersion(request):
    InitDB()
    result = ""
    url = "select id,name from BaseInfo_bixi2version order by id desc"
    results = db.select_one(url)
    if results is not None and len(results) > 0:
        result = results["name"]
    return HttpResponse(result)

def CheckAuth(req):
    username = req.GET.get("username")
    password = req.GET.get("pwd")
    user = auth.authenticate(username=username, password=password)
    return user
def InitDB():
    db.create_engine(user='root',password='root',database='bixi2server',host='127.0.0.1',port=3306)