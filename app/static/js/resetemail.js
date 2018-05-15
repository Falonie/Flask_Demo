$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        if (!email) {
            zlalert.alertInfoToast('请输入邮箱');
            return;
        }
        zlajax.get({
            'url': '/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data['data'] == 200) {
                    zlalert.alertSuccessToast('邮件发送成功！');
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});