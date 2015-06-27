task_type = '{{ requirements.task_type }}';
experiment_name = 'mvp';

worker_location = {};

$(document).ready(function () {

    $.get("/get_ipinfo", function (response) {
        worker_location = response;
    }, "jsonp");

});


var onSubmitClick = function () {
    var data = $('form').serializeArray();
    data.push({'name': 'worker_location', 'value': worker_location});

    console.log(data);
    // submit to our server
    $.ajax({
        url: "/upload_resume",
        contentType: "application/json; charset=utf-8",
        type: 'post',
        data: JSON.stringify({
            'task_type': task_type,
            'experiment_name': experiment_name,
            'operation': 'submit',
            'data': data
        }),
        success: function (result) {
            console.log('success');
            // submit to mechanical turk
            $('form').submit();
        },
        error: function (result) {
            console.log('error');
            $('form').submit();
        }
    });
}
