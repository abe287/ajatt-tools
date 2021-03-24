function changeActiveTab(id) {
    var elems = document.querySelectorAll(".nav-item");
    var i;
    for (i = 0; i < elems.length; i++) {
        if (elems[i].classList.contains("active")) {
            elems[i].classList.remove("active");
        }
    }

    var element = document.getElementById(id);
    element.classList.add("active");
}

$(document).ready(function() {

    req = $.ajax({
        url : '/audio',
        type : 'GET'
    });

    req.done(function(data) {

        $('.page-content').replaceWith(data);
        changeActiveTab("load_audio");
        
    });

    $(document).on('click', '#load_audio', function() {
        req = $.ajax({
            url : '/audio',
            type : 'GET'
        });

        req.done(function(data) {

            $('.page-content').replaceWith(data);
            changeActiveTab("load_audio");
            
        });
    });

    $(document).on('click', '#load_settings', function() {
        req = $.ajax({
            url : '/settings',
            type : 'GET'
        });

        req.done(function(data) {

            $('.page-content').replaceWith(data);
            changeActiveTab("load_settings");
            
        });
    });

    $(document).on('click', '#load_video', function() {
        req = $.ajax({
            url : '/video',
            type : 'GET'
        });

        req.done(function(data) {

            $('.page-content').replaceWith(data);
            changeActiveTab("load_video");
            
        });
    });

});