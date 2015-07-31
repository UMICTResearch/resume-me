$('#file').bind('change', function () {
    size = this.files[0].size / 1024 / 1024;

    if (size > 1) {
        $('#button').prop('disabled', true);
        alert('The file size exceeds the limit allowed. Please upload a resume which is lesser than 1MB');
    } else {
        $('#button').prop('disabled', false);
    }
});
