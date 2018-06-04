$(function () {
    $('#btn-submit-comment').click(function (event) {
        event.preventDefault();
        var comment_input = $("input[name='comment_content']");
        var question_id_input = $("input[name='question_id']");
        var comment = comment_input.val();
        var question_id = question_id_input.val();
        zlajax.post({
            'url': '/comments/',
            'data': {
                'comment_content': comment,
                'question_id': question_id
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    window.location.reload();
                    // window.location = '/'
                    console.log(data);
                } else {
                    window.location.reload();
                }
            }
        });
    });
});