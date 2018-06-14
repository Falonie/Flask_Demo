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
