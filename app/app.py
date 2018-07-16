from flask import Flask, jsonify, request, send_file, make_response
from pymongo import MongoClient
from flask_cors import CORS
import json
import yagmail
import os

# Define server app.
app = Flask(__name__)
cors = CORS(app, resources={"/api/*": {"origins": "*"}})

upload_folder = '../data/uploads/'
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route("/api/")
def hello_world():
  users = MongoClient(get_db_name(), 27017).demo.users
  users.insert_one({"username": "lightscalar"})
  users.insert_one({"username": "hirochri"})

  return get_db_name() + ' ' + str(users.count()) + ' API:Hello World from Flask'

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

@app.route("/api/video/upload", methods=['POST'])
def video_test():
  #TODO store uploaded videos and results by .. user?
  #Get videos grouped together from same upload somehow
  #Multiple files can be sent in one request

  uuid = request.form['uuid']
  print(uuid)
  filename = '../data/uploads/' + uuid + '.mp4'
  file = request.files['file']
  file.save(filename)

  return '', 200

@app.route("/api/video/remove/<uuid>")
def video_remove(uuid):
  pass

@app.route("/api/test/", methods=['GET'])
def testfunc():
  response = make_response(send_file('../data/uploads/test.mp4', mimetype='video/mp4'))
  response.headers['Content-Disposition'] = 'inline'

  return response

#Workaround for now
def get_db_name():
  return "localhost" if app.debug else "mongo-database"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
