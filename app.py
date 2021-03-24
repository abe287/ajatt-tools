from flask import Flask, render_template, request, Response, url_for
import webview

import multiprocessing, os, psutil

from tinymongo import TinyMongoClient

import datetime
import time
import subprocess

#Define flask app and window
app = Flask(__name__, static_url_path='/static')

window = webview.create_window('AJATT', app, width=1400, height=850, frameless=True, background_color="#181F39")

from audiodownload import *
from videodownload import *

@app.route('/')
def index():
    #Create settings collection & document on first run
    if db.settings.count() == 0:
        db.settings.insert_one({"_id": "settings", "audio_folder": None, "video_folder": None})

    return render_template('index.html')

@app.route('/audio')
def audio():
    audio_objects = list(db.audio.find())
    return render_template('audio.html', audio_objects = audio_objects)

@app.route('/add_audio_links', methods=['POST'])
def add_audio_links():
    links = request.form['links'].split('\n')
    links = list(map(lambda each:each.strip("\r"), links))
    links = list(filter(None, links))

    today = datetime.date.today()
    date = today.strftime("%m/%d/%y")

    for link in links:
        if "youtube" in link.lower():
            website = "YouTube"
            db.audio.insert_one({"website": website, "date": date, "status": "Idle", "link": link, "file_path": None, "process_id": None})

    audio_objects = list(db.audio.find())
    return render_template('audio_body.html', audio_objects = audio_objects)

@app.route('/delete_audio_task', methods=['POST'])
def delete_audio_task():
    #Get audio task id from post request
    task_id = request.form['task_id']
    #Remove task from database
    db.audio.remove({"_id":task_id})

    #Get updated audio tasks and render html for frontend
    audio_objects = list(db.audio.find())
    return render_template('audio_body.html', audio_objects = audio_objects)

@app.route('/start_audio_download', methods=['POST'])
def start_audio_download():
    #Get audio task id from post request
    task_id = request.form['task_id']

    #Get default audio folder path
    audio_folder = db.settings.find_one({"_id":"settings"})['audio_folder']
    if audio_folder == None:
        return {"success": False, "error_type": "no_default_audio_folder"}

    #Spwan a process
    process = multiprocessing.Process(target=audio_download, args=(task_id, audio_folder, ))
    process.start()

    #Save process id to database
    process_id = process.pid
    db.audio.update({"_id":task_id}, {"status": "Downloading", "process_id": process_id})

    audio_objects = list(db.audio.find())
    audio_html = render_template('audio_body.html', audio_objects = audio_objects)
    
    return {"success": True, "audio_html": audio_html}

@app.route('/open_audio_file', methods=['POST'])
def open_file():
    task_id = request.form['task_id']
    task = db.audio.find_one({"_id": task_id})
    
    if task['file_path'] == None:
        return {"success": False, "error_type": "no_file_path"}
    else:
        path = task['file_path']
        if os.path.isfile(path) == True:
            #Open file
            subprocess.Popen(f'explorer /select, {path}')
            return {"success": True}
        else:
            return {"success": False, "error_type": "file_not_found"}




@app.route('/video')
def video():
    video_objects = list(db.video.find())
    return render_template('video.html', video_objects = video_objects)

@app.route('/add_video_links', methods=['POST'])
def add_video_links():
    links = request.form['links'].split('\n')
    links = list(map(lambda each:each.strip("\r"), links))
    links = list(filter(None, links))

    today = datetime.date.today()
    date = today.strftime("%m/%d/%y")

    for link in links:
        website = None
        if "youtube" in link.lower():
            website = "YouTube"
        elif "crunchyroll" in link.lower():
            website = "Crunchyroll"

        if website != None:
            db.video.insert_one({"website": website, "date": date, "status": "Idle", "link": link, "file_path": None, "process_id": None})

    video_objects = list(db.video.find())
    return render_template('video_body.html', video_objects = video_objects)

