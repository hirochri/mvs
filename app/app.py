from flask import Flask
from pymongo import MongoClient

# Define server app.
app = Flask(__name__)

@app.route("/api/")
def hello_world():
  users = MongoClient(get_db_name(), 27017).demo.users
  users.insert_one({"username": "lightscalar"})
  users.insert_one({"username": "hirochri"})

  return get_db_name() + ' ' + str(users.count()) + ' API:Hello World from Flask'

#Workaround for now
def get_db_name():
  return "localhost" if app.debug else "mongo-database"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
