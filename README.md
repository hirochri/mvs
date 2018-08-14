To run all the docker containers at once:

In the main directory run
```
docker-compose build
docker-compose up
```
And then access via the IP address (website uses default port 80)

To run everything separately for ease of development:

For the API on port 3000, run this in app/
```
python app.py
```

For a standalone mongo container on port 27017, run this in app/
Make sure to shut it down before running docker-compose
```
bash dev_mongo start
```
```
bash dev_mongo stop
```

To serve images/videos while using all the local running stuff above, run
a webserver on port 8080 in data/media/
```
python -m http.server 8080
```

For a standalone frontend on port 8000, run this in nginx/mvs\_website/
(Make sure the ip in nginx/mvs\_website/.env is correct)
```
npm run dev
```
And then access via the IP address and port 8000

