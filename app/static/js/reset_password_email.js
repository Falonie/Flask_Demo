$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();

        var telephone_input = $("input[name='telephone']");
        var password1_input = $("input[name='password']");
        var password2_input = $("input[name='repeat_password']");

        var telephone = telephone_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();

        zlajax.post({
            'url':''
        });
    });
});