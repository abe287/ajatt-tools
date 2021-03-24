$(document).ready(function() {

    $(document).on('click', '#add_video_links', function() {
        var links = $("[name='links']").val();

        req = $.ajax({
            url : '/add_video_links',
            type : 'POST',
            data : { links : links }
        });

        req.done(function(data) {

            $('#video_body').replaceWith(data);
            
            // clear previous input values in modal
            $("[name='links']").val('');

        });
    });

    $(document).on('click', '#start_video_download', function() {
        var task_id = $(this).attr('task_id');

        req = $.ajax({
            url : '/start_video_download',
            type : 'POST',
            data : { task_id : task_id }
        });

        req.done(function(data) {

            if (data['success'] == false) {
                if (data['error_type'] == 'no_default_video_folder'){
                    Swal.fire({
                        type: 'error',
                        title: 'No Default Folder',
                        text: 'Please add a default video folder in settings.',
                    })
                }
            }
            else {
                $('#video_body').replaceWith(data['video_html']);
            }

            console.log("download complete")

        });
    });

    $(document).on('click', '#stop_video_download', function() {
        var task_id = $(this).attr('task_id');

        req = $.ajax({
            url : '/stop_video_download',
            type : 'POST',
            data : { task_id : task_id }
        });

        req.done(function(data) {
            
            $('#video_body').replaceWith(data['video_html']);
            console.log("download stopped")

        });
    });

    $(document).on('click', '#delete_video_task', function() {
        var task_id = $(this).attr('task_id');

        req = $.ajax({
            url : '/delete_video_task',
            type : 'POST',
            data : { task_id : task_id }
        });

        req.done(function(data) {

            $('#video_body').replaceWith(data);

        });
    });

    $(document).on('click', '#open_video_file', function() {
        var task_id = $(this).attr('task_id');

        req = $.ajax({
            url : '/open_video_file',
            type : 'POST',
            data : { task_id : task_id }
        });

        req.done(function(data) {
            if (data['success'] == false) {
                if (data['error_type'] == 'no_file_path'){
                    Swal.fire({
                        type: 'error',
                        title: 'No File Path',
                        text: 'You never downloaded this link.',
                    })
                }
                if (data['error_type'] == 'file_not_found'){
                    Swal.fire({
                        type: 'error',
                        title: 'No File Found',
                        text: 'This file is not on your computer.',
                    })
                }
                if (data['error_type'] == 'no_default_video_folder'){
                    Swal.fire({
                        type: 'error',
                        title: 'No Default Folder',
                        text: 'Please add a default video folder in settings.',
                    })
                }
            }

        });
    });
});