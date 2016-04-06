from django.conf.urls import patterns, url
from rest import views


urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^login$', views.Login),
    url(r'^logout$', views.Logout),
    url(r'^changepwd$', views.ChangePwd),
    url(r'^addproject$', views.AddProject),
    url(r'^addplan$', views.AddPlan),
    url(r'^updateauth$', views.UpdateAuth),
    url(r'^upload$', views.Upload),
    url(r'^uploadnewversion$', views.UploadNewVersion),
    url(r'^getprojectlist$', views.GetProjectList),
    url(r'^getreportlist$', views.GetReportList),
    url(r'^getuserlist$', views.GetUserList),
    url(r'^gettestplan$', views.GetTestPlan),
    url(r'^gettestresult$', views.GetTestResult),
    
    url(r'^getuserinproject$', views.GetUserInProject),
    
    url(r'^uploadlogincheck$', views.UploadLoginCheck),
    
    url(r'^getnewversion$', views.GetNewVersion),
)
