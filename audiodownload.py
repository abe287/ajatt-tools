from __future__ import unicode_literals
import youtube_dl

import pytube
import os

from tinymongo import TinyMongoClient
connection = TinyMongoClient("ajatt")
db = connection.ajatt

def youtube(link, audio_folder):
    video = pytube.YouTube(link)
    video_title = video.title
    mp4_output_file = video.streams.filter(adaptive=True, only_audio=True).first().download(output_path = audio_folder)

    bad_characters = ['<','>',':','"','/','\\','|','?','*']
    for character in bad_characters:
        video_title = video_title.replace(character, "")

    try:
        output_file = f'{audio_folder}\{video_title}.mp3'
        os.rename(mp4_output_file, output_file)
    except FileExistsError:
        num = 1
        while os.path.exists(f'{audio_folder}\{video_title}({num}).mp3'):
            num += 1
        output_file = f'{audio_folder}\{video_title}({num}).mp3'
        os.rename(mp4_output_file, output_file)
    
    return output_file

def audio_download(task_id, audio_folder):
    task = db.audio.find_one({"_id": task_id})
    link, website = task['link'], task['website']

    if website.lower() == "youtube":
        output_file = youtube(link, audio_folder)
    
    #Update task status
    db.audio.update_one({"_id": task_id}, {"status": "Complete", "file_path": output_file})