@app.route('/start_video_download', methods=['POST'])
def start_video_download():
    #Get video task id from post request
    task_id = request.form['task_id']

    #Get default video folder path
    video_folder = db.settings.find_one({"_id":"settings"})['video_folder']
    if video_folder == None:
        return {"success": False, "error_type": "no_default_video_folder"}

    #Spwan a process
    process = multiprocessing.Process(target=video_download, args=(task_id, video_folder, ))
    process.start()

    #Save process id to database
    process_id = process.pid
    db.video.update({"_id":task_id}, {"status": "Downloading", "process_id": process_id})

    video_objects = list(db.video.find())
    video_html = render_template('video_body.html', video_objects = video_objects)

    return {"success": True, "video_html": video_html}

@app.route('/stop_video_download', methods=['POST'])
def stop_video_download():
    #Read task id from ajax post
    task_id = request.form['task_id']

    #Get process_id from database
    task = db.video.find_one({"_id":task_id})
    process_id = task['process_id']

    #Kill process
    process = psutil.Process(process_id)
    process.terminate()

    #Update databse
    db.video.update({"_id":task_id}, {"status": "Idle"})

    video_objects = list(db.video.find())
    video_html = render_template('video_body.html', video_objects = video_objects)
    
    return {"success": True, "video_html": video_html}

@app.route('/stop_audio_download', methods=['POST'])
def stop_audio_download():
    #Read task id from ajax post
    task_id = request.form['task_id']

    #Get process_id from database
    task = db.audio.find_one({"_id":task_id})
    process_id = task['process_id']

    #Kill process
    process = psutil.Process(process_id)
    process.terminate()

    #Update databse
    db.audio.update({"_id":task_id}, {"status": "Idle"})

    audio_objects = list(db.audio.find())
    audio_html = render_template('audio_body.html', audio_objects = audio_objects)
    
    return {"success": True, "audio_html": audio_html}

@app.route('/delete_video_task', methods=['POST'])
def delete_video_task():
    #Get video task id from post request
    task_id = request.form['task_id']
    #Remove task from database
    db.video.remove({"_id":task_id})

    #Get updated video tasks and render html for frontend
    video_objects = list(db.video.find())
    return render_template('video_body.html', video_objects = video_objects)





@app.route('/open_video_file', methods=['POST'])
def open_video_file():
    task_id = request.form['task_id']
    task = db.video.find_one({"_id": task_id})
    
    if task['file_path'] == None:
        return {"success": False, "error_type": "no_file_path"}
    else:
        path = task['file_path']
        if os.path.isfile(path) == True:
            #Open file
            subprocess.Popen(f'explorer /select, {path}')
            return {"success": True}
        else:
            return {"success": False, "error_type": "file_not_found"}


@app.route("/settings")
def settings():
    settings = list(db.settings.find())
    return render_template('settings.html', settings = settings)

@app.route("/update_settings", methods=['POST'])
def update_settings():
    audio_folder = None if request.form['audio_folder'].strip() == "" else request.form['audio_folder']
    video_folder = None if request.form['video_folder'].strip() == "" else request.form['video_folder']

    db.settings.update({"_id":"settings"}, {"audio_folder": audio_folder, "video_folder": video_folder})
    
    settings = list(db.settings.find())
    html = render_template('settings.html', settings = settings)
    return {"success": True, "html": html}


@app.route("/get_progress")
def get_progress():
    #Get audio tasks
    audio_objects = list(db.audio.find())
    audio_html = render_template("audio_body.html", audio_objects = audio_objects)

    #Get video tasks
    video_objects = list(db.video.find())
    video_html = render_template("video_body.html", video_objects = video_objects)

    data = {"audio_html": audio_html, "video_html": video_html}
    return data

@app.route('/close_window', methods=["POST"])
def close_window():
    #Add logic to kill all running processes (tasks) before closing

    #Close window after stoping all tasks
    window.destroy()
    return "closed_window"

@app.route('/minimize_window', methods=["POST"])
def minimize_window():
    window.minimize()
    return "minimized_wwindow"

@app.route('/maximize_window', methods=["POST"])
def maximize_window():
    if window.width == 1384:
        window.resize(width=1600, height=950)
    else:
        window.resize(width=1384, height=811)
    return "maximized_window"


#Start app
if __name__ == '__main__':
    #Connect to the database
    connection = TinyMongoClient("ajatt")
    db = connection.ajatt

    #Start webview GUI
    webview.start()