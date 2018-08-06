FROM python:3.6
#TODO make sure ffmpeg is installed
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./app.py /app.py
COPY ./wsgi.py /wsgi.py
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "wsgi:app"]
