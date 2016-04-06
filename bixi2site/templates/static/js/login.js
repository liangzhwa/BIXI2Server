'use strict';
var serverHost = window.location.host;

$(document).ready(function(){
    $("#username").focus();
    var bannerSlider = new Slider($('#banner_tabs'), {
		time: 5000,
		delay: 400,
		event: 'hover',
		auto: true,
		mode: 'fade',
		controller: $('#bannerCtrl'),
		activeControllerCls: 'active'
	});
	$('#banner_tabs .flex-prev').click(function() {
		bannerSlider.prev()
	});
	$('#banner_tabs .flex-next').click(function() {
		bannerSlider.next()
	});
    $("#marquee1").marquee();
});

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
function Exit(){
    $("#username").val("");
    $("#pwd").val("");
}
function Enter(){
    if(event.keyCode ==13){
        Login();
    }
}