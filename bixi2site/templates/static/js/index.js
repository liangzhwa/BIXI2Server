'use strict';
var serverHost = window.location.host;
var curAuthList = { "userlist":[],"viewlist":[],"editlist":[],"owner":[] };
var currentRole = "";

$(document).ready(function(){
    //var tree = [
    //    { text: "Root1",href: "#root1",tags:['2'],nodes:[{text: "child1",href: "#child1", tags:['0']},{text: "child2",href: "#child2", tags:['0']}] },
    //    { text: "Root2" ,href: "#root2",tags:['rr']}
    //];
    //$('#tree').treeview({
    //    data: tree,
    //    showBorder: false,
    //    showTags: true,
    //    expandIcon: 'glyphicon glyphicon-chevron-right',
    //    collapseIcon: 'glyphicon glyphicon-chevron-down',
    //    nodeIcon: 'glyphicon glyphicon-folder-close',
    //});
    //$('#tree').on('nodeSelected', function(event, node) {
    //    console.log(node);
    //    $("#content").html("<ul><li>test</li></ul>");
    //});
    $('#loginWin').on('shown.bs.modal', function () {
        $('#username').focus()
    });
    $("#changepwd").dialog({
        width:470,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#oldpwd").val("");
            $("#newpwd").val("");
            $("#confirmpwd").val("");
        }
    });
    $("#newproject").dialog({
        width:470,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
        }
    });
    $("#newplan").dialog({
        width:470,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
        }
    });
    $("#authgrant").dialog({
        width:650,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#a_project").val("-1");
            $("#userlist").html("");
            $("#viewlist").html("");
            $("#editlist").html("");
        }
    });
    $("#userlist, #viewlist, #editlist").dragsort({ 
        dragSelector: "div", 
        dragBetween: true, 
        dragStart: StartDrag,
        dragEnd: saveOrder, 
        placeHolderTemplate: "<li class='placeHolder'><div></div></li>" 
    });
    ShowTree();
});

function ShowTree(){
    var url = "http://"+serverHost+"/rest/gettestplan?username=" + $("#username").val() + "&pwd=" +　$("#pwd").val();
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            if(JSON.parse(data)["username"] == ""){
                return;
            }else if(JSON.parse(data)["username"] == "ERROR"){
                alert("username or password error, please reinput!");
                return;
            }
            $("#btnLogin").hide();
            $("#loginUser").show();
            $("#loginUser").html("Welcome: "+JSON.parse(data)["username"]);
            var items = JSON.parse(data)["result"];
            var tree = [];
            var tempProject = "";
            for(var i=0;i<items.length;i++){
                if(tempProject != items[i]["project"]){
                    tempProject = items[i]["project"];
                    tree.push({"text":tempProject,"nodes":[]})
                }
                if(items[i]["id"]){
                    tree[tree.length-1]["nodes"].push({"id":items[i]["id"],"text":items[i]["name"],"requirement":items[i]["testrequirement"]})
                }
            }
            $('#tree').treeview({
                data: tree,
                showBorder: false,
                showTags: true,
                expandIcon: 'glyphicon glyphicon-chevron-right',
                collapseIcon: 'glyphicon glyphicon-chevron-down',
                nodeIcon: 'glyphicon glyphicon-folder-close',
            });
            $('#tree').on('nodeSelected', function(event, node) {
                $("#divTestRequirement textarea").html(node["requirement"]);
                if(node["id"]){
                    var url_testresult = "http://"+serverHost+"/rest/gettestresult?pid=" + node["id"];
                    $.ajax({
                        type: 'GET',
                        url: url_testresult,
                        success: function(data) {
                            var results = JSON.parse(data)["result"];
                            var strTemp = "";
                            for(var i=0;i<results.length;i++){
                                var tm_testcase = results[i]["casename"].split("_").slice(0,-1).join("_");
                                var ts_hsc = results[i]["hsc"] =="0" ? "--":results[i]["hsc"];
                                var ts_fpstools = results[i]["fpstools"] =="0" ? "--":results[i]["fpstools"];
                                var ts_launchtime = results[i]["launchtime"] =="0" ? "--":results[i]["launchtime"];
                                strTemp += "<tr><td>"+results[i]["app"]+"</td><td>"+tm_testcase+"</td><td>"+results[i]["index"]+"</td><td>"+ts_hsc+"</td><td>"+ts_fpstools+"</td><td>"+ts_launchtime+"</td><td><a href='/report/"+results[i]["project"]+"/"+results[i]["plan"]+"/"+results[i]["reportfilename"]+"'>"+results[i]["reportfilename"]+"</a></td></tr>";
                            }
                            $("#tbResult").html(strTemp);
                            $("#tbResult tr td").css("vertical-align","middle");
                            _w_table_rowspan("#tbResult",1,1);
                            _w_table_rowspan("#tbResult",1,1);
                        }
                    });
                }
            });
            $('#loginWin').modal('hide');
        }
    });
}
function Enter(){
    if(event.keyCode ==13){
        ShowTree();
    }
}
function Login(){    
    var username = $("#username").val();
    var pwd = $("#pwd").val();
    if(username == "" || pwd == ""){
        alert("Please input the username and password!");
        return;
    }
    var url = "http://"+serverHost+"/rest/login?username=" + username + "&pwd=" +　pwd;
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            console.log(data);
            var status = JSON.parse(data)["status"];
            if(status == "SUCCESS"){
                window.location.href = "http://"+serverHost+"/main";
            }else{
                alert("username or password invalid, please retry!");
            }
        }
    });
}
function Logout(){
    var url = "http://"+serverHost+"/rest/logout";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            window.location.href = "http://"+serverHost+"/";
            $("#tree").html("");
            $("#divTestRequirement textarea").html("");
            $("#tbResult").html("");
            $("#loginUser").html("");
            $("#username").html("");
            $("#pwd").html("");
            $("#loginUser").hide();
            $("#btnLogin").show();
        }
    });
}

