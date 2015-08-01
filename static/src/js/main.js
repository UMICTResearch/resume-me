$('#file').bind('change', function () {
    size = this.files[0].size / 1024 / 1024;

    if (size > 1) {
        $('#button').prop('disabled', true);
        alert('The file you\'re attaching is bigger than what is allowed. Try attaching a lower sized file.');
    } else {
        $('#button').prop('disabled', false);
    }
});
