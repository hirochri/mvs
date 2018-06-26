import tempfile
from flask import Flask, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        with tempfile.TemporaryDirectory() as dirpath:
          file.save(os.path.join(dirpath, file.filename))
          print(os.path.join(dirpath, file.filename))
          import ipdb; ipdb.set_trace()
        return redirect(url_for('upload_file',
                                filename=file.filename))
    return '''
    <!doctype html>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
