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
from video_processor import VideoFunctions, VideoProcessor

app = Flask(__name__)

#XXX for local testing
cors = CORS(app, resources={"/api/*": {"origins": "*"}})

##### Helper functions #####

#For when everything is running locally
def get_media_folder():
  return '../data/media/' if app.debug else '/data/media/'

def get_media_collection():
  hostname = "localhost" if app.debug else "mongo"
  client = MongoClient(hostname, 27017)
  return client.app_database.media

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

##### API #####

@app.route("/api/contact/", methods=['POST'])
def send_email():
  data = request.get_json()
  name, email, subject, message = data['name'], data['email'], data['subject'], data['message']

  #TODO Handle email validation server side

  full_message = '\n'.join(['From: {0} {1}'.format(name, email), 'Subject: {0}'.format(subject), 'Message: \n{0}'.format(message)])

  #Bot login info and point of contact stored in text file
  with open('contact.txt', 'r') as f:
    bot_email, bot_password, receiver_email  = f.readline().split()

  with yagmail.SMTP(bot_email, bot_password) as yag:
    yag.send(to=receiver_email, subject=subject, contents=full_message)

  return '', 200



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

  #Store info in database
  media = get_media_collection()
  doc = {
      'uuid': uuid,
      'processed': [] #filenames
      }

  media.insert_one(doc)

  ret = {'fps': str(fps), 'duration': str(duration)}

  return json.dumps(ret), 200

@app.route("/api/video/remove/<uuid>", methods=['DELETE'])
def video_remove(uuid):
  media = get_media_collection()
  query = {'uuid': uuid}

  if not media.find_one(query):
    return uuid + ' not found and not removed', 404
  else:
    media.delete_one(query)
    shutil.rmtree(get_media_folder() + uuid)
    return 'Removed ' + uuid, 200

@app.route("/api/video/process/<uuid>", methods=["POST"])
def video_process(uuid):
  media = get_media_collection()
  query = {'uuid': uuid}
  doc = media.find_one(query)

  if not doc:
    return uuid + ' not found and not processed', 404
  else:
    data = request.get_json()
    rate, option = data['samplingRate'], data['samplingOption']
    funcs = [getattr(VideoFunctions, funcname) for funcname in data['selectedVideoFunctions']]
    
    new_processed_file = '_'.join([str(rate), str(option)]) + '.processed.mp4'
    if new_processed_file not in doc['processed']:
      media.update_one({'_id': doc['_id']},{'$push': {'processed': new_processed_file}}, upsert=False)
      input_filename = get_media_folder() + uuid + '/original.mp4'
      output_filename = get_media_folder() + uuid + '/' + new_processed_file

      vp = VideoProcessor(funcs)
      vp.process_video(input_filename, output_filename, rate, option) #Has standard output fps of 10 and no composition

    return 'Processed ' + uuid, 200

@app.route("/api/video/get_processed/<uuid>", methods=["GET"])
def video_get_processed(uuid):
  media = get_media_collection()
  query = {'uuid': uuid}
  doc = media.find_one(query)

  if not doc:
    return json.dumps([]), 404
  else:
    filenames = ['/' + uuid + '/' + filename for filename in doc['processed']]
    return json.dumps(filenames), 200

@app.route("/api/video/functions/", methods=["GET"])
def video_get_functions():
  #Returns function names as strings
  return json.dumps([func for func in dir(VideoFunctions) if callable(getattr(VideoFunctions, func)) and not func.startswith("__")]), 200

'''
Notes on testing with curl:

1. Curl with form data and file (initial video post)
curl -F 'file=@<filename>' -F 'form_key=form_value' <ip_addr>

2. Curl with json data (video processing post)
curl -H 'Content-Type: application/json' -X POST -d '{"samplingRate": 5, "samplingOption": 0}' 192.168.2.8:3000/api/video/process/hirotest2
'''

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=3000)
