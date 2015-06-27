function LimtCharacters(txtMsg, CharLength, indicator) {
    label = indicator + "_label";
    intro = indicator + "_text";

    chars = txtMsg.value.length;
    document.getElementById(label).innerHTML = chars + " / 140";

    $("#submitButton").attr("disabled", false);

    document.getElementById(indicator + "_review").innerHTML = '"' + txtMsg.value + '"';

}

$("#submitButton").click(function (e) {
    e.preventDefault();
    for (i = 0; i < 25; i++) {
        if ($("#message" + i + '_text').length > 0) {
            if ($("#message" + i + '_text').val().length < 25) {
                $("#message" + i + '_please').show();
                return;
            } else {
                $("#message" + i + '_please').hide();
            }
        }

    }
    onSubmitClick();
});
