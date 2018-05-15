$(function () {
    $('#sms_captcha_btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var telephone = $("input[name='telephone']").val();
        if (!(/^1[345879]\d{9}$/.test(telephone))) {
            // zlalert.alertInfoToast('请输入正确手机号码');
            return;
        }
        var timestamp = (new Date).getTime();
        var sign = md5(timestamp + telephone + "werqewr2jmvspo2938lwsop");
        // zlajax.get({
        zlajax.post({
            // 'url': '/c/sms_captcha?telephone=' + telephone,
            'url': '/sms_captcha/',
            'data': {
                'telephone': telephone,
                'timestamp': timestamp,
                'sign': sign
            },
            'success': function (data) {
                // console.log(data);
                if (data['code'] == 200) {
                    // zlalert.alertSuccessToast('短信发送成功！');
                    self.attr("disabled", 'disabled');
                    var timeCount = 60;
                    var timer = setInterval(function () {
                        timeCount--;
                        self.text(timeCount);
                        if (timeCount <= 0) {
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.text('发送验证码');
                        }
                    }, 1000);
                } else {
                    zlalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});

$(function () {
    $('#submit-btn').click(function (event) {
        // $('#s').click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var sms_captcha_input = $("input[name='sms_captcha']");
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password']");
        var password2_input = $("input[name='repeat_password']");
        var email_input = $("input[name='email']");
        var captcha_input = $("input[name='captcha']");
        // var graph_captcha_input = $("input[name='graph_captcha']");

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var email = email_input.val();
        var captcha = captcha_input.val();
        // var graph_captcha = graph_captcha_input.val();

        zlajax.post({
            'url': '/register/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'username': username,
                // 'password1': password1,
                // 'password2': password2
                'password': password1,
                'repeat_password': password2,
                'email': email,
                'captcha': captcha
                // 'graph_captcha': graph_captcha
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    window.location = '/';
                    console.log(data)
                    // var return_to = $("#return-to-span").text();
                    // if (return_to) {
                    //     window.location = return_to;
                    // } else {
                    //     window.location = '/';
                    // }
                } else {
                    // zlalert.alertInfo(data['message']);
                    // alert(data['message']);
                    var message = data['message'];
                    $('#message').html(message);
                    $('#message').show();
                }
            },
            'fail': function (error) {
                // zlalert.alertNetWorkError();
                console.log(error)
            }
        });
    });
});