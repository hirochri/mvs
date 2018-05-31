FROM python:3.6
COPY . /
RUN pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "wsgi:app"]
