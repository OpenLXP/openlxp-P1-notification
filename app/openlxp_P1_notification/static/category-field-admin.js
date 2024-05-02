// JQuery to hide and show fields
window.addEventListener("load", function() {
    console.log("Working");
    (function($) {
        var selectField = $('#id_Content_Type'),
            verified = $('#id_Email_Content');

        function toggleVerified(value) {
            console.log(value);
            if (value === 'attachment') {
                console.log("in if");
                verified.show();
            } else {
                console.log("in else");
                verified.hide();
            }
        }

        // show/hide on load based on existing value of selectField
        toggleVerified(selectField.val());

        // show/hide on change
        selectField.change(function() {
            toggleVerified($(this).val());
        });
    })(django.jQuery);
});