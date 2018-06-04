$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var old_passowrd_input = $("input[name='old_password']");
        var new_passowrd_input = $("input[name='password']");
        var new_passowrd_input2 = $("input[name='password2']");

        var old_passowrd = old_passowrd_input.val();
        var new_passowrd = new_passowrd_input.val();
        var new_passowrd2 = new_passowrd_input2.val();

        zlajax.post({
            'url': '/changepassword/',
            'data': {
                'old_password': old_passowrd,
                'password': new_passowrd,
                'password2': new_passowrd2
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    window.location = '/';
                    $('#message').html(data['message']);
                    $('#message').show();
                    // window.location = '/resetpassword/';
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