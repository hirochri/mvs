#!/bin/bash

#Development version of the app, so we don't have to go through 
#NGINX and gunicorn every time

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
