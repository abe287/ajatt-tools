$(document).ready(function() {

    $(document).on('click', '#update_settings', function() {

        var audio_folder = $("[name='audio_folder']").val();
        var video_folder = $("[name='video_folder']").val();

        req = $.ajax({
            url : '/update_settings',
            type : 'POST',
            data : { audio_folder : audio_folder, video_folder : video_folder }
        });

        req.done(function(data) {
            
            $('.page-content').replaceWith(data['html']);

        });
    });

});