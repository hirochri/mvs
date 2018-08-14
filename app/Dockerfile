FROM python:3.6
RUN apt-get update && \
    apt-get -y install ffmpeg
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./wsgi.py /wsgi.py
COPY ./app.py /app.py
COPY ./video_processor.py /video_processor.py
COPY ./data_generator.py /data_generator.py
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "wsgi:app"]
