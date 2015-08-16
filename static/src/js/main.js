$('#file').bind('change', function () {
    size = this.files[0].size / 1024 / 1024;

    if (size > 1) {
        $('#submitfile').prop('disabled', true);
        alert('The file you\'re attaching is bigger than what is allowed. Try attaching a lower sized file.');
    } else {
        $('#submitfile').prop('disabled', false);
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


