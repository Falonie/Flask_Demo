$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
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
                if (data['code'] == 200) {
                    // zlalert.alertSuccessToast('邮件发送成功！');
                    // window.location = '/';
                    // console.log();
                } else {
                    zlalert.alertInfo(data['message']);
                    // var message = data['message'];
                    // $('#message').html(message);
                    // $('#message').show();
                }
            },
            'fail': function (error) {
                // zlalert.alertNetworkError();
                console.log(error)
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
            'url': '/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    // window.location = '/';
                    window.location = '/resetemail/';
                    $('#message').html(data['message']);
                    $('#message').show();
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