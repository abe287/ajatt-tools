import youtube_dl, pytube
import os

from tinymongo import TinyMongoClient
connection = TinyMongoClient("ajatt")
db = connection.ajatt

def youtube(link, video_folder):
    #Get Youtube video title
    video_folder = db.settings.find_one({"_id":"settings"})['video_folder']
    video = pytube.YouTube(link)

    #Get video title and remove all bad chars
    video_title = video.title
    bad_characters = ['<','>',':','"','/','\\','|','?','*']
    for character in bad_characters:
        video_title = video_title.replace(character, "")

    #Check if file exists and create alt filename if True
    if os.path.exists(f'{video_folder}\{video_title}.mp4') == True:
        num = 1
        while os.path.exists(f'{video_folder}\{video_title}({num}).mp4'):
            num += 1
        video_title = f'{video_title}({num})'

    #Set download options and download video
    options = {
        'outtmpl': video_folder+'/'+ video_title + '.%(ext)s',
        'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([link])

    output_file = f'{video_folder}\{video_title}.mp4'
    return output_file

def video(link, video_folder):
    #Set download options and download video
    options = {
        'outtmpl': video_folder+'/%(title)s.%(ext)s',
        'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        video_title = ydl.extract_info(link, download=False).get('title', None)
        ydl.download([link])

    output_file = f"{video_folder}\{video_title}.mp4"
    return output_file

def video_download(task_id, video_folder):
    task = db.video.find_one({"_id": task_id})
    link, website = task['link'], task['website']

    if website.lower() == "youtube":
        output_file = youtube(link, video_folder)
    else:
        output_file = video(link, video_folder)
    
    #Update task status
    db.video.update_one({"_id": task_id}, {"status": "Complete", "file_path": output_file})
