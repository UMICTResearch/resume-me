$('#file').bind('change', function () {
    size = this.files[0].size / 1024 / 1024;
    submit = $('#submitfile');

    if (size > 1) {
        submit.prop('disabled', true);
        alert('The file you\'re attaching is bigger than what is allowed. Try attaching a lower sized file.');
    } else if (size < 0.05) {
        submit.prop('disabled', true);
        alert('We\'ve detected that the size of this file is less than 50 bytes, are you sure you are uploading the right file?');
    } else {
        submit.prop('disabled', false);
    }

});

$(function () {
    // instantiate the addressPicker suggestion engine (based on bloodhound)
    var addressPicker = new AddressPicker({
        autocompleteService: {types: ['(cities)'], componentRestrictions: {country: 'US'}}
    });

    // instantiate the typeahead UI
    $('#location').typeahead(null, {
        displayKey: 'description',
        source: addressPicker.ttAdapter()
    });
});


