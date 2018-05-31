from flask import Flask
from pymongo import MongoClient


# Connect to MongoDB, just to show we can
users = MongoClient("mongo-database", 27017).demo.users
users.insert_one({"username": "lightscalar"})
users.insert_one({"username": "hirochri"})

# Define server app.
app = Flask(__name__)

@app.route("/")
def hello_world():
  print(users.count)
  return 'Hello World from App, we have users: ' + str(users.count())

@app.route("/test")
def test():
  return 'Testing another route'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
