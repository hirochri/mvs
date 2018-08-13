#!/bin/bash

#Development version of the mongo container, so we don't have to go through NGINX and gunicorn every time
#Can lead to docker-compose complaining about the port already being allocated
#if the development mongo container isn't stopped beforehand

#Usage:
#bash dev_mongo.sh start
#bash dev_mongo.sh stop

if [ "$1" == "start" ]; then
  #The mongo container get destroyed upon exit
  docker run --rm -p 27017:27017 -d --name dev-mongo mongo:latest
elif [ "$1" == "stop" ]; then
  mongo_id=$(docker container ls | grep 'dev-' | awk '{print $1}')
  if [ -n "$mongo_id" ]; then
    docker container stop "$mongo_id"
  else
    echo "Mongo is not running"
    exit 1
  fi
else
  echo "Invalid Command: Valid commands are start / stop"
fi
