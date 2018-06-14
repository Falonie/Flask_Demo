$(function () {
    $('#captcha_btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var email = $("input[name='email']").val();
        if (!email) {
            zlalert.alertInfoToast('请输入邮箱');
            return;
        }
        zlajax.get({
            // zlajax.post({
            'url': '/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                // console.log(data);
                if (data['code'] == 200) {
                    // zlalert.alertSuccessToast('短信发送成功！');
                    self.attr("disabled", 'disabled');
                    var timeCount = 60;
                    var timer = setInterval(function () {
                        timeCount--;
                        // var str = '{0}{1}'.format(timeCount, '后再发送');
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
        event.preventDefault();
        var email_input = $("input[name='email']");
        var captcha_input = $("input[name='captcha']");
        var email = email_input.val();
        var captcha = captcha_input.val();
        zlajax.post({
            'url': '/change_email/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    // window.location = '/resetemail/';
                    $('#message').html(data['message']);
                    $('#message').show();
                    window.location = '/';
                    console.log(data)
                } else {
                    var message = data['message'];
                    $('#message').html(message);
                    $('#message').show();
                }
            }
        });
    });
});