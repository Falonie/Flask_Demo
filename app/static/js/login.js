$(function () {
    $('#btn-submit-login').click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var account_input = $("input[name='account']");
        var password_input = $("input[name='password']");
        var telephone = telephone_input.val();
        var password = password_input.val();
        var account = account_input.val();
        zlajax.post({
            'url': '/login/',
            'data': {
                'telephone': telephone,
                'account': account,
                'password': password
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    // window.location = '/';
                    var return_to = $('#return-to-span').text();
                    if (return_to) {
                        window.location = return_to;
                    } else {
                        window.location = '/'
                    }
                } else {
                    // window.location.reload();
                    // window.location = '/register/';
                    // console.log('ssssssssssss')
                    var message = data['message'];
                    $('#message').html(message);
                    $('#message').show();
                }
            },
            'fail': function (error) {
                console.log(error)
            }
        })
    });
});