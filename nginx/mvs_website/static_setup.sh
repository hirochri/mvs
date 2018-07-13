#!/bin/sh
#echo XXX
#pwd
#echo XXX
#npm install
npm run build
cp index.html /usr/share/nginx/html/index.html
cp -r dist/ /usr/share/nginx/html/dist/

