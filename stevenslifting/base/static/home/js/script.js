$(document).ready(function() {
    autoHideAlerts();
    hideSetsOnLoad();

    function hideSetsOnLoad() {
        $(".setContent").each(function () {
            $(this).hide()
        });
    }

    function autoHideAlerts() {
        if ($(".alert").is(":visible")) {
            setTimeout(function() {
                $(".alert").hide()
            }, 3000);
        }
    }
    
});