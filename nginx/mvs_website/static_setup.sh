#!/bin/sh
#pwd
npm install
npm run build
cp index.html /usr/share/nginx/html/index.html
cp -r dist/ /usr/share/nginx/html/dist/

