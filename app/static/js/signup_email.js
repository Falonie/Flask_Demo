$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password']");
        var password2_input = $("input[name='repeat_password']");
        var email_input = $("input[name='email']");
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var email = email_input.val();
        zlajax.post({
            'url': '/register_by_email/',
            'data': {
                'username': username,
                'password': password1,
                'repeat_password': password2,
                'email': email
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    var message = data['message'];
                    $('#message').html(message);
                    $('#message').show();
                    window.location = '/'
                } else {
                    var message = data["message"];
                    $('#message').html(message);
                    $('#message').show();
                }
            }
        })
    });
});