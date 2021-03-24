function fetchstats(){
    $.ajax({
     url: '/get_progress',
     type: 'GET',
     success: function(data){
        var video_html = data['video_html'];
        var audio_html = data['audio_html'];

        $('#audio_body').replaceWith(audio_html);
        $('#video_body').replaceWith(video_html);

     },
     complete:function(data){
      setTimeout(fetchstats, 5000);
     }
    });
   }
   
   $(document).ready(function(){
    setTimeout(fetchstats, 5000);
   });