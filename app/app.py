from flask import Flask, jsonify, request, send_file, make_response
from pymongo import MongoClient
from flask_cors import CORS
import json
import yagmail
import os
import time
import cv2
import shutil
import math

# Define server app.
app = Flask(__name__)
cors = CORS(app, resources={"/api/*": {"origins": "*"}}) #XXX for local testing

def get_media_collection():
  hostname = "localhost" if app.debug else "mongo"
  client = MongoClient(hostname, 27017)
  return client.app_database.media

@app.route("/api/")
def hello_world():
  media = get_media_collection()
  media.insert_one({"username": "lightscalar"})
  media.insert_one({"username": "hirochri"})

  return str(media.count()) + ' Media insertions'

@app.route("/api/contact/", methods=['POST'])
def send_email():
  data = request.get_json()
  print(data)
  name, email, subject, message = data['name'], data['email'], data['subject'], data['message']

  #TODO Handle email validation server side

  full_message = '\n'.join(['From: {0} {1}'.format(name, email), 'Subject: {0}'.format(subject), 'Message: \n{0}'.format(message)])
  print(full_message)

  with open('contact.txt', 'r') as f:
    bot_email, bot_password, receiver_email  = f.readline().split()

  with yagmail.SMTP(bot_email, bot_password) as yag:
    yag.send(to=receiver_email, subject=subject, contents=full_message)

  return '', 200

def save_thumbnail(uuid):
  filename = get_media_folder() + uuid + '/original.mp4'

  cap = cv2.VideoCapture(filename)
  success, frame = cap.read()
  while not success:
    success, frame = cap.read()

  cv2.imwrite(get_media_folder() + uuid + '/thumbnail.jpg', frame)
  fps = int(cap.get(cv2.CAP_PROP_FPS))
  num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  duration = int(math.ceil(float(num_frames) / float(fps)))

  return fps, duration

#Curl with form data and file
#curl -F 'file=@<filename>' -F 'form_key=form_value' <ip_addr>

@app.route("/api/video/upload", methods=['POST'])
def video_upload():
  #Download video file
  uuid = request.form['uuid']
  os.mkdir(get_media_folder() + uuid)
  filename = get_media_folder() + uuid + '/original.mp4'
  file = request.files['file']
  file.save(filename)

  #Grab thumbnail
  fps, duration = save_thumbnail(uuid)
  print(fps, duration)

  #Store info in database
  media = get_media_collection()
  doc = {
      'uuid': uuid,
      }

  media.insert_one(doc)

  ret = {'fps': str(fps), 'duration': str(duration)}

  return json.dumps(ret), 200

@app.route("/api/video/remove/<uuid>", methods=['DELETE'])
def video_remove(uuid):
  media = get_media_collection()
  query = {'uuid': uuid}

  if media.find_one(query):
    media.delete_one(query)
    shutil.rmtree(get_media_folder() + uuid)
    return 'Removed ' + uuid, 200
  else:
    return uuid + ' not found and not removed', 404

#Ex test command: curl -H 'Content-Type: application/json' -X POST -d '{"samplingRate": 5, "samplingOption": 0}' 192.168.2.8:3000/api/video/process/hirotest2
@app.route("/api/video/process/<uuid>", methods=["POST"])
def video_process(uuid):
  #TODO file check abstraction
  #Keep track of already processed vs allow reprocessing with different options?
  media = get_media_collection()
  query = {'uuid': uuid}

  time.sleep(3)

  if media.find_one(query):
    filename = get_media_folder() + uuid + '/processed.mp4'
    data = request.get_json()
    rate, option = data['samplingRate'], data['samplingOption']
    print(rate, option)
    print('Processing', uuid)
    return 'Processed ' + uuid, 200
  else:
    return uuid + ' not found and not processed', 404

'''
Video stages -> uploaded, processed, 

TODO
* Upload video
* Remove video
* Process video
* Compose videos together


'''

def get_media_folder():
  return '../data/media/' if app.debug else '/data/media/'

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=3000)