function AddProject(){
    $("#newproject").dialog("open");
}
function SaveProject(){
    if(!$("#n_project").val()){
        alert("please input the project name!");
        return;
    }
    var url = "http://"+serverHost+"/rest/addproject";
    $.ajax({
        type: 'POST',
        url: url,
        data: { "name":$("#n_project").val(),"desc":$("#n_description").val()},
        success: function(data) {
            console.log(data);
            $("#newproject").dialog("close");
            ShowTree();
        },
        error: function(data){
            console.log(data);
        }
    });
}
function CloseProjectWindow(){
    $("#newproject").dialog("close");
}
function InitProjectList(){
    var url = "http://"+serverHost+"/rest/getprojectlist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var sltStr = "<option value='-1'>------Select------</option>";
            var sltAuthStr = "<option value='-1' selected>------Select------</option>";
            for(var i=0;i<items.length;i++){
                sltStr += "<option value='"+items[i]["id"]+"'>"+items[i]["name"]+"</option>"
                console.log(items[i]);
                if(items[i]["accesstype"] == "3"){
                    sltAuthStr += "<option value='"+items[i]["id"]+"'>"+items[i]["name"]+"</option>"
                }
            }
            $("#s_project").html(sltStr);
            $("#a_project").html(sltAuthStr);
        }
    });
}
function AddPlan(){
    InitProjectList();
    $("#newplan").dialog("open");
}
function SavePlan(){
    if($("#s_project").val() == "-1"){
        alert("please select the project!");
        return;
    }
    if(!$("#n_plan").val()){
        alert("please input the plan name!");
        return;
    }
    var url = "http://"+serverHost+"/rest/addplan";
    $.ajax({
        type: 'POST',
        url: url,
        data:{ "projectid":$("#s_project").val(),"projectname":$("#s_project").find("option:selected").text(),"name":$("#n_plan").val(),"requirement":$("#n_requirement").val() },
        success: function(data) {
            $("#newplan").dialog("close");
            ShowTree();
        }
    });
}
function ClosePlanWindow(){
    $("#newplan").dialog("close");
}
function AuthGrant(){
    InitProjectList();
    $("#authgrant").dialog("open");
}
function StartDrag(role){
    currentRole = role;
}
function saveOrder() {    
    if(currentRole != $(this).parent().attr("role")){
        console.log("从"+currentRole+"到"+$(this).parent().attr("role"))
    }
    currentRole = $(this).parent().attr("role");
    //var data = $("#list1 li").map(function() { return $(this).children().html(); }).get();
    //$("input[name=list1SortOrder]").val(data.join("|"));
};
function ProjectChange(obj){
    if($(obj).val() == "-1"){
        $("#userlist").html("");
        $("#viewlist").html("");
        $("#editlist").html("");
        return; 
    }
    curAuthList = { "userlist":[],"viewlist":[],"editlist":[],"owner":[] };
    $.ajax({
        type: 'POST',
        url: "http://"+serverHost+"/rest/getuserinproject?pid=" + $(obj).val(),
        success: function(data) {
            var view_items = JSON.parse(data)["views"];
            var edit_items = JSON.parse(data)["edits"];
            var owner_item = JSON.parse(data)["owner"];
            var viewlistStr = "";
            for(var i=0;i<view_items.length;i++){
                viewlistStr += "<li pid='"+view_items[i]["id"]+"'><div style='cursor: pointer;'>" + view_items[i]["username"] + "</div></li>";
                curAuthList["viewlist"].push(view_items[i]["id"])
            }
            $("#viewlist").html(viewlistStr);
            
            var eidtlistStr = "";
            for(var i=0;i<edit_items.length;i++){
                eidtlistStr += "<li pid='"+edit_items[i]["id"]+"'><div style='cursor: pointer;'>" + edit_items[i]["username"] + "</div></li>";
                curAuthList["editlist"].push(edit_items[i]["id"])
            }
            $("#editlist").html(eidtlistStr);
            
            for(var i=0;i<owner_item.length;i++){
                curAuthList["owner"].push(owner_item[i]["id"])
            }
            $.ajax({
                type: 'POST',
                url: "http://"+serverHost+"/rest/getuserlist",
                success: function(data) {
                    var items = JSON.parse(data)["result"];
                    var userlistStr = "";
                    for(var i=0;i<items.length;i++){
                        if(curAuthList["viewlist"].indexOf(items[i]["id"]) == -1 && curAuthList["editlist"].indexOf(items[i]["id"]) == -1 && curAuthList["owner"].indexOf(items[i]["id"]) == -1){
                            userlistStr += "<li pid='"+items[i]["id"]+"'><div style='cursor: pointer;'>" + items[i]["username"] + "</div></li>";
                        }
                    }
                    $("#userlist").html(userlistStr);
                }
            });
        }
    });
}
function SaveAuth(){
    var newviewlist = []
    var neweditlist = []
    $("#viewlist li").each(function(){
        newviewlist.push($(this).attr("pid"));
    });
    $("#editlist li").each(function(){
        neweditlist.push($(this).attr("pid"));
    });
    $.ajax({
        type: 'POST',
        url: "http://"+serverHost+"/rest/updateauth",
        data: { "project":$("#a_project").val(),"viewlist":newviewlist,"editlist":neweditlist },
        success: function(data) {
            console.log(data);
            $("#authgrant").dialog("close");
        }
    });
}
function CloseAuthGrantWindow(){
    $("#changepwd").dialog("close");
}
function ChangePwd(){
    $("#changepwd").dialog("open");
}
function SavePwd(){
    var oldpwd = $("#oldpwd").val();
    var newpwd = $("#newpwd").val();
    var confirmpwd = $("#confirmpwd").val();
    if(oldpwd == "" || newpwd == "" || confirmpwd == ""){
        alert("all input is required, please input!");
        return;
    }
    if(newpwd != confirmpwd){
        alert("The passwords you typed do not match!");
        return;
    }
    $.ajax({
        type: 'GET',
        url: "http://"+serverHost+"/rest/changepwd?oldpwd="+oldpwd+"&newpwd="+newpwd+"&confirmpwd="+confirmpwd,
        success: function(data) {
            console.log(data);
            var result = JSON.parse(data)["result"];
            if(result == "PASSWORDERROR"){
                alert("Old Password is wrong, please retry!");
            }else{
                $("#changepwd").dialog("close");
            }
        }
    });
}
function CloseChangePwdWindow(){
    $("#changepwd").dialog("close");
}
function testPost(){
    var url = "http://"+serverHost+"/rest/upload";
    var data = { "project":"Power","plan":"power_ww44","index":"3","casename":"AngryBirds_play_3","hsc":"19.6228","testdate":"2015-10-28","app":"AngryBirds","plan_id":"7","platform":"","fpstools":"35.4","reportfilename":"AngryBirds_play_3.zip","launchtime":"6574","bixibench_id":"1" }
    $.ajax({
        type: 'POST',
        url: url,
        data:data,
        success: function(data) {
            console.log(data);
        }
    });
}
function _w_table_rowspan(_w_table_id,_w_table_colnum,count){
    var _w_table_firsttd = "";
    var _w_table_currenttd = "";
    var _w_table_SpanNum = 0;
    var _w_table_Obj = $(_w_table_id + " tr td:nth-child(" + _w_table_colnum + ")");
    _w_table_Obj.each(function(i){
        if(i==0){
            if(typeof($(this).attr("rowspan"))=="undefined"){
                _w_table_firsttd = $(this);
            }else{
                _w_table_firsttd = $(this).next();
            }            
            _w_table_SpanNum = 1;
        }else{
            if(typeof($(this).attr("rowspan"))=="undefined"){
                _w_table_currenttd = $(this);
            }else{
                _w_table_currenttd = $(this).next();
            }
            if(_w_table_firsttd.text() ==_w_table_currenttd.text()){
                _w_table_SpanNum++;
                _w_table_currenttd.nextAll(":lt("+(count-1)+")").andSelf().remove();
                _w_table_firsttd.nextAll(":lt("+(count-1)+")").andSelf().attr("rowSpan",_w_table_SpanNum);
            }else{
                _w_table_firsttd = _w_table_currenttd;
                _w_table_SpanNum = 1;
            }
        }
    });
}
